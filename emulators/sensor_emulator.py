"""
IoT Parking Sensor Emulator
Simulates ultrasonic sensors detecting vehicle presence
"""
import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime

# MQTT Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
TOPIC_SPOT_STATUS = "parkmate/spot/status"
TOPIC_LED_COMMAND = "parkmate/led/command"

class ParkingSensorEmulator:
    def __init__(self, spot_id, lot_id):
        self.spot_id = spot_id
        self.lot_id = lot_id
        self.occupied = False
        self.distance = 200  # cm - empty spot distance
        self.led_color = "green"

        # MQTT Client
        self.client = mqtt.Client(client_id=f"sensor_{spot_id}")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        print(f"Sensor {self.spot_id} connected to MQTT broker with code {rc}")
        # Subscribe to LED commands for this spot
        self.client.subscribe(TOPIC_LED_COMMAND)

    def on_message(self, client, userdata, msg):
        try:
            if msg.topic == TOPIC_LED_COMMAND:
                payload = json.loads(msg.payload.decode())
                if payload.get('spot_id') == self.spot_id:
                    self.led_color = payload.get('color', 'green')
                    print(f"Sensor {self.spot_id}: LED -> {self.led_color.upper()}")
        except Exception as e:
            print(f"Error processing message: {e}")

    def measure_distance(self):
        """Simulate ultrasonic distance measurement"""
        if self.occupied:
            # Car present: distance between 10-50cm
            return random.randint(10, 50)
        else:
            # Empty spot: distance around 200cm (floor)
            return random.randint(180, 220)

    def detect_vehicle(self):
        """Simulate vehicle detection based on distance threshold"""
        self.distance = self.measure_distance()

        # Threshold: < 100cm means occupied
        new_status = self.distance < 100

        # Check if status changed
        if new_status != self.occupied:
            self.occupied = new_status
            return True  # Status changed
        return False  # No change

    def publish_status(self):
        """Publish spot status to MQTT broker"""
        payload = {
            'spot_id': self.spot_id,
            'lot_id': self.lot_id,
            'occupied': self.occupied,
            'distance': self.distance,
            'timestamp': datetime.now().isoformat()
        }

        self.client.publish(TOPIC_SPOT_STATUS, json.dumps(payload))
        status = "OCCUPIED" if self.occupied else "AVAILABLE"
        print(f"Sensor {self.spot_id}: {status} (distance: {self.distance}cm)")

    def simulate_random_event(self):
        """Randomly change occupancy status to simulate cars parking/leaving"""
        if random.random() < 0.1:  # 10% chance each cycle
            self.occupied = not self.occupied
            return True
        return False

    def connect(self):
        """Connect to MQTT broker"""
        try:
            self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
            self.client.loop_start()
            return True
        except Exception as e:
            print(f"Connection error for sensor {self.spot_id}: {e}")
            return False

    def disconnect(self):
        """Disconnect from MQTT broker"""
        self.client.loop_stop()
        self.client.disconnect()


def run_simulation(num_spots=20, lot_id="LOT001", update_interval=5):
    """
    Run the parking sensor simulation

    Args:
        num_spots: Number of parking spots to simulate
        lot_id: Parking lot identifier
        update_interval: Seconds between sensor updates
    """
    print(f"Starting ParkMate Sensor Emulator")
    print(f"Simulating {num_spots} parking spots in {lot_id}")
    print(f"Update interval: {update_interval} seconds")
    print(f"Connecting to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")
    print("-" * 60)

    # Create sensors
    sensors = []
    for i in range(1, num_spots + 1):
        spot_id = f"SPOT{i:03d}"
        sensor = ParkingSensorEmulator(spot_id, lot_id)

        if sensor.connect():
            sensors.append(sensor)
            time.sleep(0.1)  # Small delay between connections
        else:
            print(f"Failed to connect sensor {spot_id}")

    if not sensors:
        print("No sensors connected. Exiting.")
        return

    print(f"\n{len(sensors)} sensors connected successfully!")
    print("Simulation running... (Press Ctrl+C to stop)\n")

    try:
        # Initial status publish
        for sensor in sensors:
            sensor.publish_status()
            time.sleep(0.05)

        # Main simulation loop
        while True:
            time.sleep(update_interval)

            # Randomly simulate parking events
            for sensor in sensors:
                if sensor.simulate_random_event():
                    sensor.publish_status()

    except KeyboardInterrupt:
        print("\n\nStopping simulation...")
        for sensor in sensors:
            sensor.disconnect()
        print("All sensors disconnected. Goodbye!")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='ParkMate IoT Sensor Emulator')
    parser.add_argument('--spots', type=int, default=20, help='Number of parking spots (default: 20)')
    parser.add_argument('--lot', type=str, default='LOT001', help='Parking lot ID (default: LOT001)')
    parser.add_argument('--interval', type=int, default=5, help='Update interval in seconds (default: 5)')

    args = parser.parse_args()

    run_simulation(
        num_spots=args.spots,
        lot_id=args.lot,
        update_interval=args.interval
    )
