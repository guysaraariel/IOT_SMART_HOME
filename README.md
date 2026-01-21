# ParkMate - Smart IoT Parking Management System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-6.0+-green.svg)](https://www.mongodb.com/)
[![MQTT](https://img.shields.io/badge/MQTT-Mosquitto-orange.svg)](https://mosquitto.org/)
[![License](https://img.shields.io/badge/License-Educational-yellow.svg)](#-license)

A complete IoT-based smart parking management system that uses simulated ultrasonic sensors to detect vehicle presence and provides real-time parking availability through an intuitive web interface.

## 🎬 Video Demos

[![Presentation](https://img.shields.io/badge/YouTube-Presentation-red?logo=youtube)](https://www.youtube.com/watch?v=RPjkaBiDV4Q)
[![Code Execution](https://img.shields.io/badge/YouTube-Code_Execution-red?logo=youtube)](https://www.youtube.com/watch?v=OpaqvlPZbOo)

- [IoT Course | ParkMate | Presentation Recording](https://www.youtube.com/watch?v=RPjkaBiDV4Q)
- [IoT Course | ParkMate | Code Execution Recording](https://www.youtube.com/watch?v=OpaqvlPZbOo)

## 🎯 Features

- **Real-time Monitoring** - Live parking spot status updates via WebSocket
- **IoT Sensor Emulation** - 4 types of IoT device emulators (ultrasonic, DHT, LED, buttons)
- **Dual Interface** - Separate views for drivers and facility owners
- **MQTT Communication** - Industry-standard IoT messaging protocol
- **MongoDB Persistence** - Scalable NoSQL database for historical data
- **Manual Override** - Owner controls for spot management
- **Environmental Monitoring** - Temperature and humidity tracking
- **Visual Feedback** - Color-coded LED indicators (Red/Green)

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- MongoDB (running on `localhost:27017`)
- Mosquitto MQTT Broker (running on `localhost:1883`)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ParkMateApp.git
   cd ParkMateApp
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start MongoDB and Mosquitto**
   ```bash
   # Start MongoDB
   mongod

   # Start Mosquitto (in another terminal)
   mosquitto
   ```

4. **Launch the system**

   **Windows:**
   ```bash
   LAUNCH_ALL.bat
   ```

   **Linux/Mac:**
   ```bash
   chmod +x LAUNCH_ALL.sh
   ./LAUNCH_ALL.sh
   ```

5. **Access the application**
   - Driver Interface: http://localhost:5000/
   - Owner Dashboard: http://localhost:5000/owner

## 📁 Project Structure

```
ParkMateApp/
├── app.py                  # Flask backend server
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── LAUNCH_ALL.bat         # Windows launcher
├── LAUNCH_ALL.sh          # Linux/Mac launcher
├── emulators/             # IoT device emulators
│   ├── sensor_emulator.py      # Ultrasonic sensors
│   ├── dht_sensor_emulator.py  # Temperature/humidity
│   ├── led_actuator.py         # LED/Relay actuator
│   └── button_emulator.py      # Button/Knob controls
├── static/                # Frontend web interfaces
│   ├── index.html              # Driver interface
│   └── owner.html              # Owner dashboard
└── docs/                  # Documentation
    ├── HOW_TO_LAUNCH.md        # Complete launch guide
    ├── QUICK_START.txt         # Quick reference
    ├── EMULATORS_GUIDE.md      # Emulator documentation
    ├── ARCHITECTURE.md         # System architecture
    ├── TESTING.md              # Testing procedures
    ├── FEATURE_GUIDE.md        # Feature documentation
    └── FILE_STRUCTURE.txt      # File structure reference
```

## 🏗️ System Architecture

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   IoT Layer  │ ───> │ Backend Layer│ ───> │   UI Layer   │
│  (Sensors)   │ MQTT │  (Processing)│  WS  │   (Clients)  │
└──────────────┘      └──────────────┘      └──────────────┘
                             │
                             ├─── MongoDB
                             └─── MQTT Broker
```

### Components

1. **IoT Emulators** (4 types)
   - Ultrasonic sensors - Detect vehicle presence
   - DHT sensor - Monitor temperature/humidity
   - LED/Relay actuator - Visual feedback
   - Button/Knob - Manual controls

2. **Backend** (Flask)
   - REST API for data access
   - MQTT client for sensor communication
   - WebSocket for real-time updates
   - MongoDB integration

3. **Frontend** (HTML/JS)
   - Driver interface - View available spots
   - Owner dashboard - Manage facility

## 🔧 Usage

### Launching Components

The `LAUNCH_ALL` script automatically starts all 5 system components:

| Component | Description | Window Color |
|-----------|-------------|--------------|
| Backend Server | Flask + MQTT + MongoDB | 🟡 Yellow |
| Ultrasonic Sensors | 20 parking spot detectors | 🔵 Cyan |
| LED/Relay Actuators | Visual indicators | 🟣 Purple |
| Button/Knob Controls | Manual control interface | 🔴 Red |
| DHT Sensor | Temperature & humidity | 🔷 Blue |

### Manual Controls (Button Emulator)

**Button Controls:**
- `1` - Toggle spot occupancy (enter SPOT001, SPOT002, etc.)
- `2` - Mark spot as OCCUPIED
- `3` - Mark spot as AVAILABLE
- `4` - Emergency OVERRIDE button

**Knob Controls:**
- `+` - Rotate knob clockwise (+10)
- `-` - Rotate knob counter-clockwise (-10)
- `r` - Reset knob to center (50%)
- `m` - Adjust maximum parking time

**System:**
- `s` - Show current status
- `h` - Show help menu
- `q` - Quit emulator

## 📡 MQTT Topics

| Topic | Direction | Description |
|-------|-----------|-------------|
| `parkmate/spot/status` | Sensors → Backend | Parking spot status updates |
| `parkmate/led/command` | Backend → Actuators | LED control commands |
| `parkmate/button/press` | Button → Backend | Button press events |
| `parkmate/knob/adjust` | Knob → Backend | Knob rotation events |
| `parkmate/environment` | DHT → Backend | Temperature/humidity data |
| `parkmate/alerts` | DHT → Backend | Environmental alerts |

## 🗄️ Database Schema

**Collections:**
- `parking_lots` - Parking facility information
- `parking_spots` - Individual spot status
- `parking_history` - Historical event log
- `environment_data` - Temperature/humidity records
- `button_events` - Manual control events
- `alerts` - Environmental and system alerts

## 🧪 Testing

Run the test procedures from [docs/TESTING.md](docs/TESTING.md):

```bash
# Example: Test database initialization
curl -X POST http://localhost:5000/api/init

# Monitor MQTT messages
mosquitto_sub -t 'parkmate/#' -v
```

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/lots` | GET | List all parking lots |
| `/api/lots/<lot_id>` | GET | Get specific lot details |
| `/api/spots?lot_id=<id>` | GET | Get parking spots |
| `/api/spots/<spot_id>` | GET | Get specific spot details |
| `/api/stats/<lot_id>` | GET | Get statistics |
| `/api/environment/<lot_id>` | GET | Get environmental data |
| `/api/alerts/<lot_id>` | GET | Get recent alerts |
| `/api/button_events` | GET | Get recent button events |
| `/api/lots/<lot_id>/override` | POST | Manual spot override |
| `/api/init` | POST | Initialize sample data |

## 📚 Documentation

- [Quick Start Guide](docs/QUICK_START.txt) - One-page reference
- [How to Launch](docs/HOW_TO_LAUNCH.md) - Complete launch instructions
- [Emulators Guide](docs/EMULATORS_GUIDE.md) - Detailed emulator docs
- [Architecture](docs/ARCHITECTURE.md) - System design
- [Testing Guide](docs/TESTING.md) - Test procedures

## 🛠️ Technology Stack

- **Backend:** Python, Flask, Flask-SocketIO, Flask-CORS
- **Database:** MongoDB, PyMongo
- **IoT:** MQTT (Mosquitto), Paho-MQTT
- **Frontend:** HTML5, CSS3, Vanilla JavaScript, Socket.IO
- **Real-time:** WebSocket

## 👥 Team

- Sara Banay - 212254973
- Ariel Bazarsky Jarosch - 211778774
- Guy Cohen - 211883277

**Course:** Software Development for IoT Systems

## 🔮 Future Enhancements

- License Plate Recognition (LPR)
- Digital payment integration
- Smart city API integration
- Predictive AI for occupancy forecasting

## 📄 License

This is an educational project for IoT Software Development.

## 🆘 Support

For issues and questions, see [docs/HOW_TO_LAUNCH.md](docs/HOW_TO_LAUNCH.md) or contact the team.

---

**Made with ❤️ for IoT Software Development**
