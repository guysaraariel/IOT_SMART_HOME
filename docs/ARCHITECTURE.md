# ParkMate - System Architecture

## 📐 System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        ParkMate System                          │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   IoT Layer  │ ───> │ Backend Layer│ ───> │   UI Layer   │
│  (Sensors)   │ MQTT │  (Processing)│  WS  │   (Clients)  │
└──────────────┘      └──────────────┘      └──────────────┘
                             │
                             ├─── MongoDB
                             └─── MQTT Broker
```

## 🔷 Component Architecture

### 1. IoT Sensor Layer
```
┌─────────────────────────────────────────────┐
│        Parking Spot Sensor Emulator         │
│                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │ SPOT001  │  │ SPOT002  │  │ SPOT003  │ │
│  │  Sensor  │  │  Sensor  │  │  Sensor  │ │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘ │
│       │             │             │        │
│       └─────────────┴─────────────┘        │
│                     │                      │
│              Ultrasonic Distance           │
│              Measurement (simulated)       │
│                                             │
│       MQTT Publish: spot/status            │
│       MQTT Subscribe: led/command          │
└─────────────────────────────────────────────┘
```

### 2. MQTT Broker (Mosquitto)
```
┌─────────────────────────────────────────────┐
│            MQTT Message Broker              │
│                                             │
│  Topics:                                    │
│  • parkmate/spot/status    (sensors → )    │
│  • parkmate/led/command    ( → sensors)    │
│  • parkmate/payment        (app → )        │
│                                             │
│  Features:                                  │
│  • Pub/Sub messaging                        │
│  • QoS levels                               │
│  • Message persistence                      │
│  • Lightweight protocol                     │
└─────────────────────────────────────────────┘
```

### 3. Backend Processing Layer
```
┌─────────────────────────────────────────────┐
│          Flask Application (app.py)         │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │       MQTT Client Handler           │   │
│  │  • Subscribe to sensor updates      │   │
│  │  • Process spot status changes      │   │
│  │  • Send LED commands                │   │
│  └─────────────────────────────────────┘   │
│                     ↓                       │
│  ┌─────────────────────────────────────┐   │
│  │       Business Logic Layer          │   │
│  │  • Calculate availability           │   │
│  │  • Update lot statistics            │   │
│  │  • Log history                      │   │
│  │  • Handle manual overrides          │   │
│  └─────────────────────────────────────┘   │
│                     ↓                       │
│  ┌─────────────────────────────────────┐   │
│  │          REST API Layer             │   │
│  │  • GET  /api/lots                   │   │
│  │  • GET  /api/lots/:id               │   │
│  │  • GET  /api/spots                  │   │
│  │  • GET  /api/stats/:id              │   │
│  │  • POST /api/lots/:id/override      │   │
│  │  • POST /api/init                   │   │
│  └─────────────────────────────────────┘   │
│                     ↓                       │
│  ┌─────────────────────────────────────┐   │
│  │       WebSocket Layer               │   │
│  │  • Real-time spot updates           │   │
│  │  • Broadcast to all clients         │   │
│  │  • Connection management            │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

### 4. Database Layer (MongoDB)
```
┌─────────────────────────────────────────────┐
│          MongoDB (parkmate_db)              │
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │  Collection: parking_lots             │ │
│  │  • lot_id (indexed)                   │ │
│  │  • name, address                      │ │
│  │  • total_spots, occupied_spots        │ │
│  │  • available_spots                    │ │
│  │  • price_per_hour                     │ │
│  └───────────────────────────────────────┘ │
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │  Collection: parking_spots            │ │
│  │  • spot_id (indexed)                  │ │
│  │  • lot_id (indexed)                   │ │
│  │  • occupied, distance                 │ │
│  │  • manual_override                    │ │
│  │  • last_update                        │ │
│  └───────────────────────────────────────┘ │
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │  Collection: parking_history          │ │
│  │  • spot_id, lot_id                    │ │
│  │  • occupied                            │ │
│  │  • timestamp (indexed)                │ │
│  └───────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

### 5. Frontend Layer
```
┌─────────────────────────────────────────────┐
│          Driver Interface (index.html)      │
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │  • Real-time parking grid             │ │
│  │  • Live statistics display            │ │
│  │  • Lot selector                       │ │
│  │  • Color-coded spots                  │ │
│  │  • WebSocket connection               │ │
│  └───────────────────────────────────────┘ │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│          Owner Dashboard (owner.html)       │
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │  • Occupancy metrics                  │ │
│  │  • Revenue tracking                   │ │
│  │  • Spot management table              │ │
│  │  • Manual override controls           │ │
│  │  • Historical data visualization      │ │
│  └───────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

## 🔄 Data Flow Diagrams

