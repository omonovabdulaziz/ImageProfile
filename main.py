from telethon.sync import TelegramClient
from telethon.tl import functions
from datetime import datetime
import time
from PIL import Image, ImageDraw, ImageFont
import io
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
            current_time = datetime.now(tz_uzbekistan).strftime("%H:%M")

            # Create an image with the current time
            img = Image.new('RGB', (400, 200), color='white')
            d = ImageDraw.Draw(img)

            # Choose a smaller font size and center the text
            font_size = 20
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            font = ImageFont.truetype(font_path, font_size)

            text_width, text_height = d.textsize(f'Current Time: {current_time}', font=font)
            text_x = (img.width - text_width) // 2
            text_y = (img.height - text_height) // 2

            d.text((text_x, text_y), f'Current Time: {current_time}', font=font, fill='black')

            # Save the image locally
            img_path = 'profile_photo.png'
            img.save(img_path, format='PNG')  # Save as PNG to preserve transparency

            # Delete existing profile photos
            await client(functions.photos.DeletePhotosRequest(await client.get_profile_photos('me')))

            # Upload the new image as your profile photo
            result = await client(functions.photos.UploadProfilePhotoRequest(
                file=await client.upload_file(img_path)
            ))

            print(result)  # Print the result for debugging purposes

            # Sleep for a short duration (adjust as needed)
            time.sleep(60)
        except Exception as e:
            print(f"An error occurred: {e}")


# Start the client
client.start()

# Run the update_profile_photo function in an event loop
with client:
    client.loop.run_until_complete(update_profile_photo())
