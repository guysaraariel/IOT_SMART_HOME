"""
IoT DHT Sensor Emulator (Temperature & Humidity)
Simulates DHT11/DHT22 environmental sensors
Monitors parking lot environmental conditions
"""
import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime

# MQTT Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
TOPIC_ENVIRONMENT = "parkmate/environment"
TOPIC_ALERTS = "parkmate/alerts"

# Color codes for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class DHTSensorEmulator:
    def __init__(self, sensor_id, lot_id):
        self.sensor_id = sensor_id
        self.lot_id = lot_id

        # Environmental parameters (realistic ranges)
        self.temperature = 22.0  # Celsius
        self.humidity = 50.0     # Percentage
        self.heat_index = 22.0   # Feels like temperature

        # Alert thresholds
        self.temp_high_threshold = 35.0   # Hot day
        self.temp_low_threshold = 0.0     # Freezing
        self.humidity_high_threshold = 80.0  # Very humid
        self.humidity_low_threshold = 20.0   # Very dry

        # MQTT Client
        self.client = mqtt.Client(client_id=f"dht_{sensor_id}")
        self.client.on_connect = self.on_connect

    def on_connect(self, client, userdata, flags, rc):
        print(f"{Colors.BLUE}{Colors.BOLD}╔════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.BLUE}{Colors.BOLD}║     DHT SENSOR EMULATOR STARTED           ║{Colors.RESET}")
        print(f"{Colors.BLUE}{Colors.BOLD}╚════════════════════════════════════════════╝{Colors.RESET}")
        print(f"{Colors.GREEN}✓ Connected to MQTT Broker (RC: {rc}){Colors.RESET}")
        print(f"{Colors.GREEN}✓ Sensor ID: {self.sensor_id}{Colors.RESET}")
        print(f"{Colors.GREEN}✓ Parking Lot: {self.lot_id}{Colors.RESET}")
        print(f"{Colors.GREEN}✓ Publishing to: {TOPIC_ENVIRONMENT}{Colors.RESET}")
        print(f"{Colors.YELLOW}{'─' * 50}{Colors.RESET}\n")

    def simulate_temperature(self):
        """Simulate realistic temperature fluctuations"""
        # Small random walk with bounds
        change = random.uniform(-0.5, 0.5)
        self.temperature += change

        # Keep within realistic bounds (0°C to 40°C)
        self.temperature = max(0.0, min(40.0, self.temperature))

        # Round to 1 decimal place
        self.temperature = round(self.temperature, 1)

        return self.temperature

    def simulate_humidity(self):
        """Simulate realistic humidity fluctuations"""
        # Small random walk with bounds
        change = random.uniform(-2.0, 2.0)
        self.humidity += change

        # Keep within realistic bounds (20% to 90%)
        self.humidity = max(20.0, min(90.0, self.humidity))

        # Round to 1 decimal place
        self.humidity = round(self.humidity, 1)

        return self.humidity

    def calculate_heat_index(self):
        """Calculate heat index (feels like temperature)"""
        # Simplified heat index calculation
        t = self.temperature
        h = self.humidity

        if t >= 27:  # Heat index only relevant at higher temps
            hi = -8.78469475556 + 1.61139411 * t + 2.33854883889 * h
            hi += -0.14611605 * t * h + -0.012308094 * t * t
            hi += -0.0164248277778 * h * h + 0.002211732 * t * t * h
            hi += 0.00072546 * t * h * h + -0.000003582 * t * t * h * h
            self.heat_index = round(hi, 1)
        else:
            self.heat_index = t

        return self.heat_index

    def check_alerts(self):
        """Check if environmental conditions require alerts"""
        alerts = []

        # Temperature alerts
        if self.temperature >= self.temp_high_threshold:
            alerts.append({
                'type': 'HIGH_TEMPERATURE',
                'severity': 'WARNING',
                'message': f'High temperature detected: {self.temperature}°C',
                'recommendation': 'Ensure parking lot ventilation is adequate'
            })
        elif self.temperature <= self.temp_low_threshold:
            alerts.append({
                'type': 'LOW_TEMPERATURE',
                'severity': 'WARNING',
                'message': f'Freezing temperature detected: {self.temperature}°C',
                'recommendation': 'Check for ice on parking surfaces'
            })

        # Humidity alerts
        if self.humidity >= self.humidity_high_threshold:
            alerts.append({
                'type': 'HIGH_HUMIDITY',
                'severity': 'INFO',
                'message': f'High humidity detected: {self.humidity}%',
                'recommendation': 'Monitor for condensation issues'
            })
        elif self.humidity <= self.humidity_low_threshold:
            alerts.append({
                'type': 'LOW_HUMIDITY',
                'severity': 'INFO',
                'message': f'Low humidity detected: {self.humidity}%',
                'recommendation': 'Static electricity risk increased'
            })

        # Heat index alert
        if self.heat_index >= 32:
            alerts.append({
                'type': 'HIGH_HEAT_INDEX',
                'severity': 'WARNING',
                'message': f'High heat index: {self.heat_index}°C',
                'recommendation': 'Extreme heat conditions - ensure shade availability'
            })

        return alerts

    def publish_reading(self):
        """Publish sensor reading to MQTT"""
        # Update readings
        temp = self.simulate_temperature()
        humid = self.simulate_humidity()
        hi = self.calculate_heat_index()

        timestamp = datetime.now().isoformat()

        # Prepare payload
        payload = {
            'sensor_id': self.sensor_id,
            'lot_id': self.lot_id,
            'temperature': temp,
            'humidity': humid,
            'heat_index': hi,
            'unit_temp': 'celsius',
            'unit_humidity': 'percent',
            'timestamp': timestamp
        }

        # Publish to MQTT
        self.client.publish(TOPIC_ENVIRONMENT, json.dumps(payload))

        # Display reading
        self.display_reading(temp, humid, hi, timestamp)

        # Check and publish alerts
        alerts = self.check_alerts()
        if alerts:
            self.publish_alerts(alerts)

    def display_reading(self, temp, humid, hi, timestamp):
        """Display sensor reading with visual indicators"""
        time_str = datetime.now().strftime("%H:%M:%S")

        # Temperature color coding
        if temp >= 30:
            temp_color = Colors.RED
            temp_icon = "🔥"
        elif temp >= 20:
            temp_color = Colors.GREEN
            temp_icon = "🌡️"
        else:
            temp_color = Colors.CYAN
            temp_icon = "❄️"

        # Humidity color coding
        if humid >= 70:
            humid_color = Colors.BLUE
            humid_icon = "💧"
        elif humid >= 40:
            humid_color = Colors.GREEN
            humid_icon = "💨"
        else:
            humid_color = Colors.YELLOW
            humid_icon = "🏜️"

        # Heat index color coding
        if hi >= 32:
            hi_color = Colors.RED
        elif hi >= 27:
            hi_color = Colors.YELLOW
        else:
            hi_color = Colors.GREEN

        print(f"{Colors.CYAN}[{time_str}]{Colors.RESET} Environmental Reading:")
        print(f"  {temp_icon} Temperature: {temp_color}{temp}°C{Colors.RESET}")
        print(f"  {humid_icon} Humidity: {humid_color}{humid}%{Colors.RESET}")
        print(f"  🌡️  Heat Index: {hi_color}{hi}°C{Colors.RESET} (feels like)")
        print(f"  📍 Location: {Colors.BOLD}{self.lot_id}{Colors.RESET} | Sensor: {self.sensor_id}")
        print(f"{Colors.YELLOW}{'─' * 50}{Colors.RESET}\n")

    def publish_alerts(self, alerts):
        """Publish alerts to MQTT"""
        for alert in alerts:
            timestamp = datetime.now().isoformat()

            payload = {
                'sensor_id': self.sensor_id,
                'lot_id': self.lot_id,
                'alert': alert,
                'timestamp': timestamp
            }

            self.client.publish(TOPIC_ALERTS, json.dumps(payload))

            # Display alert
            severity_color = Colors.RED if alert['severity'] == 'WARNING' else Colors.YELLOW

            print(f"{severity_color}⚠️  ALERT - {alert['type']}{Colors.RESET}")
            print(f"  Severity: {severity_color}{alert['severity']}{Colors.RESET}")
            print(f"  Message: {alert['message']}")
            print(f"  Recommendation: {Colors.CYAN}{alert['recommendation']}{Colors.RESET}")
            print(f"{Colors.YELLOW}{'─' * 50}{Colors.RESET}\n")

    def connect(self):
        """Connect to MQTT broker"""
        try:
            self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
            self.client.loop_start()
            return True
        except Exception as e:
            print(f"{Colors.RED}✗ Connection error: {e}{Colors.RESET}")
            return False

    def disconnect(self):
        """Disconnect from MQTT broker"""
        self.client.loop_stop()
        self.client.disconnect()

