# 🔧 ParkMate IoT Emulators - Complete Guide

## Overview

ParkMate includes **4 types of IoT emulators** that simulate real hardware devices:

| # | Emulator | Type | Function | File |
|---|----------|------|----------|------|
| 1 | **Ultrasonic Sensor** | Data Producer | Detects parking spot occupancy | [sensor_emulator.py](../emulators/sensor_emulator.py) |
| 2 | **DHT Sensor** | Data Producer | Monitors temperature & humidity | [dht_sensor_emulator.py](../emulators/dht_sensor_emulator.py) |
| 3 | **LED/Relay Actuator** | Actuator (Receiver) | Displays visual feedback | [led_actuator.py](../emulators/led_actuator.py) |
| 4 | **Button/Knob** | Actuator (Sender) | Manual control interface | [button_emulator.py](../emulators/button_emulator.py) |

---

## 1️⃣ Ultrasonic Sensor Emulator

### Purpose
Simulates HC-SR04 ultrasonic distance sensors that detect vehicle presence in parking spots.

### How It Works
- **Distance Measurement**:
  - Occupied: 10-50 cm (car detected)
  - Available: 180-220 cm (empty spot, measuring to floor)
- **Threshold**: < 100 cm = Occupied
- **Random Events**: Simulates cars parking and leaving (10% chance per cycle)

### MQTT Communication
**Publishes to:** `parkmate/spot/status`
```json
{
  "spot_id": "SPOT001",
  "lot_id": "LOT001",
  "occupied": true,
  "distance": 35,
  "timestamp": "2024-01-10T12:00:00"
}
```

**Subscribes to:** `parkmate/led/command` (receives LED feedback)

### Launch
```bash
python emulators/sensor_emulator.py

# With custom parameters:
python emulators/sensor_emulator.py --spots 30 --lot LOT001 --interval 3
```

### Parameters
- `--spots`: Number of parking spots (default: 20)
- `--lot`: Parking lot ID (default: LOT001)
- `--interval`: Update interval in seconds (default: 5)

### Visual Output
```
Sensor SPOT001: OCCUPIED (distance: 35cm)
Sensor SPOT002: AVAILABLE (distance: 195cm)
```

---

## 2️⃣ DHT Environmental Sensor Emulator

### Purpose
Simulates DHT11/DHT22 temperature and humidity sensors for environmental monitoring.

### How It Works
- **Temperature**: Random walk between 0-40°C (realistic fluctuations)
- **Humidity**: Random walk between 20-90% (realistic fluctuations)
- **Heat Index**: Calculated "feels like" temperature
- **Alerts**: Automatic warnings for extreme conditions

### Alert Thresholds
| Condition | Threshold | Severity |
|-----------|-----------|----------|
| High Temperature | ≥ 35°C | WARNING |
| Low Temperature | ≤ 0°C | WARNING |
| High Humidity | ≥ 80% | INFO |
| Low Humidity | ≤ 20% | INFO |
| High Heat Index | ≥ 32°C | WARNING |

### MQTT Communication
**Publishes to:** `parkmate/environment`
```json
{
  "sensor_id": "DHT001",
  "lot_id": "LOT001",
  "temperature": 24.5,
  "humidity": 55.0,
  "heat_index": 25.2,
  "unit_temp": "celsius",
  "unit_humidity": "percent",
  "timestamp": "2024-01-10T12:00:00"
}
```

**Publishes alerts to:** `parkmate/alerts`
```json
{
  "sensor_id": "DHT001",
  "lot_id": "LOT001",
  "alert": {
    "type": "HIGH_TEMPERATURE",
    "severity": "WARNING",
    "message": "High temperature detected: 36.5°C",
    "recommendation": "Ensure parking lot ventilation is adequate"
  },
  "timestamp": "2024-01-10T12:00:00"
}
```

### Launch
```bash
python emulators/dht_sensor_emulator.py

# With custom parameters:
python emulators/dht_sensor_emulator.py --sensor DHT002 --lot LOT001 --interval 10
```

### Parameters
- `--sensor`: Sensor ID (default: DHT001)
- `--lot`: Parking lot ID (default: LOT001)
- `--interval`: Reading interval in seconds (default: 10)

### Visual Output
```
[12:00:00] Environmental Reading:
  🌡️  Temperature: 24.5°C
  💧 Humidity: 55.0%
  🌡️  Heat Index: 25.2°C (feels like)
  📍 Location: LOT001 | Sensor: DHT001
```

---

## 3️⃣ LED/Relay Actuator Emulator

### Purpose
Simulates LED indicators and relay switches that provide visual feedback for parking spot status.

### How It Works
- **Receives Commands**: Listens for LED control messages from backend
- **Visual Display**: Shows colored terminal output representing LED state
- **Relay Control**: Simulates electrical relay on/off states

### MQTT Communication
**Subscribes to:** `parkmate/led/command`
```json
{
  "spot_id": "SPOT001",
  "lot_id": "LOT001",
  "color": "red"
}
```

**Subscribes to:** `parkmate/relay/command`
```json
{
  "relay_id": "RELAY001",
  "state": "on",
  "action": "gate_open"
}
```

### Launch
```bash
python emulators/led_actuator.py
```

### Visual Output
```
[12:00:00] LED Command Received:
  💡 Spot: SPOT001 | Lot: LOT001
  ● Color: RED → Status: OCCUPIED

[12:00:05] Relay Command Received:
  🔌 Relay: RELAY001
  ⚡ State: ON | Action: gate_open
```

### Color Meanings
- 🔴 **RED**: Spot occupied
- 🟢 **GREEN**: Spot available
- 🟡 **YELLOW**: Spot reserved

---

## 4️⃣ Button/Knob Actuator Emulator

