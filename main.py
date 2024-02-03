from telethon.sync import TelegramClient
from telethon.tl import functions
from datetime import datetime, timedelta
import time
from PIL import Image, ImageDraw, ImageFont
import pytz

# Replace these values with your own API ID, API hash, and phone number
api_id = '26311979'
api_hash = '8f2d3c6a7f72f4210b1ede2e744ba3b8'
phone_number = '+998950960153'

# Create a new TelegramClient session
client = TelegramClient('session_name', api_id, api_hash)


async def update_profile_photo():
    while True:
        try:
            # Get the current time in Uzbekistan (Tashkent time)
            tz_uzbekistan = pytz.timezone('Asia/Tashkent')
            current_time = datetime.now(tz_uzbekistan)
            current_time_str = current_time.strftime("%H : %M")

            img = Image.new('RGB', (400, 200), color='white')
            draw = ImageDraw.Draw(img)

            # Choose a default font size
            font_size = 20
            font = ImageFont.load_default()

            # Get the size of the text
            text = f'Hozirgi Soat : {current_time_str}'
            text_width, text_height = draw.textsize(text, font=font)

            # Center the text
            text_x = (img.width - text_width) // 2
            text_y = (img.height - text_height) // 2

            draw.text((text_x, text_y), text, font=font, fill='black')

            # Save the image locally
            img_path = 'profile_photo.png'
            img.save(img_path, format='PNG')  # Save as PNG to preserve transparency

            # Delete existing profile photos
            await client(functions.photos.DeletePhotosRequest(await client.get_profile_photos('me')))

            # Upload the new image as your profile photo
            result = await client(functions.photos.UploadProfilePhotoRequest(
                file=await client.upload_file(img_path)
            ))

            # Set user status online
            await client(functions.account.UpdateStatusRequest(offline=False))

            print(result)  # Print the result for debugging purposes

            # Sleep for a short duration (adjust as needed)
            time.sleep(60)
        except Exception as e:
            print(f"An error occurred: {e}")


# Start the client
client.start()

# Run the update_profile_photo function in an event loop
with client:
    try:
        client.loop.run_until_complete(update_profile_photo())
    except KeyboardInterrupt:
        print("Program terminated by user.")