def run_simulation(sensor_id="DHT001", lot_id="LOT001", interval=10):
    """
    Run the DHT sensor simulation

    Args:
        sensor_id: Sensor identifier
        lot_id: Parking lot identifier
        interval: Reading interval in seconds
    """
    print(f"\n{Colors.BOLD}Starting DHT Sensor Emulator{Colors.RESET}")
    print(f"Sensor ID: {sensor_id}")
    print(f"Parking Lot: {lot_id}")
    print(f"Reading Interval: {interval} seconds")
    print(f"Connecting to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")
    print(f"{Colors.YELLOW}{'─' * 50}{Colors.RESET}\n")

    sensor = DHTSensorEmulator(sensor_id, lot_id)

    if not sensor.connect():
        print(f"{Colors.RED}Failed to connect. Exiting.{Colors.RESET}")
        return

    time.sleep(1)  # Wait for connection

    print(f"{Colors.GREEN}Sensor active! Publishing readings every {interval} seconds...{Colors.RESET}")
    print(f"{Colors.WHITE}Press Ctrl+C to stop{Colors.RESET}\n")

    try:
        while True:
            sensor.publish_reading()
            time.sleep(interval)

    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Stopping DHT sensor emulator...{Colors.RESET}")
        sensor.disconnect()
        print(f"{Colors.GREEN}Sensor stopped. Goodbye!{Colors.RESET}\n")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='ParkMate DHT Sensor Emulator')
    parser.add_argument('--sensor', type=str, default='DHT001', help='Sensor ID (default: DHT001)')
    parser.add_argument('--lot', type=str, default='LOT001', help='Parking lot ID (default: LOT001)')
    parser.add_argument('--interval', type=int, default=10, help='Reading interval in seconds (default: 10)')

    args = parser.parse_args()

    run_simulation(
        sensor_id=args.sensor,
        lot_id=args.lot,
        interval=args.interval
    )
