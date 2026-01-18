# ParkMate - Testing Guide

## 🧪 Manual Testing Procedures

### Pre-requisites Checklist

- [ ] Python 3.8+ installed
- [ ] MongoDB running on port 27017
- [ ] Mosquitto MQTT broker running on port 1883
- [ ] Dependencies installed (`pip install -r requirements.txt`)

## 🚦 Test Scenarios

### Test 1: System Startup

**Objective:** Verify all components start successfully

**Steps:**
1. Start MongoDB: `mongod`
2. Start Mosquitto: `mosquitto -v`
3. Start Flask backend: `python app.py`
4. Start sensor emulator: `python emulators/sensor_emulator.py`

**Expected Results:**
- ✓ MongoDB connects successfully
- ✓ MQTT broker accepts connections
- ✓ Flask server starts on port 5000
- ✓ Sensors connect to MQTT broker
- ✓ No error messages in console

**Pass/Fail:** ___________

---

### Test 2: Database Initialization

**Objective:** Verify database setup and sample data creation

**Steps:**
1. Start backend server
2. Send POST request: `curl -X POST http://localhost:5000/api/init`
3. Check response
4. Verify in MongoDB: `mongosh`
   ```javascript
   use parkmate_db
   db.parking_lots.find()
   db.parking_spots.find()
   ```

**Expected Results:**
- ✓ API returns success message
- ✓ LOT001 created with 20 spots
- ✓ All spots show in database
- ✓ Initial status: all spots available

**Pass/Fail:** ___________

---

### Test 3: Driver Interface - Initial Load

**Objective:** Verify driver interface loads and displays data

**Steps:**
1. Open browser: http://localhost:5000/
2. Check page load
3. Verify lot selector shows LOT001
4. Check statistics display
5. Verify parking grid displays 20 spots

**Expected Results:**
- ✓ Page loads without errors
- ✓ "Central Parking Tower" appears in dropdown
- ✓ Statistics show: Total=20, Available=20, Occupied=0
- ✓ All 20 spots display in grid
- ✓ All spots show green (available)
- ✓ Connection status shows "Live Updates Active"

**Pass/Fail:** ___________

---

### Test 4: Real-time Sensor Updates

**Objective:** Verify real-time updates from sensors to UI

**Steps:**
1. Open driver interface
2. Keep browser window visible
3. Watch sensor emulator console for status changes
4. Observe UI updates

**Expected Results:**
- ✓ When sensor detects "occupied", spot turns red in UI
- ✓ When sensor detects "available", spot turns green in UI
- ✓ Updates appear within 1-2 seconds
- ✓ Statistics update automatically
- ✓ No page refresh needed

**Pass/Fail:** ___________

---

### Test 5: Owner Dashboard - Overview

**Objective:** Verify owner dashboard displays correctly

**Steps:**
1. Open browser: http://localhost:5000/owner
2. Select LOT001 from dropdown
3. Check all dashboard sections

**Expected Results:**
- ✓ Overview metrics display correctly
- ✓ Revenue section shows price per hour
- ✓ Spot management table shows all 20 spots
- ✓ Each spot shows status, distance, last update
- ✓ Manual override buttons visible

**Pass/Fail:** ___________

---

### Test 6: Manual Override Functionality

**Objective:** Verify owner can manually change spot status

**Steps:**
1. Open owner dashboard
2. Find a spot that is "Available" (green)
3. Click "Set Occupied" button
4. Observe changes
5. Open driver interface in another tab
6. Verify change appears there too

**Expected Results:**
- ✓ Spot status changes to "Occupied"
- ✓ Badge turns red
- ✓ Change reflects in overview statistics
- ✓ Driver interface shows spot as red
- ✓ Update happens immediately (< 1 second)

**Pass/Fail:** ___________

---

### Test 7: Multi-client Real-time Sync

**Objective:** Verify multiple clients receive updates simultaneously

**Steps:**
1. Open driver interface in Browser 1
2. Open owner dashboard in Browser 2
3. Open another driver interface in Browser 3
4. Use Browser 2 to override a spot
5. Watch Browsers 1 and 3

**Expected Results:**
- ✓ All browsers show same initial state
- ✓ Override in Browser 2 triggers updates in all browsers
- ✓ Updates appear simultaneously
- ✓ No need to refresh any browser

**Pass/Fail:** ___________

---

### Test 8: MQTT Communication

**Objective:** Verify MQTT messages are published and received

**Steps:**
1. Open terminal and subscribe to all MQTT topics:
   ```bash
   mosquitto_sub -t 'parkmate/#' -v
   ```
2. Start sensor emulator
3. Observe messages

**Expected Results:**
- ✓ See `parkmate/spot/status` messages from sensors
- ✓ See `parkmate/led/command` messages from backend
- ✓ JSON payloads are valid
- ✓ Messages include spot_id, lot_id, occupied, distance

**Pass/Fail:** ___________

---

### Test 9: API Endpoints

**Objective:** Verify all REST API endpoints work correctly

**Test 9.1: GET /api/lots**
```bash
curl http://localhost:5000/api/lots
```
Expected: Array with LOT001 details

**Test 9.2: GET /api/lots/LOT001**
```bash
curl http://localhost:5000/api/lots/LOT001
```
Expected: Lot details with spots array

