from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from pymongo import MongoClient
from datetime import datetime
import paho.mqtt.client as mqtt
import json
import os
import random

app = Flask(__name__, static_folder='static')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# MongoDB Setup
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['parkmate_db']
parking_spots = db['parking_spots']
parking_lots = db['parking_lots']
parking_history = db['parking_history']
users = db['users']
environment_data = db['environment_data']
button_events = db['button_events']
alerts = db['alerts']

# MQTT Setup
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
mqtt_client = mqtt.Client()

# MQTT Topics
TOPIC_SPOT_STATUS = "parkmate/spot/status"
TOPIC_LED_COMMAND = "parkmate/led/command"
TOPIC_RELAY_COMMAND = "parkmate/relay/command"
TOPIC_PAYMENT = "parkmate/payment"
TOPIC_ENVIRONMENT = "parkmate/environment"
TOPIC_BUTTON_PRESS = "parkmate/button/press"
TOPIC_KNOB_ADJUST = "parkmate/knob/adjust"
TOPIC_ALERTS = "parkmate/alerts"

def on_mqtt_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe(TOPIC_SPOT_STATUS)
    client.subscribe(TOPIC_PAYMENT)
    client.subscribe(TOPIC_ENVIRONMENT)
    client.subscribe(TOPIC_BUTTON_PRESS)
    client.subscribe(TOPIC_KNOB_ADJUST)
    client.subscribe(TOPIC_ALERTS)
    print("Subscribed to all MQTT topics")

def on_mqtt_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())

        if msg.topic == TOPIC_SPOT_STATUS:
            handle_spot_status(payload)
        elif msg.topic == TOPIC_PAYMENT:
            handle_payment(payload)
        elif msg.topic == TOPIC_ENVIRONMENT:
            handle_environment_data(payload)
        elif msg.topic == TOPIC_BUTTON_PRESS:
            handle_button_press(payload)
        elif msg.topic == TOPIC_KNOB_ADJUST:
            handle_knob_adjust(payload)
        elif msg.topic == TOPIC_ALERTS:
            handle_alert(payload)

    except Exception as e:
        print(f"Error processing MQTT message: {e}")

def handle_spot_status(data):
    """Handle parking spot status updates from sensors"""
    spot_id = data.get('spot_id')
    lot_id = data.get('lot_id')
    occupied = data.get('occupied')
    distance = data.get('distance')

    # Update spot in database
    parking_spots.update_one(
        {'spot_id': spot_id, 'lot_id': lot_id},
        {
            '$set': {
                'occupied': occupied,
                'distance': distance,
                'last_update': datetime.now()
            }
        },
        upsert=True
    )

    # Log to history
    parking_history.insert_one({
        'spot_id': spot_id,
        'lot_id': lot_id,
        'occupied': occupied,
        'timestamp': datetime.now()
    })

    # Update lot availability count
    update_lot_availability(lot_id)

    # Send LED command
    led_color = "red" if occupied else "green"
    mqtt_client.publish(TOPIC_LED_COMMAND, json.dumps({
        'spot_id': spot_id,
        'lot_id': lot_id,
        'color': led_color
    }))

    # Notify connected clients via WebSocket
    socketio.emit('spot_update', {
        'spot_id': spot_id,
        'lot_id': lot_id,
        'occupied': occupied,
        'distance': distance
    })

def handle_payment(data):
    """Handle payment notifications"""
    socketio.emit('payment_notification', data)

def handle_environment_data(data):
    """Handle environmental sensor data (DHT sensor)"""
    sensor_id = data.get('sensor_id')
    lot_id = data.get('lot_id')
    temperature = data.get('temperature')
    humidity = data.get('humidity')
    heat_index = data.get('heat_index')

    # Store in database
    environment_data.insert_one({
        'sensor_id': sensor_id,
        'lot_id': lot_id,
        'temperature': temperature,
        'humidity': humidity,
        'heat_index': heat_index,
        'timestamp': datetime.now()
    })

    # Update lot with latest environmental data
    parking_lots.update_one(
        {'lot_id': lot_id},
        {
            '$set': {
                'temperature': temperature,
                'humidity': humidity,
                'heat_index': heat_index,
                'env_last_update': datetime.now()
            }
        }
    )

    # Broadcast to connected clients
    socketio.emit('environment_update', {
        'lot_id': lot_id,
        'temperature': temperature,
        'humidity': humidity,
        'heat_index': heat_index
    })

    print(f"Environment update: Lot {lot_id} - Temp: {temperature}°C, Humidity: {humidity}%")

