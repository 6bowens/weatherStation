import Adafruit_DHT
import os
import glob
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

RST = None
DC = 23
SPI_PORT = 0  # setting  i2c settings
SPI_DEVICE = 0

disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST) # define the display

os.system('modprobe w1-gpio') #initialize 1 wire temp
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave' #ref temp location

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 27            # BCM PIN (Board Pin is 13)
DSB_PIN = 17            # BCM PIN (Board Pin is 11)

#Prep display
disp.begin() #init display
disp.clear()
disp.display() # wipe display
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)
padding = -2
top = padding
bottom = height-padding
x = 0
font = ImageFont.load_default()

#query  IP for display
cmd = "hostname -I | cut -d\' \' -f1"
IP = subprocess.check_output(cmd, shell = True )

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c

while True:
    airHum, airTemp = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    waterTemp = read_temp()

    if airHum is not None and airTemp is not None and waterTemp is not None:
        print("WaterTemp={0:0.1f}*C CaseTemp={1:0.1f}*C CaseHum={2:0.1f}%".format(waterTemp, airTemp, airHum))
    else:
        print("Failed to retrieve data from humidity sensor")

    # Write lines of text.
    draw.text((x, top),       "      ",  font=font, fill=255)
    draw.text((x, top+8),     "Air Temp:   %9.1f" % airTemp, font=font, fill=255)
    draw.text((x, top+16),    "Air Hum:    %9.1f" % airHum, font=font, fill=255)
    draw.text((x, top+25),    "Water Temp: %9.1f" % waterTemp, font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()

    #sleep for a sec
    time.sleep(1)
