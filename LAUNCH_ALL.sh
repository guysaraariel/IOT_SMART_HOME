#!/bin/bash

# ====================================================================
#  ParkMate IoT System - COMPLETE LAUNCHER (Linux/Mac)
#  Starts ALL components of the ParkMate system
# ====================================================================

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

clear

echo -e "${GREEN}${BOLD}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║        PARKMATE IOT PARKING MANAGEMENT SYSTEM                  ║"
echo "║              Complete System Launcher                          ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo "This script will launch ALL components of the ParkMate system:"
echo ""
echo "  1. Flask Backend Server (Data Manager)"
echo "  2. Ultrasonic Sensor Emulator (Data Producer)"
echo "  3. LED/Relay Actuator Emulator (Actuator - Receives Commands)"
echo "  4. Button/Knob Emulator (Actuator - Sends Commands)"
echo "  5. DHT Sensor Emulator (Environmental Data Producer)"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""

# Check MongoDB
echo -e "${CYAN}[1/3] Checking MongoDB status...${NC}"
if pgrep -x "mongod" > /dev/null; then
    echo -e "${GREEN}✓ MongoDB is running${NC}"
else
    echo -e "${RED}✗ WARNING: MongoDB is NOT running!${NC}"
    echo -e "${YELLOW}  Please start MongoDB first:${NC}"
    echo "    sudo systemctl start mongod"
    echo "    OR: mongod"
    echo ""
    read -p "Press Enter to continue anyway or Ctrl+C to exit..."
fi

# Check Mosquitto
echo -e "${CYAN}[2/3] Checking Mosquitto MQTT Broker status...${NC}"
if pgrep -x "mosquitto" > /dev/null; then
    echo -e "${GREEN}✓ Mosquitto MQTT Broker is running${NC}"
else
    echo -e "${RED}✗ WARNING: Mosquitto is NOT running!${NC}"
    echo -e "${YELLOW}  Please start Mosquitto first:${NC}"
    echo "    sudo systemctl start mosquitto"
    echo "    OR: mosquitto"
    echo ""
    read -p "Press Enter to continue anyway or Ctrl+C to exit..."
fi

# Check Python
echo -e "${CYAN}[3/3] Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✓ Python is installed: $(python3 --version)${NC}"
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    echo -e "${GREEN}✓ Python is installed: $(python --version)${NC}"
    PYTHON_CMD=python
else
    echo -e "${RED}✗ ERROR: Python is not installed${NC}"
    echo "  Please install Python 3.8+ from python.org"
    exit 1
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "Starting all components in separate terminal windows..."
echo ""
echo "NOTE: Each component will open in its own terminal window"
echo "      Do NOT close these windows while the system is running!"
echo ""

sleep 2

# Detect terminal emulator
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    TERMINAL_CMD="open -a Terminal"
elif command -v gnome-terminal &> /dev/null; then
    # GNOME
    TERMINAL_CMD="gnome-terminal --"
elif command -v xterm &> /dev/null; then
    # XTerm
    TERMINAL_CMD="xterm -e"
else
    echo -e "${YELLOW}Warning: Could not detect terminal emulator${NC}"
    echo "Starting processes in background instead..."
    TERMINAL_CMD=""
fi

# 1. Start Flask Backend
echo -e "${CYAN}[1/5] Starting Flask Backend Server...${NC}"
if [[ "$OSTYPE" == "darwin"* ]]; then
    osascript -e 'tell app "Terminal" to do script "cd \"'$(pwd)'\" && python3 app.py"'
elif [ -n "$TERMINAL_CMD" ]; then
    $TERMINAL_CMD bash -c "cd $(pwd) && $PYTHON_CMD app.py; exec bash" &
else
    $PYTHON_CMD app.py &
fi
sleep 3

