"""
IoT Button/Knob Actuator Emulator
Simulates physical button presses and knob adjustments
Allows manual control of parking system functions
"""
import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime
import threading
import sys

# MQTT Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
TOPIC_BUTTON_PRESS = "parkmate/button/press"
TOPIC_KNOB_ADJUST = "parkmate/knob/adjust"

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

class ButtonKnobEmulator:
    def __init__(self, device_id="BTN001"):
        self.device_id = device_id
        self.knob_value = 50  # Initial knob position (0-100)
        self.button_press_count = 0
        self.knob_adjust_count = 0

        # MQTT Client
        self.client = mqtt.Client(client_id=f"button_knob_{device_id}")
        self.client.on_connect = self.on_connect
        self.running = True

    def on_connect(self, client, userdata, flags, rc):
        print(f"{Colors.MAGENTA}{Colors.BOLD}╔════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.MAGENTA}{Colors.BOLD}║   BUTTON/KNOB ACTUATOR EMULATOR STARTED   ║{Colors.RESET}")
        print(f"{Colors.MAGENTA}{Colors.BOLD}╚════════════════════════════════════════════╝{Colors.RESET}")
        print(f"{Colors.GREEN}✓ Connected to MQTT Broker (RC: {rc}){Colors.RESET}")
        print(f"{Colors.GREEN}✓ Device ID: {self.device_id}{Colors.RESET}")
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

    def press_button(self, spot_id, action="toggle"):
        """Simulate button press to control a parking spot"""
        self.button_press_count += 1
        timestamp = datetime.now().isoformat()

        payload = {
            'button_id': self.device_id,
            'spot_id': spot_id,
            'action': action,
            'pressed': True,
            'timestamp': timestamp,
            'press_count': self.button_press_count
        }

        self.client.publish(TOPIC_BUTTON_PRESS, json.dumps(payload))

        print(f"{Colors.GREEN}[{datetime.now().strftime('%H:%M:%S')}]{Colors.RESET} Button Pressed:")
        print(f"  🔘 Button: {Colors.BOLD}{self.device_id}{Colors.RESET}")
        print(f"  🅿️  Spot: {Colors.BOLD}{spot_id}{Colors.RESET}")
        print(f"  ⚡ Action: {Colors.CYAN}{action}{Colors.RESET}")
        print(f"  📊 Press Count: {self.button_press_count}")
        print(f"{Colors.YELLOW}{'─' * 50}{Colors.RESET}\n")

    def adjust_knob(self, adjustment, function="parking_time"):
        """Simulate knob rotation to adjust values"""
        self.knob_adjust_count += 1

        # Adjust knob value (0-100 range)
        self.knob_value += adjustment
        self.knob_value = max(0, min(100, self.knob_value))

        timestamp = datetime.now().isoformat()

        payload = {
            'knob_id': self.device_id,
            'function': function,
            'value': self.knob_value,
            'adjustment': adjustment,
            'timestamp': timestamp,
            'adjust_count': self.knob_adjust_count
        }

        self.client.publish(TOPIC_KNOB_ADJUST, json.dumps(payload))

        # Visual knob indicator
        bar_length = 20
        filled = int((self.knob_value / 100) * bar_length)
        bar = '█' * filled + '░' * (bar_length - filled)

        print(f"{Colors.BLUE}[{datetime.now().strftime('%H:%M:%S')}]{Colors.RESET} Knob Adjusted:")
        print(f"  🎛️  Knob: {Colors.BOLD}{self.device_id}{Colors.RESET}")
        print(f"  ⚙️  Function: {Colors.CYAN}{function}{Colors.RESET}")
        print(f"  📈 Value: {Colors.BOLD}{self.knob_value}%{Colors.RESET} [{bar}]")
        print(f"  🔄 Adjustment: {'+' if adjustment > 0 else ''}{adjustment}")
        print(f"{Colors.YELLOW}{'─' * 50}{Colors.RESET}\n")

    def show_menu(self):
        """Display interactive menu"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}╔════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}║         INTERACTIVE CONTROL MENU          ║{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}╚════════════════════════════════════════════╝{Colors.RESET}\n")
        print(f"{Colors.BOLD}Button Controls:{Colors.RESET}")
        print(f"  {Colors.GREEN}1{Colors.RESET} - Press button to TOGGLE spot occupancy")
        print(f"  {Colors.GREEN}2{Colors.RESET} - Press button to MARK spot as OCCUPIED")
        print(f"  {Colors.GREEN}3{Colors.RESET} - Press button to MARK spot as AVAILABLE")
        print(f"  {Colors.GREEN}4{Colors.RESET} - Emergency OVERRIDE button\n")

        print(f"{Colors.BOLD}Knob Controls:{Colors.RESET}")
        print(f"  {Colors.BLUE}+{Colors.RESET} - Rotate knob CLOCKWISE (+10)")
        print(f"  {Colors.BLUE}-{Colors.RESET} - Rotate knob COUNTER-CLOCKWISE (-10)")
        print(f"  {Colors.BLUE}r{Colors.RESET} - RESET knob to center (50%)")
        print(f"  {Colors.BLUE}m{Colors.RESET} - Adjust MAXIMUM parking time\n")

        print(f"{Colors.BOLD}System:{Colors.RESET}")
        print(f"  {Colors.YELLOW}s{Colors.RESET} - Show current STATUS")
        print(f"  {Colors.YELLOW}h{Colors.RESET} - Show this HELP menu")
        print(f"  {Colors.RED}q{Colors.RESET} - QUIT emulator\n")
        print(f"{Colors.YELLOW}{'─' * 50}{Colors.RESET}\n")

    def show_status(self):
        """Display current status"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}╔════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}║            DEVICE STATUS                  ║{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}╚════════════════════════════════════════════╝{Colors.RESET}\n")
        print(f"  Device ID: {Colors.BOLD}{self.device_id}{Colors.RESET}")
        print(f"  Button Presses: {Colors.GREEN}{self.button_press_count}{Colors.RESET}")
        print(f"  Knob Adjustments: {Colors.BLUE}{self.knob_adjust_count}{Colors.RESET}")
        print(f"  Current Knob Value: {Colors.BOLD}{self.knob_value}%{Colors.RESET}")
        print(f"{Colors.YELLOW}{'─' * 50}{Colors.RESET}\n")

    def run_interactive(self):
        """Run interactive mode"""
        self.show_menu()

        while self.running:
            try:
                print(f"{Colors.CYAN}Enter command:{Colors.RESET} ", end='', flush=True)
                choice = input().strip().lower()

                if choice == '1':
                    spot_id = input(f"{Colors.GREEN}Enter Spot ID (e.g., SPOT001): {Colors.RESET}").strip()
                    if spot_id:
                        self.press_button(spot_id, action="toggle")
                    else:
                        print(f"{Colors.RED}Invalid spot ID!{Colors.RESET}\n")

                elif choice == '2':
                    spot_id = input(f"{Colors.GREEN}Enter Spot ID (e.g., SPOT001): {Colors.RESET}").strip()
                    if spot_id:
                        self.press_button(spot_id, action="occupy")
                    else:
                        print(f"{Colors.RED}Invalid spot ID!{Colors.RESET}\n")

                elif choice == '3':
                    spot_id = input(f"{Colors.GREEN}Enter Spot ID (e.g., SPOT001): {Colors.RESET}").strip()
                    if spot_id:
                        self.press_button(spot_id, action="free")
                    else:
                        print(f"{Colors.RED}Invalid spot ID!{Colors.RESET}\n")

                elif choice == '4':
                    spot_id = input(f"{Colors.RED}Enter Spot ID for EMERGENCY OVERRIDE: {Colors.RESET}").strip()
                    if spot_id:
                        self.press_button(spot_id, action="emergency_override")
                    else:
                        print(f"{Colors.RED}Invalid spot ID!{Colors.RESET}\n")

                elif choice == '+':
                    self.adjust_knob(10, function="parking_time")

                elif choice == '-':
                    self.adjust_knob(-10, function="parking_time")

                elif choice == 'r':
                    old_value = self.knob_value
                    self.knob_value = 50
                    self.adjust_knob(0, function="reset")
                    print(f"{Colors.BLUE}Knob reset from {old_value}% to 50%{Colors.RESET}\n")

                elif choice == 'm':
                    self.adjust_knob(0, function="max_parking_time")

                elif choice == 's':
                    self.show_status()

                elif choice == 'h':
                    self.show_menu()

                elif choice == 'q':
                    print(f"{Colors.YELLOW}Exiting...{Colors.RESET}\n")
                    self.running = False
                    break

                else:
                    print(f"{Colors.RED}Invalid command! Press 'h' for help.{Colors.RESET}\n")

            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}Ctrl+C detected. Exiting...{Colors.RESET}\n")
                self.running = False
                break
            except Exception as e:
                print(f"{Colors.RED}Error: {e}{Colors.RESET}\n")

    def cleanup(self):
        """Cleanup and disconnect"""
        self.client.loop_stop()
        self.client.disconnect()

if __name__ == "__main__":
    print(f"\n{Colors.BOLD}Starting Button/Knob Actuator Emulator...{Colors.RESET}\n")

    emulator = ButtonKnobEmulator("BTN001")

    if emulator.connect():
        time.sleep(1)  # Wait for connection to establish

        try:
            emulator.run_interactive()
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Interrupted by user{Colors.RESET}")
        finally:
            emulator.show_status()
            emulator.cleanup()
            print(f"{Colors.GREEN}Button/Knob emulator stopped. Goodbye!{Colors.RESET}\n")
    else:
        print(f"{Colors.RED}Failed to connect to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}{Colors.RESET}")
        print(f"{Colors.YELLOW}Make sure Mosquitto is running!{Colors.RESET}\n")
