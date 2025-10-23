# test_bot.py (Asynchronous Version)
import telegram
import asyncio # <<< NEW: Import the asyncio library

# Paste your credentials here
TELEGRAM_TOKEN = "8246777701:AAGPRRczONwxjAcyHrQ5rUMteqERUtgvzAc"
CHAT_ID = "5295754598"

# <<< CHANGED: The main logic is now in an 'async' function
async def main():
    """Asynchronously sends the test message."""
    print("Attempting to send a test message...")
    try:
        bot = telegram.Bot(token=TELEGRAM_TOKEN)
        # <<< CHANGED: We now 'await' the result of the send_message command
        await bot.send_message(chat_id=CHAT_ID, text="Hello! This is a test from the VM.")
        print("✅ Success! The message was sent. Check your Telegram.")
    except Exception as e:
        print(f"❌ Failure! An error occurred: {e}")

if __name__ == '__main__':
    # <<< CHANGED: We run the main async function using asyncio.run()
    asyncio.run(main())
