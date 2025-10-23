# telegram_alerter.py (v15 - Fixed Order)
import time, os, telegram, asyncio
from datetime import datetime, timedelta

# --- PASTE YOUR CREDENTIALS HERE ---
TELEGRAM_TOKEN = "YOUR_HTTP_API_TOKEN_HERE"
CHAT_ID = "YOUR_CHAT_ID"
ALERT_LOG_FILE = 'logs/attack.log'

# --- IDS CONFIGURATION ---
DEVICE_CONTACT_THRESHOLD = 2 
TIME_WINDOW_SECONDS = 5 # Set a shorter "memory" for attackers
attackers = {}

async def send_alert(message):
    try:
        bot = telegram.Bot(token=TELEGRAM_TOKEN)
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown')
        print(f"--> Alert sent: {message.splitlines()[0]}")
    except Exception as e:
        print(f"!!! Failed to send alert: {e} !!!")

# <<< CHANGED: This function is now async
async def process_log_block(block):
    """Parses a log block and sends alerts sequentially."""
    details = {key.strip(): value.strip() for line in block.strip().split('\n') if ':' in line for key, value in [line.split(':', 1)]}
    
    attacker_ip = details.get("Attacker IP")
    device_info = details.get("Device")
    log_details = details.get("Details", "")
    if not attacker_ip or not device_info: return

    device_type = device_info.split('(')[0].strip()
    now = datetime.now()

    if attacker_ip not in attackers:
        # alert_level: 0=none, 1=connection, 2=scan, 3=exploit
        attackers[attacker_ip] = {'last_seen': now, 'contacted_hosts': set(), 'alert_level': 0}
    
    attackers[attacker_ip]['last_seen'] = now
    attackers[attacker_ip]['contacted_hosts'].add(device_type)
    state = attackers[attacker_ip]

    # <<< CHANGED: Reverted to if/elif logic and 'await' to guarantee order
    
    # LEVEL 3: Exploit Attempt
    if "command: 'off'" in log_details and state['alert_level'] < 3:
        state['alert_level'] = 3
        alert_message = (f"🔥 *Exploit Attempt Detected* 🔥\n\n*Source IP:* `{attacker_ip}`\n*Action:* Sent 'off' command to the Smart Plug.")
        await send_alert(alert_message)

    # LEVEL 2: Suspicious Scan
    elif len(state['contacted_hosts']) >= DEVICE_CONTACT_THRESHOLD and state['alert_level'] < 2:
        state['alert_level'] = 2
        contacted_devices_str = ", ".join(sorted(list(state['contacted_hosts'])))
        alert_message = (f"⚠️ *Suspicious Scan Detected* ⚠️\n\n*Source IP:* `{attacker_ip}`\n*Activity:* Scanned multiple devices ({contacted_devices_str}).")
        await send_alert(alert_message)

    # LEVEL 1: New Connection
    elif state['alert_level'] < 1:
        state['alert_level'] = 1
        alert_message = (f"ℹ️ *New Connection Detected*\n\n*Source IP:* `{attacker_ip}`\n*Target:* {device_type}")
        await send_alert(alert_message)

def cleanup_old_attackers():
    now = datetime.now()
    old_attackers = [ip for ip, data in attackers.items() if now - data['last_seen'] >= timedelta(seconds=TIME_WINDOW_SECONDS)]
    for ip in old_attackers:
        del attackers[ip]
        print(f"Cleaned up old entry for IP: {ip}")

async def main():
    """Main loop to watch the log file and process entries."""
    print(f"--- Ordered IDS Alerter is running (Timeout: {TIME_WINDOW_SECONDS}s) ---")
    last_position, incomplete_block = 0, ""
    while True:
        try:
            if not os.path.exists(ALERT_LOG_FILE):
                await asyncio.sleep(2); continue
            with open(ALERT_LOG_FILE, 'r') as logfile:
                logfile.seek(last_position); new_content = logfile.read(); last_position = logfile.tell()
            if new_content:
                full_buffer = incomplete_block + new_content
                alerts = full_buffer.split('---')
                incomplete_block = alerts.pop(-1)
                for alert_block in alerts:
                    if alert_block.strip():
                        # <<< CHANGED: We now 'await' the processing function
                        await process_log_block(alert_block)
            cleanup_old_attackers()
            await asyncio.sleep(1)
        except Exception as e:
            print(f"An error occurred in the main loop: {e}"); await asyncio.sleep(5)

if __name__ == '__main__':
    if TELEGRAM_TOKEN == "YOUR_HTTP_API_TOKEN_HERE":
        print("!!! ERROR: Please paste your credentials.")
    else:
        asyncio.run(main())