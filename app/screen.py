import os
import adafruit_ssd1306
import busio
from PIL import Image, ImageDraw, ImageFont
from board import SCL, SDA

DISP_OFF = 0xAE

def setup(rotation = 2, fill = 0):
    global disp
    global i2c
    global width
    global height
    global padding
    global top
    global bottom
    global image
    global draw
    global font

    i2c = busio.I2C(SCL, SDA)
    disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

    # Clear display.
    disp.rotation = rotation
    disp.fill(fill)
    disp.show()

    width = disp.width
    height = disp.height
    padding = -2
    top = padding
    bottom = height - padding

    image = Image.new("1", (width, height))

    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    # font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 9)

    clear()


def clear():
    global draw
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

def draw_text(position, text):
    global draw
    draw.text(position, text, font=font, fill=255)

def render():
    global disp
    disp.image(image)
    disp.show()