def handle_button_press(data):
    """Handle button press events"""
    button_id = data.get('button_id')
    spot_id = data.get('spot_id')
    action = data.get('action')

    # Store button event
    button_events.insert_one({
        'button_id': button_id,
        'spot_id': spot_id,
        'action': action,
        'timestamp': datetime.now()
    })

    # Execute action based on button press
    if action == 'toggle':
        # Toggle spot status
        spot = parking_spots.find_one({'spot_id': spot_id})
        if spot:
            new_status = not spot.get('occupied', False)
            # Update distance based on new status
            new_distance = random.randint(30, 50) if new_status else random.randint(180, 220)
            parking_spots.update_one(
                {'spot_id': spot_id},
                {'$set': {'occupied': new_status, 'distance': new_distance, 'last_update': datetime.now()}}
            )
            lot_id = spot.get('lot_id')
            update_lot_availability(lot_id)

            # Send LED command
            led_color = "red" if new_status else "green"
            mqtt_client.publish(TOPIC_LED_COMMAND, json.dumps({
                'spot_id': spot_id,
                'lot_id': lot_id,
                'color': led_color
            }))

            # Notify clients
            socketio.emit('spot_update', {
                'spot_id': spot_id,
                'lot_id': lot_id,
                'occupied': new_status,
                'distance': new_distance,
                'source': 'button'
            })

    elif action == 'occupy':
        spot = parking_spots.find_one({'spot_id': spot_id})
        if spot:
            # Simulate car present - distance should be 30-50cm
            new_distance = random.randint(30, 50)
            parking_spots.update_one(
                {'spot_id': spot_id},
                {'$set': {'occupied': True, 'distance': new_distance, 'last_update': datetime.now()}}
            )
            lot_id = spot.get('lot_id')
            update_lot_availability(lot_id)
            mqtt_client.publish(TOPIC_LED_COMMAND, json.dumps({
                'spot_id': spot_id,
                'lot_id': lot_id,
                'color': 'red'
            }))
            socketio.emit('spot_update', {
                'spot_id': spot_id,
                'lot_id': lot_id,
                'occupied': True,
                'distance': new_distance,
                'source': 'button'
            })

    elif action == 'free':
        spot = parking_spots.find_one({'spot_id': spot_id})
        if spot:
            # Simulate empty spot - distance should be ~200cm (floor)
            new_distance = random.randint(180, 220)
            parking_spots.update_one(
                {'spot_id': spot_id},
                {'$set': {'occupied': False, 'distance': new_distance, 'last_update': datetime.now()}}
            )
            lot_id = spot.get('lot_id')
            update_lot_availability(lot_id)
            mqtt_client.publish(TOPIC_LED_COMMAND, json.dumps({
                'spot_id': spot_id,
                'lot_id': lot_id,
                'color': 'green'
            }))
            socketio.emit('spot_update', {
                'spot_id': spot_id,
                'lot_id': lot_id,
                'occupied': False,
                'distance': new_distance,
                'source': 'button'
            })

    # Broadcast button event to clients
    socketio.emit('button_event', data)

    print(f"Button press: {button_id} - Spot {spot_id} - Action: {action}")

def handle_knob_adjust(data):
    """Handle knob adjustment events"""
    knob_id = data.get('knob_id')
    function = data.get('function')
    value = data.get('value')

    # Broadcast knob adjustment to clients
    socketio.emit('knob_adjust', data)

    print(f"Knob adjust: {knob_id} - {function}: {value}%")

def handle_alert(data):
    """Handle environmental alerts"""
    sensor_id = data.get('sensor_id')
    lot_id = data.get('lot_id')
    alert = data.get('alert')

    # Store alert
    alerts.insert_one({
        'sensor_id': sensor_id,
        'lot_id': lot_id,
        'alert_type': alert.get('type'),
        'severity': alert.get('severity'),
        'message': alert.get('message'),
        'recommendation': alert.get('recommendation'),
        'timestamp': datetime.now()
    })

    # Broadcast alert to clients
    socketio.emit('alert', {
        'lot_id': lot_id,
        'alert': alert
    })

    print(f"Alert: {lot_id} - {alert.get('type')} - {alert.get('message')}")

def update_lot_availability(lot_id):
    """Update the available spots count for a parking lot"""
    total_spots = parking_spots.count_documents({'lot_id': lot_id})
    occupied_spots = parking_spots.count_documents({'lot_id': lot_id, 'occupied': True})
    available_spots = total_spots - occupied_spots

    parking_lots.update_one(
        {'lot_id': lot_id},
        {
            '$set': {
                'total_spots': total_spots,
                'occupied_spots': occupied_spots,
                'available_spots': available_spots,
                'last_update': datetime.now()
            }
        },
        upsert=True
    )

# Initialize MQTT
mqtt_client.on_connect = on_mqtt_connect
mqtt_client.on_message = on_mqtt_message

try:
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_start()
except Exception as e:
    print(f"Could not connect to MQTT broker: {e}")

# REST API Endpoints

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/owner')
def owner_dashboard():
    return send_from_directory('static', 'owner.html')

@app.route('/api/lots', methods=['GET'])
def get_parking_lots():
    """Get all parking lots with availability"""
    lots = list(parking_lots.find({}, {'_id': 0}))
    return jsonify(lots)