**Test 9.3: GET /api/spots**
```bash
curl http://localhost:5000/api/spots
```
Expected: Array of all parking spots

**Test 9.4: GET /api/stats/LOT001**
```bash
curl http://localhost:5000/api/stats/LOT001
```
Expected: Current status and history

**Test 9.5: POST /api/lots/LOT001/override**
```bash
curl -X POST http://localhost:5000/api/lots/LOT001/override \
  -H "Content-Type: application/json" \
  -d '{"spot_id":"SPOT001","occupied":true}'
```
Expected: {"success": true}

**Pass/Fail:** ___________

---

### Test 10: Sensor Emulator Configuration

**Objective:** Verify sensor emulator accepts custom parameters

**Steps:**
1. Stop current sensor emulator
2. Start with custom settings:
   ```bash
   python emulators/sensor_emulator.py --spots 10 --lot LOT001 --interval 3
   ```
3. Verify in UI

**Expected Results:**
- ✓ Only 10 spots appear (SPOT001-SPOT010)
- ✓ Updates occur every 3 seconds
- ✓ Console shows correct configuration

**Pass/Fail:** ___________

---

### Test 11: Database Persistence

**Objective:** Verify data persists across restarts

**Steps:**
1. Override a few spots to "occupied"
2. Stop Flask backend (Ctrl+C)
3. Stop sensor emulator (Ctrl+C)
4. Restart Flask backend
5. Open driver interface

**Expected Results:**
- ✓ Previous spot statuses are preserved
- ✓ Statistics show correct counts
- ✓ History is maintained

**Pass/Fail:** ___________

---

### Test 12: Error Handling - MongoDB Down

**Objective:** Verify graceful handling of database failure

**Steps:**
1. Start system normally
2. Stop MongoDB service
3. Try to access driver interface
4. Check console errors

**Expected Results:**
- ✓ System logs error message
- ✓ No crash/exception
- ✓ Attempts to reconnect

**Pass/Fail:** ___________

---

### Test 13: Error Handling - MQTT Broker Down

**Objective:** Verify handling of MQTT broker failure

**Steps:**
1. Start system normally
2. Stop Mosquitto broker
3. Check sensor emulator and backend logs

**Expected Results:**
- ✓ Sensors log connection error
- ✓ Backend logs connection error
- ✓ System continues running
- ✓ UI still accessible (shows last known state)

**Pass/Fail:** ___________

---

### Test 14: Performance - Multiple Concurrent Updates

**Objective:** Verify system handles multiple simultaneous updates

**Steps:**
1. Start system with 20 spots
2. Trigger multiple spot changes rapidly
3. Monitor UI responsiveness

**Expected Results:**
- ✓ All updates appear in UI
- ✓ No updates lost
- ✓ UI remains responsive
- ✓ Statistics update correctly

**Pass/Fail:** ___________

---

### Test 15: Browser Compatibility

**Objective:** Verify interfaces work across browsers

**Browsers to Test:**
- [ ] Chrome/Edge
- [ ] Firefox
- [ ] Safari (if available)

**Steps:**
1. Open driver interface in each browser
2. Open owner dashboard in each browser
3. Test all features

**Expected Results:**
- ✓ Layout displays correctly
- ✓ WebSocket connects successfully
- ✓ All buttons work
- ✓ Real-time updates work

**Pass/Fail:** ___________

---

## 📊 Test Summary

| Test # | Test Name | Status | Notes |
|--------|-----------|--------|-------|
| 1 | System Startup | ☐ | |
| 2 | Database Init | ☐ | |
| 3 | Driver Interface | ☐ | |
| 4 | Real-time Updates | ☐ | |
| 5 | Owner Dashboard | ☐ | |
| 6 | Manual Override | ☐ | |
| 7 | Multi-client Sync | ☐ | |
| 8 | MQTT Communication | ☐ | |
| 9 | API Endpoints | ☐ | |
| 10 | Sensor Config | ☐ | |
| 11 | Persistence | ☐ | |
| 12 | MongoDB Failure | ☐ | |
| 13 | MQTT Failure | ☐ | |
| 14 | Performance | ☐ | |
| 15 | Browser Compat | ☐ | |

## 🔍 Debugging Tips

### Check MongoDB
```bash
# Connect to MongoDB
mongosh

# Check databases
show dbs

# Use parkmate database
use parkmate_db

# View collections
show collections

# Query spots
db.parking_spots.find().pretty()
```

### Check MQTT
```bash
# Subscribe to all topics
mosquitto_sub -t 'parkmate/#' -v

# Test publish
mosquitto_pub -t 'parkmate/test' -m 'hello'
```

### Check Logs
```bash
# Backend logs (in terminal running app.py)
# Sensor logs (in terminal running sensor_emulator.py)

# Browser console (F12 in browser)
```

### Network Debugging
```bash
# Check if ports are open
netstat -an | findstr "5000"  # Flask
netstat -an | findstr "27017" # MongoDB
netstat -an | findstr "1883"  # MQTT
```

## ✅ Acceptance Criteria

System is ready for demonstration if:
- [x] All 15 tests pass
- [x] Real-time updates work smoothly
- [x] Both interfaces display correctly
- [x] No critical errors in console
- [x] Database persists data correctly
- [x] MQTT communication is reliable

---

**Tester Name:** ________________

**Date:** ________________

**Overall Result:** PASS / FAIL

**Comments:**
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
