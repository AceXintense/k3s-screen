import time
import subprocess
from board import SCL, SDA
import busio
import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import psutil
import re

DISP_OFF = 0xAE

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Clear display.
disp.rotation = 2
disp.fill(0)
disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 9)

import os
import time
import datetime
clear = lambda: os.system('clear')

tick = 0
startTime = int(time.time())
slide = 0
maxSlide = 1

def log(message):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print("[" + st + "] " + message)

while True:
    tick = (tick + 1)

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname"
    HOSTNAME =  subprocess.check_output(cmd, shell = True)
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True )

    cmd = "vcgencmd measure_temp"
    CPU_TEMPERATURE = subprocess.check_output(cmd, shell = True)
    temperature = re.search('temp=(\d+)', CPU_TEMPERATURE.decode('UTF-8')).group(1)

    hostname = HOSTNAME.decode('UTF-8').strip()
    ipAddress = IP.decode('UTF-8').strip()
    changeSlide = int(tick % 5) #If the number is divisible by 5 then it will be 0

    if (changeSlide == 0):
        if (slide < maxSlide):
            slide = (slide + 1)
        else:
            slide = 0

    # Examples of getting system information from psutil : https://www.thepythoncode.com/article/get-hardware-system-information-python#CPU_info
    CPU = "{:3.0f}".format(psutil.cpu_percent())
    svmem = psutil.virtual_memory()
    MemUsage = "{:2.0f}".format(svmem.percent)

    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    if (slide == 0):
        try:
            cmd = "kubectl describe node " + HOSTNAME.decode("utf-8")
            K8_NODE = subprocess.check_output(cmd, shell = True)
        except subprocess.CalledProcessError as e:
            print(e)

        pods = re.search('(\d) in ', K8_NODE.decode('UTF-8')).group(1)
        
        draw.text((x, top),       "NAME: " + hostname, font=font, fill=255)
        draw.text((x, top+12),    "IP  : " + ipAddress,  font=font, fill=255)
        draw.text((x, top+24),    "PODS : " + pods + " | TEMP: " + temperature + "c", font=font, fill=255)
    elif (slide == 1):             
        draw.text((x, top),       "NAME: " + hostname, font=font, fill=255)
        draw.text((x, top+12),    "IP  : " + ipAddress,  font=font, fill=255)
        draw.text((x, top+24),    "CPU : " + CPU + "% | MEM: " + MemUsage + "%", font=font, fill=255)

    log("----------")
    log("Script start time: " + str(startTime))
    log("Time: " + str(int(time.time())))
    log("Tick: " + str(tick))
    log("Change slide: " + str(changeSlide))
    log("Slide: " + str(slide))
    log("Hostname: " + hostname)
    log("CPU Temperature: " + temperature + "c")
    log("Pods: " + pods)


    
    disp.image(image)
    disp.show()
    #clear()
    time.sleep(1)
