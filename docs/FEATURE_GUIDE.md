# ParkMate - Feature Guide

## 🎛️ Auto-Update Toggle Feature

### Quick Overview

The Auto-Update Toggle allows you to control when the interface receives real-time updates from the parking sensors.

---

## 📍 Where to Find It

The toggle button appears in **both interfaces**:

- **Driver Interface** (http://localhost:5000/)
- **Owner Dashboard** (http://localhost:5000/owner)

Location: Top navigation bar, between "Refresh" and "Owner Dashboard" buttons

---

## 🎨 Visual Guide

### Button States

**Active (Updates ON):**
```
┌────────────────────────────┐
│  ⚡ Auto Updates: ON       │  <- Bright cyan background
└────────────────────────────┘
```

**Inactive (Updates OFF):**
```
┌────────────────────────────┐
│  ⚡ Auto Updates: OFF      │  <- Dimmed/transparent
└────────────────────────────┘
```

### Status Bar States

**1. Live Updates Active (Green)**
```
┌──────────────────────────────────────┐
│  ● Live Updates Active               │  <- Pulsing green dot
└──────────────────────────────────────┘
```

**2. Auto Updates Paused (Yellow/Amber)**
```
┌──────────────────────────────────────┐
│  Auto Updates Paused - Click Refresh │  <- Yellow warning
│  to Update                            │
└──────────────────────────────────────┘
```

**3. Disconnected (Red)**
```
┌──────────────────────────────────────┐
│  Disconnected - Attempting to        │  <- Red error state
│  reconnect...                         │
└──────────────────────────────────────┘
```

---

## 🔄 How It Works

### With Auto Updates ON (Default)

```
Sensor detects car
      ↓
MQTT message sent
      ↓
Backend receives
      ↓
WebSocket broadcast
      ↓
✅ UI updates IMMEDIATELY
```

### With Auto Updates OFF

```
Sensor detects car
      ↓
MQTT message sent
      ↓
Backend receives
      ↓
WebSocket broadcast
      ↓
❌ UI ignores the update
      ↓
💡 Click "Refresh" to manually update
```

---

## 📖 Usage Scenarios

### Scenario 1: Monitoring Mode
**Situation:** You want to watch parking changes in real-time

**Action:**
1. Keep "Auto Updates: ON" (default)
2. Watch spots change color automatically
3. Status shows green with pulsing indicator

### Scenario 2: Analysis Mode
**Situation:** You need to analyze current data without interruption

**Action:**
1. Click toggle to turn "Auto Updates: OFF"
2. Data freezes at current state
3. Analyze without spots changing
4. Click "Refresh" when ready for new data

### Scenario 3: Battery Saving
**Situation:** On mobile device, want to conserve battery

**Action:**
1. Turn "Auto Updates: OFF"
2. Manually refresh periodically
3. Reduces CPU and network usage

### Scenario 4: Taking Screenshots
**Situation:** Need to capture current state for reporting

**Action:**
1. Turn "Auto Updates: OFF"
2. State freezes - perfect for screenshots
3. Take your time documenting
4. Turn back ON when done

---

## 🎯 Step-by-Step Instructions

### To Disable Auto Updates

1. **Locate the button:** Find "⚡ Auto Updates: ON" in the navigation bar
2. **Click once:** Button changes to "Auto Updates: OFF" and becomes dimmed
3. **Observe status bar:** Changes to yellow "Auto Updates Paused"
4. **Verify:** Parking spots no longer change automatically

### To Enable Auto Updates

1. **Click the button:** "Auto Updates: OFF" → "Auto Updates: ON"
2. **Button highlights:** Becomes bright cyan
3. **Status bar updates:** Changes to green "Live Updates Active"
4. **Real-time resumes:** Spots update automatically again

### To Manually Refresh (When Paused)

1. **Ensure updates are OFF:** Button shows "Auto Updates: OFF"
2. **Click "🔄 Refresh":** Full page reload
3. **Latest data loads:** Shows current parking state
4. **Updates remain paused:** Toggle stays OFF after refresh

---

## ⚙️ Technical Notes

### What Happens Behind the Scenes

**When you toggle OFF:**
- WebSocket connection **stays active** (no disconnect)
- Incoming `spot_update` events are **ignored**
- Connection status remains "Connected"
- No data is lost - just not displayed

**When you toggle ON:**
- WebSocket events are **processed normally**
- UI updates occur **immediately** when data arrives
- Full real-time functionality restored

### Browser Console Messages

When toggling, check browser console (F12) for:

```javascript
// When turning OFF:
Auto updates disabled

// When turning ON:
Auto updates enabled
```

---

## 💡 Pro Tips

1. **Combine with Refresh:** Turn OFF updates, then use Refresh button to control exactly when data updates

2. **Quick Toggle:** The button responds instantly - no delay or loading time

3. **State Persists:** Your toggle preference is remembered during your session (until page reload)

4. **Independent per Tab:** Each browser tab has its own toggle state

5. **Works Offline:** Toggle function works even if backend is temporarily down

---

## 🔍 Troubleshooting

**Problem:** Button doesn't respond when clicked

**Solution:**
- Check browser console for errors (F12)
- Refresh the page
- Ensure JavaScript is enabled

---

**Problem:** Status stays "Paused" even when Auto Updates is ON

**Solution:**
- Toggle OFF then ON again
- Check WebSocket connection (should be green)
- Refresh the page

---

**Problem:** Updates still happening when toggle is OFF

**Solution:**
- This shouldn't happen - check browser console
- Try clearing browser cache
- Verify you're looking at the correct window/tab

---

## 📊 Comparison Table

| Feature | Auto Updates ON | Auto Updates OFF |
|---------|----------------|------------------|
| Real-time updates | ✅ Yes | ❌ No |
| WebSocket connection | ✅ Active | ✅ Active |
| Manual refresh works | ✅ Yes | ✅ Yes |
| Network usage | Higher | Lower |
| CPU usage | Normal | Reduced |
| Battery usage | Normal | Reduced |
| Best for | Monitoring | Analysis |

---

## 🎓 Learning Objectives

This feature demonstrates:
- Client-side state management
- Event handling control
- WebSocket communication patterns
- User interface feedback
- Progressive enhancement

---

**Version:** 1.2
**Last Updated:** January 2026
**Applies To:** Driver Interface & Owner Dashboard