### Purpose
Simulates physical buttons and rotary knobs for manual control and testing.

### How It Works
- **Interactive Terminal**: Menu-driven interface
- **Button Presses**: Trigger spot status changes
- **Knob Adjustments**: Control system parameters (0-100%)
- **Real-time Feedback**: Changes appear instantly in web interface

### MQTT Communication
**Publishes to:** `parkmate/button/press`
```json
{
  "button_id": "BTN001",
  "spot_id": "SPOT005",
  "action": "toggle",
  "pressed": true,
  "timestamp": "2024-01-10T12:00:00",
  "press_count": 15
}
```

**Publishes to:** `parkmate/knob/adjust`
```json
{
  "knob_id": "BTN001",
  "function": "parking_time",
  "value": 75,
  "adjustment": 10,
  "timestamp": "2024-01-10T12:00:00",
  "adjust_count": 8
}
```

### Launch
```bash
python emulators/button_emulator.py
```

### Interactive Menu
```
╔════════════════════════════════════════════╗
║         INTERACTIVE CONTROL MENU          ║
╚════════════════════════════════════════════╝

Button Controls:
  1 - Press button to TOGGLE spot occupancy
  2 - Press button to MARK spot as OCCUPIED
  3 - Press button to MARK spot as AVAILABLE
  4 - Emergency OVERRIDE button

Knob Controls:
  + - Rotate knob CLOCKWISE (+10)
  - - Rotate knob COUNTER-CLOCKWISE (-10)
  r - RESET knob to center (50%)
  m - Adjust MAXIMUM parking time

System:
  s - Show current STATUS
  h - Show this HELP menu
  q - QUIT emulator

Enter command:
```

### Button Actions
| Action | Effect |
|--------|--------|
| **toggle** | Flip spot between occupied/available |
| **occupy** | Force spot to occupied state |
| **free** | Force spot to available state |
| **emergency_override** | Immediate override with alert |

### Knob Functions
| Function | Range | Use Case |
|----------|-------|----------|
| **parking_time** | 0-100% | Adjust parking duration limit |
| **max_parking_time** | 0-100% | Set maximum allowed time |
| **brightness** | 0-100% | LED brightness control |

### Visual Output
```
[12:00:00] Button Pressed:
  🔘 Button: BTN001
  🅿️  Spot: SPOT005
  ⚡ Action: toggle
  📊 Press Count: 15

[12:00:05] Knob Adjusted:
  🎛️  Knob: BTN001
  ⚙️  Function: parking_time
  📈 Value: 75% [███████████████░░░░░]
  🔄 Adjustment: +10
```

---

## 🔄 Data Flow Example

### Complete System Interaction

```
1. User parks car
         ↓
2. Ultrasonic Sensor detects (distance: 200cm → 35cm)
         ↓
3. Sensor publishes to MQTT: parkmate/spot/status
   {"spot_id": "SPOT001", "occupied": true}
         ↓
4. Backend receives MQTT message
         ↓
5. Backend updates MongoDB database
         ↓
6. Backend publishes LED command to MQTT: parkmate/led/command
   {"spot_id": "SPOT001", "color": "red"}
         ↓
7. LED Actuator receives command
         ↓
8. LED Actuator displays: "SPOT001: RED (OCCUPIED)"
         ↓
9. Backend broadcasts WebSocket event
         ↓
10. Web interface updates: Green spot → Red spot
         ↓
11. DHT Sensor publishes environment data
         ↓
12. Owner dashboard shows temperature alert if > 35°C
         ↓
13. Owner presses button to free spot manually
         ↓
14. Button emulator publishes to MQTT: parkmate/button/press
         ↓
15. Backend processes and updates database
         ↓
16. Backend sends LED command: "green"
         ↓
17. LED Actuator displays: "SPOT001: GREEN (AVAILABLE)"
         ↓
18. Web interface updates: Red spot → Green spot
```

---

## 🧪 Testing the Emulators

### Test 1: Sensor to GUI
1. Start all emulators
2. Open Driver Interface
3. Watch spots change automatically
4. **Expected**: Real-time updates in web interface

### Test 2: Button to LED
1. Start Button Emulator
2. Start LED Actuator
3. Press `1` in Button window
4. Enter spot ID (e.g., SPOT005)
5. **Expected**: LED window shows color change

### Test 3: Environment Monitoring
1. Start DHT Sensor
2. Open Owner Dashboard
3. **Expected**: Temperature/humidity display updates every 10 seconds

### Test 4: Alert System
1. Start DHT Sensor
2. Wait for extreme temperature (or modify thresholds)
3. **Expected**: Alert appears in Owner Dashboard

---

## 📝 Configuration

All emulators use the same MQTT broker settings defined in [config.py](../config.py):

```python
MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
```

To change broker location, edit `config.py` or modify each emulator file.

---

## 🐛 Troubleshooting

### Emulator won't start
**Problem:** `Connection error: [Errno 111] Connection refused`
**Solution:** Start Mosquitto MQTT broker first
```bash
mosquitto
```

### No data in web interface
**Problem:** Emulator running but no updates
**Solution:**
1. Check Backend Server is running
2. Verify MQTT topics match
3. Check console for error messages

### Button actions not working
**Problem:** Button press has no effect
**Solution:**
1. Ensure Backend Server is running
2. Verify spot ID exists in database
3. Initialize database: `curl -X POST http://localhost:5000/api/init`

---

## 🎓 Educational Value

These emulators demonstrate:
- **IoT Protocols**: MQTT pub/sub messaging
- **Sensor Simulation**: Realistic data generation
- **Actuator Control**: Command-response patterns
- **Real-time Systems**: Event-driven architecture
- **Data Flow**: End-to-end IoT pipeline