# 2. Start Sensor Emulator
echo -e "${CYAN}[2/5] Starting Ultrasonic Sensor Emulator...${NC}"
if [[ "$OSTYPE" == "darwin"* ]]; then
    osascript -e 'tell app "Terminal" to do script "cd \"'$(pwd)'\" && python3 emulators/sensor_emulator.py"'
elif [ -n "$TERMINAL_CMD" ]; then
    $TERMINAL_CMD bash -c "cd $(pwd) && $PYTHON_CMD emulators/sensor_emulator.py; exec bash" &
else
    $PYTHON_CMD emulators/sensor_emulator.py &
fi
sleep 2

# 3. Start LED Actuator
echo -e "${CYAN}[3/5] Starting LED/Relay Actuator Emulator...${NC}"
if [[ "$OSTYPE" == "darwin"* ]]; then
    osascript -e 'tell app "Terminal" to do script "cd \"'$(pwd)'\" && python3 emulators/led_actuator.py"'
elif [ -n "$TERMINAL_CMD" ]; then
    $TERMINAL_CMD bash -c "cd $(pwd) && $PYTHON_CMD emulators/led_actuator.py; exec bash" &
else
    $PYTHON_CMD emulators/led_actuator.py &
fi
sleep 2

# 4. Start Button Emulator
echo -e "${CYAN}[4/5] Starting Button/Knob Actuator Emulator...${NC}"
if [[ "$OSTYPE" == "darwin"* ]]; then
    osascript -e 'tell app "Terminal" to do script "cd \"'$(pwd)'\" && python3 emulators/button_emulator.py"'
elif [ -n "$TERMINAL_CMD" ]; then
    $TERMINAL_CMD bash -c "cd $(pwd) && $PYTHON_CMD emulators/button_emulator.py; exec bash" &
else
    $PYTHON_CMD emulators/button_emulator.py &
fi
sleep 2

# 5. Start DHT Sensor
echo -e "${CYAN}[5/5] Starting DHT Environmental Sensor Emulator...${NC}"
if [[ "$OSTYPE" == "darwin"* ]]; then
    osascript -e 'tell app "Terminal" to do script "cd \"'$(pwd)'\" && python3 emulators/dht_sensor_emulator.py"'
elif [ -n "$TERMINAL_CMD" ]; then
    $TERMINAL_CMD bash -c "cd $(pwd) && $PYTHON_CMD emulators/dht_sensor_emulator.py; exec bash" &
else
    $PYTHON_CMD emulators/dht_sensor_emulator.py &
fi
sleep 2

echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""
echo -e "${GREEN}${BOLD}✓ ALL COMPONENTS STARTED SUCCESSFULLY!${NC}"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "  ACCESS THE APPLICATION:"
echo ""
echo -e "    Driver Interface:    ${CYAN}http://localhost:5000/${NC}"
echo -e "    Owner Dashboard:     ${CYAN}http://localhost:5000/owner${NC}"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "  RUNNING COMPONENTS (5 separate windows/processes):"
echo ""
echo "    1. Backend Server       - Flask + MQTT Data Manager"
echo "    2. Ultrasonic Sensors   - Parking spot detectors"
echo "    3. LED/Relay Actuators  - Visual indicators"
echo "    4. Button/Knob Controls - Interactive controls"
echo "    5. DHT Sensor          - Environmental monitoring"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "  TO STOP THE SYSTEM:"
echo "    - Close each terminal window individually, OR"
echo "    - Press Ctrl+C in each window"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""

# Try to open browser
echo "Opening web browser..."
sleep 3

if [[ "$OSTYPE" == "darwin"* ]]; then
    open http://localhost:5000/
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:5000/ &
elif command -v firefox &> /dev/null; then
    firefox http://localhost:5000/ &
elif command -v chromium-browser &> /dev/null; then
    chromium-browser http://localhost:5000/ &
else
    echo -e "${YELLOW}Could not open browser automatically${NC}"
    echo "Please open http://localhost:5000/ manually"
fi

echo ""
echo -e "${GREEN}System is now running!${NC}"
echo ""
