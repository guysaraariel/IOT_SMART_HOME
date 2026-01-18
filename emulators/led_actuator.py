"""
IoT LED/Relay Actuator Emulator
Simulates LED indicators and relay controls for parking spots
Receives commands via MQTT and displays visual feedback
"""
import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime
import os
import sys

# MQTT Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
TOPIC_LED_COMMAND = "parkmate/led/command"
TOPIC_RELAY_COMMAND = "parkmate/relay/command"

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

class LEDActuator:
    def __init__(self, actuator_id):
        self.actuator_id = actuator_id
        self.led_states = {}  # spot_id -> color
        self.relay_states = {}  # relay_id -> state (on/off)

        # MQTT Client
        self.client = mqtt.Client(client_id=f"led_actuator_{actuator_id}")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        print(f"{Colors.CYAN}{Colors.BOLD}╔════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}║   LED/RELAY ACTUATOR EMULATOR STARTED     ║{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}╚════════════════════════════════════════════╝{Colors.RESET}")
        print(f"{Colors.GREEN}✓ Connected to MQTT Broker (RC: {rc}){Colors.RESET}")

        # Subscribe to LED and Relay command topics
        self.client.subscribe(TOPIC_LED_COMMAND)
        self.client.subscribe(TOPIC_RELAY_COMMAND)
        print(f"{Colors.GREEN}✓ Subscribed to: {TOPIC_LED_COMMAND}{Colors.RESET}")
        print(f"{Colors.GREEN}✓ Subscribed to: {TOPIC_RELAY_COMMAND}{Colors.RESET}")
        print(f"{Colors.YELLOW}{'─' * 50}{Colors.RESET}")
        print(f"{Colors.WHITE}Waiting for commands...{Colors.RESET}\n")

    def on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())

            if msg.topic == TOPIC_LED_COMMAND:
                self.handle_led_command(payload)
            elif msg.topic == TOPIC_RELAY_COMMAND:
                self.handle_relay_command(payload)

        except Exception as e:
            print(f"{Colors.RED}✗ Error processing message: {e}{Colors.RESET}")

    def handle_led_command(self, data):
        """Handle LED control commands"""
        spot_id = data.get('spot_id')
        color = data.get('color', 'green').lower()
        lot_id = data.get('lot_id', 'N/A')

        # Store LED state
        self.led_states[spot_id] = color

        # Display visual feedback
        timestamp = datetime.now().strftime("%H:%M:%S")

        if color == 'red':
            color_symbol = f"{Colors.RED}●{Colors.RESET}"
            color_text = f"{Colors.RED}RED{Colors.RESET}"
            status_text = f"{Colors.RED}OCCUPIED{Colors.RESET}"
        elif color == 'green':
            color_symbol = f"{Colors.GREEN}●{Colors.RESET}"
            color_text = f"{Colors.GREEN}GREEN{Colors.RESET}"
            status_text = f"{Colors.GREEN}AVAILABLE{Colors.RESET}"
        elif color == 'yellow':
            color_symbol = f"{Colors.YELLOW}●{Colors.RESET}"
            color_text = f"{Colors.YELLOW}YELLOW{Colors.RESET}"
            status_text = f"{Colors.YELLOW}RESERVED{Colors.RESET}"
        else:
            color_symbol = f"{Colors.WHITE}●{Colors.RESET}"
            color_text = f"{Colors.WHITE}{color.upper()}{Colors.RESET}"
            status_text = f"{Colors.WHITE}UNKNOWN{Colors.RESET}"

        print(f"{Colors.CYAN}[{timestamp}]{Colors.RESET} LED Command Received:")
        print(f"  💡 Spot: {Colors.BOLD}{spot_id}{Colors.RESET} | Lot: {lot_id}")
        print(f"  {color_symbol} Color: {color_text} → Status: {status_text}")
        print(f"{Colors.YELLOW}{'─' * 50}{Colors.RESET}\n")

    def handle_relay_command(self, data):
        """Handle Relay control commands"""
        relay_id = data.get('relay_id')
        state = data.get('state', 'off').lower()
        action = data.get('action', 'N/A')

        # Store relay state
        self.relay_states[relay_id] = state

        # Display visual feedback
        timestamp = datetime.now().strftime("%H:%M:%S")

        if state == 'on':
            state_symbol = f"{Colors.GREEN}⚡{Colors.RESET}"
            state_text = f"{Colors.GREEN}ON{Colors.RESET}"
        else:
            state_symbol = f"{Colors.WHITE}○{Colors.RESET}"
            state_text = f"{Colors.WHITE}OFF{Colors.RESET}"

        print(f"{Colors.MAGENTA}[{timestamp}]{Colors.RESET} Relay Command Received:")
        print(f"  🔌 Relay: {Colors.BOLD}{relay_id}{Colors.RESET}")
        print(f"  {state_symbol} State: {state_text} | Action: {action}")
        print(f"{Colors.YELLOW}{'─' * 50}{Colors.RESET}\n")

    def display_status(self):
        """Display current status of all LEDs and Relays"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}╔════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}║          ACTUATOR STATUS SUMMARY          ║{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}╚════════════════════════════════════════════╝{Colors.RESET}\n")

        if self.led_states:
            print(f"{Colors.BOLD}LED States:{Colors.RESET}")
            for spot_id, color in sorted(self.led_states.items()):
                symbol = f"{Colors.RED}●{Colors.RESET}" if color == 'red' else f"{Colors.GREEN}●{Colors.RESET}"
                print(f"  {symbol} {spot_id}: {color.upper()}")
            print()

        if self.relay_states:
            print(f"{Colors.BOLD}Relay States:{Colors.RESET}")
            for relay_id, state in sorted(self.relay_states.items()):
                symbol = f"{Colors.GREEN}⚡{Colors.RESET}" if state == 'on' else f"{Colors.WHITE}○{Colors.RESET}"
                print(f"  {symbol} {relay_id}: {state.upper()}")
            print()

        print(f"{Colors.YELLOW}{'─' * 50}{Colors.RESET}\n")

    def connect(self):
        """Connect to MQTT broker"""
        try:
            self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
            return True
        except Exception as e:
            print(f"{Colors.RED}✗ Connection error: {e}{Colors.RESET}")
            return False

    def run(self):
        """Run the actuator emulator"""
        if self.connect():
            self.client.loop_forever()
        else:
            print(f"{Colors.RED}Failed to connect to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}{Colors.RESET}")
            print(f"{Colors.YELLOW}Make sure Mosquitto is running!{Colors.RESET}")

if __name__ == "__main__":
    print(f"\n{Colors.BOLD}Starting LED/Relay Actuator Emulator...{Colors.RESET}\n")

    actuator = LEDActuator("001")

    try:
        actuator.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Stopping actuator emulator...{Colors.RESET}")
        actuator.display_status()
        print(f"{Colors.GREEN}Actuator emulator stopped. Goodbye!{Colors.RESET}\n")
