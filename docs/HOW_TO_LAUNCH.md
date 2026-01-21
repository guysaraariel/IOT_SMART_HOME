# 🚀 HOW TO LAUNCH PARKMATE - COMPLETE GUIDE

## ✨ **EASIEST WAY** - One-Click Launch (RECOMMENDED)

### Windows:
```batch
Double-click: LAUNCH_ALL.bat
```

### Linux/Mac:
```bash
./LAUNCH_ALL.sh
```

**That's it!** The script will automatically:
- Check if MongoDB and Mosquitto are running
- Start all 5 system components
- Open your web browser to the application

---

## 📋 What You'll See

After launching, **5 separate windows** will open:

| Window Color | Component | Description |
|-------------|-----------|-------------|
| 🟡 **Yellow** | Backend Server | Flask + MQTT Data Manager |
| 🔵 **Cyan** | Ultrasonic Sensors | 20 parking spot sensors |
| 🟣 **Purple** | LED/Relay Actuators | Visual LED indicators |
| 🔴 **Red** | Button/Knob Controls | Interactive manual controls |
| 🔷 **Blue** | DHT Sensor | Temperature & humidity monitor |

**DO NOT CLOSE THESE WINDOWS** while using the system!

---

## 🌐 Access the Application

Once all components are running:

- **Driver Interface**: http://localhost:5000/
- **Owner Dashboard**: http://localhost:5000/owner

The browser should open automatically. If not, manually navigate to the URLs above.

---

## ⚙️ Prerequisites (MUST be running BEFORE launching)

### 1. MongoDB
**Check if running:**
```bash
# Windows
tasklist | findstr mongod

# Linux/Mac
ps aux | grep mongod
```

**Start MongoDB:**
```bash
# Windows
mongod

# Linux/Mac
sudo systemctl start mongod
# OR
mongod
```

### 2. Mosquitto MQTT Broker
**Check if running:**
```bash
# Windows
tasklist | findstr mosquitto

# Linux/Mac
ps aux | grep mosquitto
```

**Start Mosquitto:**
```bash
# Windows
mosquitto

# Linux/Mac
sudo systemctl start mosquitto
# OR
mosquitto
```

### 3. Python 3.8+
**Check version:**
```bash
python --version
# OR
python3 --version
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

---

## 🔧 Manual Launch (Alternative Method)

If you prefer to start components individually:

### Terminal 1 - Backend Server
```bash
python app.py
```
**Wait for:** `Starting ParkMate Backend Server...`

### Terminal 2 - Initialize Database (FIRST TIME ONLY)
```bash
curl -X POST http://localhost:5000/api/init
```
**Or visit:** http://localhost:5000/api/init in your browser

### Terminal 3 - Ultrasonic Sensor Emulator
```bash
python emulators/sensor_emulator.py
```
**Wait for:** `20 sensors connected successfully!`

### Terminal 4 - LED/Relay Actuator
```bash
python emulators/led_actuator.py
```
**Wait for:** `LED/RELAY ACTUATOR EMULATOR STARTED`

### Terminal 5 - Button/Knob Control
```bash
python emulators/button_emulator.py
```
**Wait for:** `BUTTON/KNOB ACTUATOR EMULATOR STARTED`

### Terminal 6 - DHT Environmental Sensor
```bash
python emulators/dht_sensor_emulator.py
```
**Wait for:** `DHT SENSOR EMULATOR STARTED`

---

## 🎮 Using the System

### Driver Interface (`http://localhost:5000/`)
1. Select "Central Parking Tower" from dropdown
2. View real-time parking availability
3. Green spots = Available
4. Red spots = Occupied
5. Watch spots change in real-time!

### Owner Dashboard (`http://localhost:5000/owner`)
1. Select parking lot
2. View statistics, occupancy rate, revenue
3. Monitor environmental conditions (temperature, humidity)
4. See real-time alerts
5. Manually override spot status with buttons
6. View occupancy trend chart

### Button Emulator (Interactive Terminal)
In the RED window, you can:
- Press `1` - Toggle spot occupancy (enter spot ID like SPOT001)
- Press `2` - Mark spot as occupied
- Press `3` - Mark spot as available
- Press `+` - Adjust knob clockwise
- Press `-` - Adjust knob counter-clockwise
- Press `s` - Show status
- Press `q` - Quit

Watch the changes appear INSTANTLY in the web interface!

---

## 🛑 How to Stop the System

### Option 1: Close All Windows
Simply close each of the 5 colored terminal windows.

### Option 2: Ctrl+C
Press `Ctrl+C` in each window to gracefully shut down.

### Option 3: Kill All (Emergency)
```bash
# Windows
taskkill /F /IM python.exe

# Linux/Mac
pkill -f "python.*parkmate"
```

---

## ✅ Verification Checklist

Before launching, make sure:

- [ ] MongoDB is running on port 27017
- [ ] Mosquitto is running on port 1883
- [ ] Python 3.8+ is installed
- [ ] All dependencies are installed (`pip install -r requirements.txt`)
- [ ] You're in the `ParkMateApp` directory

---

## 📊 System Architecture (5 Components)

```
┌─────────────────────────────────────────────────────────────┐
│                    PARKMATE SYSTEM                          │
└─────────────────────────────────────────────────────────────┘

Component 1: ULTRASONIC SENSOR EMULATOR (Data Producer)
├── Simulates 20 parking spot sensors
├── Measures distance (occupied < 100cm, available ~200cm)
└── Publishes to MQTT: parkmate/spot/status

Component 2: DHT SENSOR EMULATOR (Data Producer)
├── Simulates temperature & humidity sensor
├── Monitors environmental conditions
└── Publishes to MQTT: parkmate/environment

Component 3: LED/RELAY ACTUATOR (Actuator - Receiver)
├── Receives LED commands from backend
├── Displays visual feedback (Red/Green)
└── Subscribes to MQTT: parkmate/led/command

Component 4: BUTTON/KNOB EMULATOR (Actuator - Sender)
├── Interactive manual controls
├── Toggle spot occupancy, adjust settings
└── Publishes to MQTT: parkmate/button/press

Component 5: BACKEND SERVER (Data Manager)
├── Flask REST API + WebSocket server
├── MQTT message broker client
├── MongoDB database manager
├── Processes all data and sends commands
└── Serves web interface on port 5000

         MQTT Broker (Mosquitto)
                  ↕
         MongoDB Database
```

---

## 🆘 Troubleshooting

### Problem: "MongoDB connection error"
**Solution:** Start MongoDB first
```bash
mongod
```

### Problem: "MQTT broker connection error"
**Solution:** Start Mosquitto first
```bash
mosquitto
```

### Problem: "Port 5000 already in use"
**Solution:** Kill the process using port 5000
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :5000
kill -9 <PID>
```

### Problem: "Module not found"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Problem: Web page shows "Disconnected"
**Solution:**
1. Make sure Backend Server (yellow window) is running
2. Refresh the web page
3. Check browser console for errors (F12)

---

## 📞 Support

If you encounter any issues:
1. Check that MongoDB and Mosquitto are running
2. Verify all dependencies are installed
3. Check the terminal windows for error messages
4. Review the [ARCHITECTURE.md](ARCHITECTURE.md) for system details

---

## 🎓 Course Information

**Project:** ParkMate - IoT Software Development Project
**Team:**
- Sara Banay | ID: 212254973
- Ariel Bazarsky Jarosch | ID: 211778774
- Guy Cohen | ID: 211883277

**Course:** Software Development for IoT Systems

---

**Enjoy using ParkMate! 🚗🅿️**