### Real-time Spot Update Flow
```
1. Vehicle parks in spot
        ↓
2. Sensor detects distance change (200cm → 30cm)
        ↓
3. Sensor publishes MQTT message
   Topic: parkmate/spot/status
   Payload: {spot_id: "SPOT001", occupied: true}
        ↓
4. MQTT Broker receives and distributes message
        ↓
5. Flask Backend receives MQTT message
        ↓
6. Backend updates MongoDB
   • parking_spots: Set occupied = true
   • parking_history: Insert new event
   • parking_lots: Update available_spots count
        ↓
7. Backend publishes LED command
   Topic: parkmate/led/command
   Payload: {spot_id: "SPOT001", color: "red"}
        ↓
8. Backend broadcasts WebSocket event
   Event: spot_update
        ↓
9. All connected web clients receive update
        ↓
10. UI updates spot color (green → red)
```

### Manual Override Flow
```
1. Owner clicks "Set Occupied" button
        ↓
2. Frontend sends POST request
   /api/lots/LOT001/override
   {spot_id: "SPOT001", occupied: true}
        ↓
3. Backend updates MongoDB
   • Set manual_override flag
   • Update spot status
        ↓
4. Backend broadcasts WebSocket event
        ↓
5. All clients see immediate update
```

### Initial Page Load Flow
```
1. User opens http://localhost:5000/
        ↓
2. Browser loads HTML/CSS/JS
        ↓
3. JavaScript initiates WebSocket connection
        ↓
4. JavaScript fetches parking lots
   GET /api/lots
        ↓
5. User selects a lot from dropdown
        ↓
6. JavaScript fetches lot details
   GET /api/lots/LOT001
        ↓
7. Display statistics and parking grid
        ↓
8. WebSocket receives real-time updates
```

## 🌐 Network Communication

### MQTT Messages

**Sensor → Broker (Status Update)**
```json
{
  "spot_id": "SPOT001",
  "lot_id": "LOT001",
  "occupied": true,
  "distance": 35,
  "timestamp": "2024-01-01T12:00:00Z"
}
```

**Broker → Sensor (LED Command)**
```json
{
  "spot_id": "SPOT001",
  "lot_id": "LOT001",
  "color": "red"
}
```

### WebSocket Messages

**Server → Client (Spot Update)**
```json
{
  "spot_id": "SPOT001",
  "lot_id": "LOT001",
  "occupied": true,
  "distance": 35
}
```

### REST API Requests

**GET /api/lots/LOT001**
```json
{
  "lot_id": "LOT001",
  "name": "Central Parking Tower",
  "total_spots": 20,
  "available_spots": 15,
  "occupied_spots": 5,
  "spots": [...]
}
```

## 🔐 Security Considerations

### Current Implementation
- CORS enabled for development
- No authentication (development mode)
- Local network only

### Production Enhancements
- Add TLS/SSL for MQTT (port 8883)
- Implement user authentication (JWT)
- Add API rate limiting
- Enable HTTPS for web interface
- Implement MQTT username/password
- Add database authentication

## ⚡ Performance Optimizations

### Real-time Updates
- WebSocket for instant notifications
- MongoDB indexing on spot_id, lot_id
- Efficient MQTT QoS levels

### Scalability
- Horizontal scaling via multiple backends
- MongoDB sharding for large deployments
- MQTT broker clustering
- CDN for static assets

## 📊 Monitoring Points

### Key Metrics
- WebSocket connection count
- MQTT message throughput
- Database query performance
- API response times
- Sensor update frequency

### Health Checks
- MongoDB connection status
- MQTT broker connectivity
- WebSocket server status
- Sensor heartbeats

## 🔧 Configuration

All settings centralized in `config.py`:
- MongoDB connection
- MQTT broker settings
- Flask server configuration
- Sensor parameters
- System thresholds

## 🚀 Deployment Architecture

### Development (Current)
```
Single Machine:
├── MongoDB (localhost:27017)
├── Mosquitto (localhost:1883)
├── Flask Backend (localhost:5000)
└── Sensor Emulator (local process)
```

### Production (Future)
```
Cloud Infrastructure:
├── MongoDB Atlas (managed cluster)
├── MQTT Broker (AWS IoT Core / HiveMQ)
├── Flask Backend (containerized, auto-scaling)
├── Load Balancer
└── CDN for static assets
```

## 📈 Scalability Path

1. **Single Lot** → Current implementation
2. **Multiple Lots** → Add more sensor emulators
3. **City-wide** → Deploy multiple backends
4. **Regional** → Add database sharding
5. **National** → Implement microservices architecture

---

This architecture provides a solid foundation for a production-ready smart parking system while maintaining simplicity for educational purposes.
