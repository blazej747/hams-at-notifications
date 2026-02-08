// HAMS.AT Alert Checker - NEW ALERTS ONLY
// Only sends notifications when new alerts appear

const API_KEY = "PASTE YOUR API KEY HERE";
const API_URL = "https://hams.at/api/alerts/upcoming";
const SEEN_ALERTS_KEY = "hams_seen_alerts";

// SET THIS TO true TO RESET AND SEE ALL ALERTS AGAIN
const RESET_MODE = false;

async function fetchAlerts() {
  try {
    let req = new Request(API_URL);
    req.headers = {
      "Authorization": `Bearer ${API_KEY}`
    };
    
    let response = await req.loadJSON();
    return response;
  } catch (error) {
    console.error("Error fetching alerts: " + error);
    return null;
  }
}

function getSeenAlerts() {
  if (RESET_MODE) {
    console.log("RESET MODE: Clearing all seen alerts");
    return [];
  }
  
  // Get list of alert IDs we've already notified about
  let fm = FileManager.iCloud();
  let path = fm.joinPath(fm.documentsDirectory(), SEEN_ALERTS_KEY);
  
  if (fm.fileExists(path)) {
    let data = fm.readString(path);
    return JSON.parse(data);
  }
  return [];
}

function saveSeenAlerts(seenIds) {
  let fm = FileManager.iCloud();
  let path = fm.joinPath(fm.documentsDirectory(), SEEN_ALERTS_KEY);
  fm.writeString(path, JSON.stringify(seenIds));
}

function cleanOldSeenAlerts(seenIds, currentAlerts) {
  // Keep only IDs that are still in current alerts
  // This prevents the list from growing forever
  let currentIds = currentAlerts.map(a => a.id);
  return seenIds.filter(id => currentIds.includes(id));
}

async function notifyNewAlerts(newAlerts) {
  if (newAlerts.length === 0) {
    console.log("No new alerts");
    return;
  }
  
  let notification = new Notification();
  notification.title = `🆕 ${newAlerts.length} New Satellite Alert${newAlerts.length > 1 ? 's' : ''}!`;
  
  let body = "";
  for (let i = 0; i < Math.min(newAlerts.length, 5); i++) {
    let alert = newAlerts[i];
    
    let callsign = alert.callsign || "Unknown";
    let satellite = alert.satellite ? alert.satellite.name : "";
    let grids = alert.grids && alert.grids.length > 0 ? alert.grids.join(", ") : "";
    let mode = alert.mode || "";
    let frequency = alert.mhz ? `${alert.mhz} MHz` : "";
    
    // Format time
    let aosTime = "";
    if (alert.aos_at) {
      let date = new Date(alert.aos_at);
      let dateFormatter = new DateFormatter();
      dateFormatter.dateFormat = "MMM d HH:mm";
      aosTime = dateFormatter.string(date);
    }
    
    body += `${callsign}`;
    if (satellite) body += ` • ${satellite}`;
    if (grids) body += ` • ${grids}`;
    body += "\n";
    if (aosTime) body += `  ${aosTime}`;
    if (mode) body += ` ${mode}`;
    if (frequency) body += ` ${frequency}`;
    body += "\n";
  }
  
  if (newAlerts.length > 5) {
    body += `\n...and ${newAlerts.length - 5} more`;
  }
  
  notification.body = body.trim();
  notification.sound = "default";
  
  await notification.schedule();
  console.log(`Notified about ${newAlerts.length} new alerts`);
}

// Main execution
let data = await fetchAlerts();

if (data && data.data) {
  let currentAlerts = data.data;
  let seenIds = getSeenAlerts();
  
  // Find new alerts (ones we haven't seen before)
  let newAlerts = currentAlerts.filter(alert => !seenIds.includes(alert.id));
  
  if (newAlerts.length > 0) {
    // Notify about new alerts
    await notifyNewAlerts(newAlerts);
    
    // Add new alert IDs to seen list
    let newIds = newAlerts.map(a => a.id);
    seenIds = seenIds.concat(newIds);
  } else {
    console.log("No new alerts found");
  }
  
  // Clean up old alerts from seen list
  seenIds = cleanOldSeenAlerts(seenIds, currentAlerts);
  
  // Save updated seen list
  saveSeenAlerts(seenIds);
  
  console.log(`Total alerts: ${currentAlerts.length}, New: ${newAlerts.length}, Tracking: ${seenIds.length}`);
  
} else {
  console.error("Failed to fetch alerts");
}

// Widget display
if (config.runsInWidget) {
  let widget = new ListWidget();
  widget.backgroundColor = new Color("#1c1c1e");
  
  let title = widget.addText("🛰️ HAMS.AT");
  title.textColor = Color.white();
  title.font = Font.boldSystemFont(16);
  
  widget.addSpacer(8);
  
  if (data && data.data) {
    let count = widget.addText(`${data.data.length} upcoming alerts`);
    count.textColor = Color.orange();
    count.font = Font.systemFont(14);
  } else {
    let error = widget.addText("Error loading");
    error.textColor = Color.red();
    error.font = Font.systemFont(14);
  }
  
  Script.setWidget(widget);
}

Script.complete();
