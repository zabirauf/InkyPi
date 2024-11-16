import os,random,time,signal
from inky.auto import auto
from PIL import ImageDraw,Image 

print("Inky.py is running")

inky_display = auto(ask_user=True, verbose=True)
inky_display.set_border(inky_display.BLACK)

filename = "images/sample.jpg"
with Image.open(filename) as img:
    # resize image to display resolution
    img = img.resize(inky_display.resolution)

    inky_display.set_image(img)
    inky_display.show()