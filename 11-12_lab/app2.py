import os
import requests
import sys
import configparser
from PIL import Image, ImageDraw, ImageFont

# Define a function to download the first image of a book from the Project Gutenberg website
def download_first_image(book_id: str):
    # Construct the URL of the image
    img_url = (
        f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.cover.medium.jpg"
    )
    # Send a GET request to the URL to download the image
    img_response = requests.get(img_url)
    # Check if the response status code is 200 (OK)
    if img_response.status_code == 200:
        # Get the filename of the image from the URL
        filename = os.path.basename(img_url)
        # Save the image to a file
        with open(filename, "wb") as f:
            f.write(img_response.content)
        print(f"Downloaded image to {filename}")
    else:
        print("No images found")


# Define a function to process an image by cropping it, resizing it and adding a watermark to it
def process_image():
    # Read the configuration file to get the settings for processing the image
    config = configparser.ConfigParser()
    config.read("config.ini")
    filename = config.get("settings", "filename")
    crop_factor = config.getfloat("settings", "crop_factor")
    resize_factor = config.getfloat("settings", "resize_factor")
    watermark_text = config.get("settings", "watermark_text")

    # Open the image using PIL
    with Image.open(filename) as img:
        # Crop the image by calculating the new dimensions and coordinates based on the crop factor
        width, height = img.size
        new_width = int(width * crop_factor)
        new_height = int(height * crop_factor)
        left = (width - new_width) // 2
        top = (height - new_height) // 2
        right = (width + new_width) // 2
        bottom = (height + new_height) // 2
        img = img.crop((left, top, right, bottom))

        # Resize the image by calculating the new dimensions based on the resize factor
        new_width = int(new_width * resize_factor)
        new_height = int(new_height * resize_factor)
        img = img.resize((new_width, new_height), Image.ANTIALIAS)

        # Add a watermark to the image by drawing text on it using PIL's ImageDraw and ImageFont modules
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 16)
        text_width, text_height = draw.textsize(watermark_text, font)
        x = 0
        y = new_height - text_height - 5
        draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255))

        # Save the processed image to a file with a filename that includes the word "processed"
        processed_filename = f"processed_{filename}"
        img.save(processed_filename)
        print(f"Saved processed image to {processed_filename}")


# Run the download_first_image and process_image functions when the script is executed and a book ID is provided as a command line argument
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a book identifier.")
        sys.exit(1)
    book_id = sys.argv[1]
    download_first_image(book_id)
    process_image()
