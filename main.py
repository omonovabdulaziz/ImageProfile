from telethon.sync import TelegramClient
from telethon.tl import functions
from datetime import datetime
import time
import pytz

# Replace these values with your own API ID, API hash, and phone number
api_id = '26311979'
api_hash = '8f2d3c6a7f72f4210b1ede2e744ba3b8'
phone_number = '+998950960153'

# Create a new TelegramClient session
client = TelegramClient('session_name', api_id, api_hash)


async def update_name_status():
    while True:
        try:
            # Get the current time in Uzbekistan (Tashkent time)
            tz_uzbekistan = pytz.timezone('Asia/Tashkent')
            current_time = datetime.now(tz_uzbekistan).strftime("%H:%M")

            # Update your Telegram name with the current time
            await client(functions.account.UpdateProfileRequest(
                first_name=f'A. {current_time}'
            ))

            # Set your Telegram status to online
            await client(functions.account.UpdateStatusRequest(
                offline=False
            ))

            # Sleep for a short duration (adjust as needed)
            time.sleep(60)
        except Exception as e:
            print(f"An error occurred: {e}")


# Start the client
client.start()

# Run the update_name_status function in an event loop
with client:
    client.loop.run_until_complete(update_name_status())
