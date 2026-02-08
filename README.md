# hams-at-notifications
notifications for new hams.at satellite alerts

# 🛰️ HAMS.AT Satellite Alert Notifications

Get instant push notifications on your iPhone, Apple Watch, or desktop when new satellite alerts are posted on [hams.at](https://hams.at).

## ✨ Features

- 📱 **Real-time notifications** - Only notifies on NEW alerts (no spam!)
- 🛰️ **Detailed info** - Shows callsign, satellite, grid, time, mode, frequency
- ⌚ **Apple Watch support** - iOS notifications automatically sync to Smart Watch
- 💻 **Cross-platform** - Works on iOS, macOS, Linux, and Windows
- 🆓 **Completely free** - No subscriptions or paid apps required
- 🔒 **Privacy-focused** - Runs locally on your device

## 📋 Table of Contents

- [iOS Setup (iPhone/iPad)](#-ios-setup-iphoneipad)
- [macOS Setup](#-macos-setup)
- [Linux Setup](#-linux-setup)
- [Windows Setup](#-windows-setup)
- [Getting Your API Key](#-getting-your-api-key)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

---

## 📱 iOS Setup (iPhone/iPad)

### Requirements
- iPhone or iPad running iOS 14 or later
- Free [Scriptable](https://apps.apple.com/us/app/scriptable/id1405459188) app from App Store

### Step 1: Install Scriptable

1. Download **Scriptable** from the App Store
2. Open the app

### Step 2: Create the Script

1. In Scriptable, tap the **"+"** button (top right)
2. Tap on **"Untitled Script"** and rename it to **"HAMS Alerts"**
3. Delete any placeholder code
4. Copy the entire contents of [`hams_alerts.js`](hams_alerts.js)
5. Paste it into Scriptable
6. **Important:** Replace `PASTE YOUR API HERE` with your actual API key (see [Getting Your API Key](#-getting-your-api-key))
7. Tap **"Done"**

### Step 3: Test the Script

1. Tap on **"HAMS Alerts"** to run it
2. The first time it runs, it will remember all current alerts but won't notify
3. Run it again - you should see "No new alerts" (this is correct!)
4. When a new alert appears on hams.at, you'll get a notification!

### Step 4: Set Up Automatic Checks

You need to create iOS Shortcuts automations to run the script every 30 minutes.

**For every 30 minutes from 7:00 AM to 1:00 AM:**

1. Open the **Shortcuts** app
2. Tap **"Automation"** tab (bottom)
3. Tap **"+"** (top right)
4. Select **"Create Personal Automation"**
5. Choose **"Time of Day"**
6. Set the time (e.g., **7:00 AM**)
7. Set **Repeat: Daily**
8. Tap **"Next"**
9. Search for and add **"Scriptable"**
10. Select **"Run Script"**
11. Choose **"HAMS Alerts"**
12. Tap **"Next"**
13. **Turn OFF** "Ask Before Running" (important!)
14. Tap **"Done"**

**Repeat this process for each 30-minute interval:**

7:00 AM, 7:30 AM, 8:00 AM, 8:30 AM, 9:00 AM, 9:30 AM, 10:00 AM, 10:30 AM, 11:00 AM, 11:30 AM, 12:00 PM, 12:30 PM, 1:00 PM, 1:30 PM, 2:00 PM, 2:30 PM, 3:00 PM, 3:30 PM, 4:00 PM, 4:30 PM, 5:00 PM, 5:30 PM, 6:00 PM, 6:30 PM, 7:00 PM, 7:30 PM, 8:00 PM, 8:30 PM, 9:00 PM, 9:30 PM, 10:00 PM, 10:30 PM, 11:00 PM, 11:30 PM, 12:00 AM, 12:30 AM, 1:00 AM

**Time-saving tip:** After creating the first automation, you can duplicate it and just change the time!

### Step 5: Disable Shortcuts Notifications (Optional)

To avoid "Running your automation" notifications:

1. Go to iPhone **Settings**
2. Scroll to **Shortcuts**
3. Tap **Notifications**
4. Turn **OFF** "Notify When Run"

Your HAMS alerts will still come through (they're from Scriptable, not Shortcuts)!

### 🍎 Apple Watch / Garmin Watch

Notifications automatically sync to your smart Watch - no extra setup needed!

---

## 💻 macOS Setup

### Requirements
- macOS (any recent version)
- Python 3 (comes pre-installed on macOS)

### Step 1: Download the Script

1. Download [`hams_alerts.py`](hams_alerts.py) from this repository
2. Save it to your home folder or anywhere convenient
3. Open the file in a text editor
4. Replace `PASTE YOUR API KEY HERE` with your actual API key

### Step 2: Install Dependencies

Open Terminal and run:

```bash
pip3 install requests --break-system-packages
```

### Step 3: Make the Script Executable

```bash
chmod +x ~/hams_alerts.py
```

### Step 4: Test the Script

```bash
python3 ~/hams_alerts.py
```

You should see output showing how many alerts were found.

### Step 5: Set Up Automatic Checks (Every 30 Minutes)

1. Open Terminal
2. Edit your crontab:

```bash
crontab -e
```

3. Press `i` to enter insert mode
4. Add this line (adjust the path if you saved the script elsewhere):

```
*/30 * * * * /usr/bin/python3 ~/hams_alerts.py >> ~/hams_alerts.log 2>&1
```

5. Press `Esc`, then type `:wq` and press Enter

The script will now run every 30 minutes automatically!

### View Logs

```bash
tail -f ~/hams_alerts.log
```

---

## 🐧 Linux Setup

### Requirements
- Python 3
- `notify-send` (usually pre-installed)

### Step 1: Install Dependencies

```bash
# Debian/Ubuntu
sudo apt-get install python3 python3-pip libnotify-bin

# Fedora
sudo dnf install python3 python3-pip libnotify

# Arch
sudo pacman -S python python-pip libnotify

# Install Python packages
pip3 install requests
```

### Step 2: Download and Configure

1. Download [`hams_alerts.py`](hams_alerts.py)
2. Save to `~/hams_alerts.py`
3. Edit the file and replace `PASTE YOUR API KEY HERE` with your API key
4. Make executable:

```bash
chmod +x ~/hams_alerts.py
```

### Step 3: Test

```bash
python3 ~/hams_alerts.py
```

### Step 4: Set Up Cron Job

```bash
crontab -e
```

Add:

```
*/30 * * * * /usr/bin/python3 ~/hams_alerts.py >> ~/hams_alerts.log 2>&1
```

---

## 🪟 Windows Setup

### Requirements
- Python 3 ([Download here](https://www.python.org/downloads/))
- Make sure to check "Add Python to PATH" during installation

### Step 1: Install Dependencies

Open Command Prompt or PowerShell:

```powershell
pip install requests win10toast
```

### Step 2: Download and Configure

1. Download [`hams_alerts.py`](hams_alerts.py)
2. Save to `C:\Users\YourUsername\hams_alerts.py`
3. Edit with Notepad and replace `PASTE YOUR API KEY HERE` with your API key

### Step 3: Test

```powershell
python C:\Users\YourUsername\hams_alerts.py
```

### Step 4: Set Up Task Scheduler (Every 30 Minutes)

1. Open **Task Scheduler**
2. Click **"Create Basic Task"**
3. Name: **HAMS Alerts**
4. Trigger: **Daily**
5. Start time: **12:00 AM**
6. Action: **Start a program**
7. Program: `python`
8. Arguments: `C:\Users\YourUsername\hams_alerts.py`
9. Finish the wizard
10. Right-click the task → **Properties**
11. Go to **Triggers** tab → **Edit**
12. Check **"Repeat task every: 30 minutes"**
13. Duration: **1 day**
14. Click **OK**

---

## 🔑 Getting Your API Key

1. Go to [hams.at](https://hams.at)
2. Log in or create an account
3. Click on your **callsign** (top right)
4. Go to **Settings** or **API Settings**
5. Find your **API Key** (it looks like: `5ff939cc-XXXX-XXXX-XXXX-afbbXXXX1f1c`)
6. Copy it and paste it into the script where it says `PASTE YOUR API HERE` or `PASTE YOUR API KEY HERE`

**Security Note:** Keep your API key private! Don't share screenshots with your API key visible.

---

## 🔧 Troubleshooting

### iOS: "No notifications appearing"

1. Make sure notifications are enabled for Scriptable:
   - Settings → Scriptable → Notifications → Allow Notifications
2. Run the script manually first to test
3. Check that you turned OFF "Ask Before Running" in each automation

### iOS: "Too many 'Running your automation' notifications"

Go to Settings → Shortcuts → Notifications → Turn OFF

### macOS/Linux: "Command not found: python3"

Try `python` instead of `python3`

### Windows: "No module named 'win10toast'"

Run: `pip install win10toast`

### All platforms: "Failed to fetch alerts"

1. Check your internet connection
2. Verify your API key is correct
3. Make sure you're logged into hams.at

### Reset and See All Alerts Again

In the script, change:
```javascript
const RESET_MODE = false;
```
to:
```javascript
const RESET_MODE = true;
```

Run once, then change back to `false`.

---

## 📸 Example Notification

```
🆕 2 New Satellite Alerts!

SP9BE • SO-50 • EM24
  Feb 7 18:13 FM 436.795 MHz

SP9BE • RS-44 • EL98
  Feb 13 14:03 SSB
```

---

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Share your improvements

---

## 📄 License

MIT License - feel free to use and modify!

---

## 📡 Credits

- Created for the ham radio community
- Uses the [hams.at](https://hams.at) API
- Inspired by the need for real-time satellite alert notifications

---

## ❓ Support

Having issues? 
1. Check the [Troubleshooting](#-troubleshooting) section
2. Open an issue on GitHub
3. Reach out on QRZ or your preferred ham radio forum

**73!** 📻🛰️

---

## 🏷️ Tags

`ham-radio` `amateur-radio` `satellites` `notifications` `ios` `macos` `linux` `windows` `scriptable` `python` `hams-at` `satellite-tracking`

