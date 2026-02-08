#!/usr/bin/env python3
"""
HAMS.AT Alert Checker - NEW ALERTS ONLY
Sends desktop notifications when new satellite alerts appear on hams.at
"""

import requests
import json
import os
from datetime import datetime
from pathlib import Path

# Configuration
API_KEY = "PASTE YOUR API KEY HERE"
API_URL = "https://hams.at/api/alerts/upcoming"
SEEN_ALERTS_FILE = os.path.expanduser("~/.hams_seen_alerts.json")

# Set to True to reset and see all alerts again
RESET_MODE = False


def fetch_alerts():
    """Fetch upcoming alerts from hams.at API"""
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}"
        }
        response = requests.get(API_URL, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching alerts: {e}")
        return None


def get_seen_alerts():
    """Get list of alert IDs we've already notified about"""
    if RESET_MODE:
        print("RESET MODE: Clearing all seen alerts")
        return []
    
    if os.path.exists(SEEN_ALERTS_FILE):
        try:
            with open(SEEN_ALERTS_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []


def save_seen_alerts(seen_ids):
    """Save seen alert IDs to file"""
    with open(SEEN_ALERTS_FILE, 'w') as f:
        json.dump(seen_ids, f)


def clean_old_seen_alerts(seen_ids, current_alerts):
    """Keep only IDs that are still in current alerts"""
    current_ids = [alert['id'] for alert in current_alerts]
    return [alert_id for alert_id in seen_ids if alert_id in current_ids]


def format_time(iso_time):
    """Format ISO timestamp to readable format"""
    try:
        dt = datetime.fromisoformat(iso_time.replace('Z', '+00:00'))
        return dt.strftime("%b %d %H:%M")
    except:
        return ""


def send_notification(title, message):
    """Send desktop notification (cross-platform)"""
    try:
        # macOS
        if os.system("which osascript > /dev/null 2>&1") == 0:
            escaped_title = title.replace('"', '\\"')
            escaped_message = message.replace('"', '\\"')
            os.system(f'''osascript -e 'display notification "{escaped_message}" with title "{escaped_title}" sound name "default"' ''')
        
        # Linux (requires notify-send)
        elif os.system("which notify-send > /dev/null 2>&1") == 0:
            os.system(f'notify-send "{title}" "{message}"')
        
        # Windows (requires win10toast - pip install win10toast)
        else:
            try:
                from win10toast import ToastNotifier
                toaster = ToastNotifier()
                toaster.show_toast(title, message, duration=10)
            except ImportError:
                print(f"Notification: {title}\n{message}")
    except Exception as e:
        print(f"Error sending notification: {e}")
        print(f"Notification: {title}\n{message}")


def notify_new_alerts(new_alerts):
    """Send notification about new alerts"""
    if len(new_alerts) == 0:
        print("No new alerts")
        return
    
    title = f"🆕 {len(new_alerts)} New Satellite Alert{'s' if len(new_alerts) > 1 else ''}!"
    
    message_lines = []
    for i, alert in enumerate(new_alerts[:5]):
        callsign = alert.get('callsign', 'Unknown')
        satellite = alert.get('satellite', {}).get('name', '')
        grids = ', '.join(alert.get('grids', []))
        mode = alert.get('mode', '')
        frequency = f"{alert['mhz']} MHz" if alert.get('mhz') else ''
        aos_time = format_time(alert.get('aos_at', ''))
        
        line = f"{callsign}"
        if satellite:
            line += f" • {satellite}"
        if grids:
            line += f" • {grids}"
        
        details = []
        if aos_time:
            details.append(aos_time)
        if mode:
            details.append(mode)
        if frequency:
            details.append(frequency)
        
        if details:
            line += f"\n  {' '.join(details)}"
        
        message_lines.append(line)
    
    if len(new_alerts) > 5:
        message_lines.append(f"\n...and {len(new_alerts) - 5} more")
    
    message = '\n'.join(message_lines)
    
    send_notification(title, message)
    print(f"Notified about {len(new_alerts)} new alerts")


def main():
    """Main execution"""
    data = fetch_alerts()
    
    if data and 'data' in data:
        current_alerts = data['data']
        seen_ids = get_seen_alerts()
        
        # Find new alerts (ones we haven't seen before)
        new_alerts = [alert for alert in current_alerts if alert['id'] not in seen_ids]
        
        if new_alerts:
            # Notify about new alerts
            notify_new_alerts(new_alerts)
            
            # Add new alert IDs to seen list
            new_ids = [alert['id'] for alert in new_alerts]
            seen_ids.extend(new_ids)
        else:
            print("No new alerts found")
        
        # Clean up old alerts from seen list
        seen_ids = clean_old_seen_alerts(seen_ids, current_alerts)
        
        # Save updated seen list
        save_seen_alerts(seen_ids)
        
        print(f"Total alerts: {len(current_alerts)}, New: {len(new_alerts)}, Tracking: {len(seen_ids)}")
    else:
        print("Failed to fetch alerts")


if __name__ == "__main__":
    main()
