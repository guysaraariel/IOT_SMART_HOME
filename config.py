"""
ParkMate Configuration File
Customize these settings for your deployment
"""

# MongoDB Configuration
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_DATABASE = 'parkmate_db'

# MQTT Configuration
MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60

# MQTT Topics
TOPIC_SPOT_STATUS = 'parkmate/spot/status'
TOPIC_LED_COMMAND = 'parkmate/led/command'
TOPIC_PAYMENT = 'parkmate/payment'

# Flask Configuration
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000
FLASK_DEBUG = True

# Sensor Emulator Configuration
DEFAULT_LOT_ID = 'LOT001'
DEFAULT_NUM_SPOTS = 20
DEFAULT_UPDATE_INTERVAL = 5  # seconds

# Parking Lot Settings
DEFAULT_PRICE_PER_HOUR = 2.0
DEFAULT_LOT_NAME = 'Central Parking Tower'
DEFAULT_LOT_ADDRESS = '123 Main Street'

# Sensor Thresholds
OCCUPIED_THRESHOLD = 100  # cm - distance below this means occupied
EMPTY_DISTANCE = 200      # cm - typical distance to floor
MIN_CAR_DISTANCE = 10     # cm - minimum distance when car present
MAX_CAR_DISTANCE = 50     # cm - maximum distance when car present

# System Settings
CORS_ENABLED = True
SOCKETIO_ASYNC_MODE = 'eventlet'
