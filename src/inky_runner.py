import os,random,time,signal
from inky.auto import auto
from PIL import ImageDraw,Image 

import warnings
warnings.filterwarnings("ignore")

print("Inky.py is running")

inky_display = auto()
inky_display.set_border(inky_display.BLACK)

print(f"Resolution {inky_display.resolution}")

path = "images"
images  = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
index = 6
while True:
    filename = os.path.join(path, images[index])
    print(f"Displaying image {filename}")
    with Image.open(filename) as img:
        # resize image to display resolution
        img = img.resize(inky_display.resolution)

        inky_display.set_image(img)
        inky_display.show()
    
    index = (index + 1) % len(images)
    time.sleep(150)