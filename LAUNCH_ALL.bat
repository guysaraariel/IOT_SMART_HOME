@echo off
REM ====================================================================
REM  ParkMate IoT System - COMPLETE LAUNCHER
REM  Starts ALL components of the ParkMate system
REM ====================================================================

color 0A
title ParkMate - Complete System Launcher

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║        PARKMATE IOT PARKING MANAGEMENT SYSTEM                  ║
echo ║              Complete System Launcher                          ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

echo This script will launch ALL components of the ParkMate system:
echo.
echo   1. Flask Backend Server (Data Manager)
echo   2. Ultrasonic Sensor Emulator (Data Producer)
echo   3. LED/Relay Actuator Emulator (Actuator - Receives Commands)
echo   4. Button/Knob Emulator (Actuator - Sends Commands)
echo   5. DHT Sensor Emulator (Environmental Data Producer)
echo.
echo ════════════════════════════════════════════════════════════════
echo.

REM Check if MongoDB is running
echo [1/3] Checking MongoDB status...
tasklist /FI "IMAGENAME eq mongod.exe" 2>NUL | find /I /N "mongod.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo ✓ MongoDB is running
) else (
    echo ✗ WARNING: MongoDB is NOT running!
    echo   Please start MongoDB first:
    echo   - Run 'mongod' in a separate terminal
    echo   - Or start MongoDB service
    echo.
    pause
)

REM Check if Mosquitto is running
echo [2/3] Checking Mosquitto MQTT Broker status...
tasklist /FI "IMAGENAME eq mosquitto.exe" 2>NUL | find /I /N "mosquitto.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo ✓ Mosquitto MQTT Broker is running
) else (
    echo ✗ WARNING: Mosquitto is NOT running!
    echo   Please start Mosquitto first:
    echo   - Run 'mosquitto' in a separate terminal
    echo   - Or start Mosquitto service
    echo.
    pause
)

echo [3/3] Checking Python installation...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ✗ ERROR: Python is not installed or not in PATH
    echo   Please install Python 3.8+ from python.org
    pause
    exit /b 1
) else (
    python --version
    echo ✓ Python is installed
)

echo.
echo ════════════════════════════════════════════════════════════════
echo.
echo Starting all components in separate windows...
echo.
echo NOTE: Each component will open in its own command window
echo       Do NOT close these windows while the system is running!
echo.

REM Wait a bit for user to read
timeout /t 3 /nobreak >nul

REM 1. Start Flask Backend
echo [1/5] Starting Flask Backend Server...
start "ParkMate - Backend Server" cmd /k "color 0E && python app.py"
timeout /t 3 /nobreak >nul

REM 2. Start Sensor Emulator
echo [2/5] Starting Ultrasonic Sensor Emulator...
start "ParkMate - Ultrasonic Sensors" cmd /k "color 0B && python emulators/sensor_emulator.py"
timeout /t 2 /nobreak >nul

REM 3. Start LED Actuator
echo [3/5] Starting LED/Relay Actuator Emulator...
start "ParkMate - LED/Relay Actuators" cmd /k "color 0D && python emulators/led_actuator.py"
timeout /t 2 /nobreak >nul

REM 4. Start Button Emulator
echo [4/5] Starting Button/Knob Actuator Emulator...
start "ParkMate - Button/Knob Controls" cmd /k "color 0C && python emulators/button_emulator.py"
timeout /t 2 /nobreak >nul

REM 5. Start DHT Sensor
echo [5/5] Starting DHT Environmental Sensor Emulator...
start "ParkMate - DHT Sensor" cmd /k "color 09 && python emulators/dht_sensor_emulator.py"
timeout /t 2 /nobreak >nul

echo.
echo ════════════════════════════════════════════════════════════════
echo.
echo ✓ ALL COMPONENTS STARTED SUCCESSFULLY!
echo.
echo ════════════════════════════════════════════════════════════════
echo.
echo  ACCESS THE APPLICATION:
echo.
echo    Driver Interface:    http://localhost:5000/
echo    Owner Dashboard:     http://localhost:5000/owner
echo.
echo ════════════════════════════════════════════════════════════════
echo.
echo  RUNNING COMPONENTS (5 separate windows):
echo.
echo    1. Backend Server       - Yellow window (Flask + MQTT)
echo    2. Ultrasonic Sensors   - Cyan window   (Data Producer)
echo    3. LED/Relay Actuators  - Purple window (Receives LED commands)
echo    4. Button/Knob Controls - Red window    (Interactive control)
echo    5. DHT Sensor          - Blue window    (Environmental data)
echo.
echo ════════════════════════════════════════════════════════════════
echo.
echo  TO STOP THE SYSTEM:
echo    - Close each colored window individually, OR
echo    - Press Ctrl+C in each window
echo.
echo ════════════════════════════════════════════════════════════════
echo.
echo.

REM Open web browser automatically
echo Opening web browser in 5 seconds...
timeout /t 5 /nobreak >nul

start http://localhost:5000/

echo.
echo System is now running! This window can be closed.
echo The system will continue running in the background windows.
echo.
pause