@app.route('/api/lots/<lot_id>', methods=['GET'])
def get_parking_lot(lot_id):
    """Get specific parking lot details"""
    lot = parking_lots.find_one({'lot_id': lot_id}, {'_id': 0})
    if not lot:
        return jsonify({'error': 'Lot not found'}), 404

    # Get all spots for this lot
    spots = list(parking_spots.find({'lot_id': lot_id}, {'_id': 0}))
    lot['spots'] = spots

    return jsonify(lot)

@app.route('/api/spots', methods=['GET'])
def get_all_spots():
    """Get all parking spots"""
    lot_id = request.args.get('lot_id')
    query = {'lot_id': lot_id} if lot_id else {}
    spots = list(parking_spots.find(query, {'_id': 0}))
    return jsonify(spots)

@app.route('/api/spots/<spot_id>', methods=['GET'])
def get_spot(spot_id):
    """Get specific spot details"""
    spot = parking_spots.find_one({'spot_id': spot_id}, {'_id': 0})
    if not spot:
        return jsonify({'error': 'Spot not found'}), 404
    return jsonify(spot)

@app.route('/api/stats/<lot_id>', methods=['GET'])
def get_lot_stats(lot_id):
    """Get statistics for a parking lot"""
    # Occupancy over time
    history = list(parking_history.find(
        {'lot_id': lot_id},
        {'_id': 0}
    ).sort('timestamp', -1).limit(100))

    # Current status
    lot = parking_lots.find_one({'lot_id': lot_id}, {'_id': 0})

    return jsonify({
        'current': lot,
        'history': history
    })

@app.route('/api/lots/<lot_id>/override', methods=['POST'])
def manual_override(lot_id):
    """Manual override for spot status (Owner mode)"""
    data = request.json
    spot_id = data.get('spot_id')
    occupied = data.get('occupied')

    # Update distance based on occupied status
    # Occupied = car present (30-50cm), Available = empty (180-220cm)
    new_distance = random.randint(30, 50) if occupied else random.randint(180, 220)

    parking_spots.update_one(
        {'spot_id': spot_id, 'lot_id': lot_id},
        {
            '$set': {
                'occupied': occupied,
                'distance': new_distance,
                'manual_override': True,
                'last_update': datetime.now()
            }
        }
    )

    update_lot_availability(lot_id)

    # Send LED command
    led_color = "red" if occupied else "green"
    mqtt_client.publish(TOPIC_LED_COMMAND, json.dumps({
        'spot_id': spot_id,
        'lot_id': lot_id,
        'color': led_color
    }))

    # Broadcast update to clients
    socketio.emit('spot_update', {
        'spot_id': spot_id,
        'lot_id': lot_id,
        'occupied': occupied,
        'distance': new_distance,
        'source': 'manual_override'
    })

    return jsonify({'success': True})

@app.route('/api/init', methods=['POST'])
def initialize_data():
    """Initialize sample parking lot data"""
    # Clear existing data
    parking_spots.delete_many({})
    parking_lots.delete_many({})

    # Create sample parking lot
    lot_id = "LOT001"
    parking_lots.insert_one({
        'lot_id': lot_id,
        'name': 'Central Parking Tower',
        'address': '123 Main Street',
        'total_spots': 20,
        'occupied_spots': 0,
        'available_spots': 20,
        'price_per_hour': 2.0,
        'last_update': datetime.now()
    })

    # Create 20 parking spots
    for i in range(1, 21):
        spot_id = f"SPOT{i:03d}"
        parking_spots.insert_one({
            'spot_id': spot_id,
            'lot_id': lot_id,
            'occupied': False,
            'distance': 200,
            'last_update': datetime.now()
        })

    return jsonify({'success': True, 'message': 'Data initialized'})

@app.route('/api/environment/<lot_id>', methods=['GET'])
def get_environment_data(lot_id):
    """Get latest environmental data for a parking lot"""
    # Get latest reading
    latest = environment_data.find_one(
        {'lot_id': lot_id},
        {'_id': 0},
        sort=[('timestamp', -1)]
    )

    # Get recent history
    history = list(environment_data.find(
        {'lot_id': lot_id},
        {'_id': 0}
    ).sort('timestamp', -1).limit(20))

    return jsonify({
        'latest': latest,
        'history': history
    })

@app.route('/api/alerts/<lot_id>', methods=['GET'])
def get_alerts(lot_id):
    """Get recent alerts for a parking lot"""
    recent_alerts = list(alerts.find(
        {'lot_id': lot_id},
        {'_id': 0}
    ).sort('timestamp', -1).limit(10))

    return jsonify(recent_alerts)

@app.route('/api/button_events', methods=['GET'])
def get_button_events():
    """Get recent button events"""
    events = list(button_events.find({}, {'_id': 0}).sort('timestamp', -1).limit(20))
    return jsonify(events)

# WebSocket Events
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('connected', {'data': 'Connected to ParkMate'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    print("Starting ParkMate Backend Server...")
    print("Make sure MongoDB is running on localhost:27017")
    print("Make sure MQTT broker (mosquitto) is running on localhost:1883")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
