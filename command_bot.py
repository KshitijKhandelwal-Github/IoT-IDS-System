# command_bot.py (v3 - Graceful Shutdown)
import os, telegram, asyncio
from telegram.ext import Application, CommandHandler

# --- PASTE YOUR CREDENTIALS HERE ---
TELEGRAM_TOKEN = "YOUR_HTTP_API_TOKEN_HERE"
ALERT_LOG_FILE = 'logs/attack.log'
COORDINATION_FILE = 'coordination.log'

async def get_logs(update, context):
    # Sends the last 25 lines of the attack log.
    print(f"Received /getlogs command from user {update.effective_chat.id}")
    try:
        if not os.path.exists(ALERT_LOG_FILE):
            await update.message.reply_text("Log file does not exist yet.")
            return
        with open(ALERT_LOG_FILE, 'r') as f: lines = f.readlines()
        if not lines:
            await update.message.reply_text("The attack log is currently empty.")
            return
        last_logs = "".join(lines[-25:])
        message = f"📜 *Last 25 lines of attack.log:*\n\n```\n{last_logs}\n```"
        await update.message.reply_text(message, parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")

async def get_status(update, context):
    # Checks and reports the status of the honeypot devices.
    print(f"Received /status command from user {update.effective_chat.id}")
    plug_status = "🔴 OFFLINE"
    if os.path.exists(COORDINATION_FILE):
        with open(COORDINATION_FILE, 'r') as f:
            for line in f:
                if "plug_1_power:ON" in line:
                    plug_status = "🟢 ONLINE"; break
    camera_status = plug_status
    status_message = (f"🩺 *Honeynet Status* 🩺\n\n*Smart Plug:* {plug_status}\n*Smart Camera:* {camera_status}")
    await update.message.reply_text(status_message, parse_mode='Markdown')


async def main():
    """Sets up and runs the Telegram command bot with a graceful shutdown."""
    print("--- Command Bot is starting up ---")
    
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("getlogs", get_logs))
    application.add_handler(CommandHandler("status", get_status))

    try:
        await application.initialize()
        await application.updater.start_polling()
        await application.start()
        print("--- Bot is now running. Press Ctrl-C to stop. ---")
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped by user.")
    finally:
        print("--- Shutting down bot ---")
        if application.updater.running:
            await application.updater.stop()
        if application.running:
            await application.stop()
        await application.shutdown()
        print("--- Bot shutdown complete ---")

if __name__ == '__main__':
    if TELEGRAM_TOKEN == "YOUR_HTTP_API_TOKEN_HERE":
        print("!!! ERROR: Please paste your credentials.")
    else:
        asyncio.run(main())