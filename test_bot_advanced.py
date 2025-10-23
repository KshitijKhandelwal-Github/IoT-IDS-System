# test_bot_advanced.py
import asyncio
import logging
import httpx
from telegram import Bot
from telegram.request import HTTPXRequest

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
_logger = logging.getLogger(__name__)

# --- PASTE YOUR CREDENTIALS HERE ---
TELEGRAM_TOKEN = "8246777701:AAGPRRczONwxjAcyHrQ5rUMteqERUtgvzAc"
CHAT_ID = "5295754598"

async def main():
    """Sends a test message with advanced options."""
    print("\n--- RUNNING ADVANCED BOT TEST ---")
    try:
        # This gives us more control over the connection
        req = HTTPXRequest()
        bot = Bot(token=TELEGRAM_TOKEN, request=req)

        print("\n--- ATTEMPTING NORMAL CONNECTION ---")
        await bot.send_message(chat_id=CHAT_ID, text="[Advanced Test] Normal connection.")
        print("\n✅ SUCCESS: Normal connection worked!")

    except Exception as e:
        print(f"\n❌ FAILED: Normal connection failed. Error: {e}")
        print("\n--- ATTEMPTING CONNECTION WITH SSL VERIFICATION DISABLED ---")
        try:
            # This is insecure, but a perfect diagnostic tool
            async with httpx.AsyncClient(verify=False) as client:
                req_no_ssl = HTTPXRequest(http_client=client)
                bot_no_ssl = Bot(token=TELEGRAM_TOKEN, request=req_no_ssl)
                await bot_no_ssl.send_message(chat_id=CHAT_ID, text="[Advanced Test] Connection with SSL verification OFF.")
                print("\n✅ SUCCESS: Connection worked only after disabling SSL verification.")
                print(">>> This confirms a CA certificate issue on the VM.")
        except Exception as e2:
            print(f"\n❌ FAILED: Connection failed even with SSL verification disabled. Error: {e2}")

if __name__ == '__main__':
    if TELEGRAM_TOKEN == "YOUR_HTTP_API_TOKEN_HERE":
        print("!!! ERROR: Please paste your Telegram token and chat ID into the script. !!!")
    else:
        asyncio.run(main())