from PIL import Image, ImageDraw, ImageFont
import os

# Create a new image with a white background
width, height = 600, 400
img = Image.new('RGB', (width, height), color='white')
d = ImageDraw.Draw(img)

# Try to use a standard font
try:
    # For Windows
    font_path = "C:/Windows/Fonts/Arial.ttf"
    if not os.path.exists(font_path):
        # Fallback
        font = None
    else:
        font = ImageFont.truetype(font_path, 24)
except:
    font = None

# Add text to the image
title_text = "Image Placeholder"
subtitle_text = "The 'Plotting Anomalies.png' visualization"
subtitle_text2 = "is not available"

# Draw the text on the image
d.text((width/2-100, height/2-50), title_text, fill=(0, 0, 0), font=font)
d.text((width/2-180, height/2), subtitle_text, fill=(0, 0, 0), font=font)
d.text((width/2-100, height/2+50), subtitle_text2, fill=(0, 0, 0), font=font)

# Draw a border
d.rectangle([(20, 20), (width-20, height-20)], outline=(0, 0, 0), width=2)

# Save the image
img.save("images/image-placeholder.png")
