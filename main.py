import Adafruit_DHT
import os
import glob
import time
import datetime
import subprocess

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

#oled defs
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#webserver defs
from flask import Flask, render_template

#Display definitions
RST = None
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# define temp sensor mount point
os.system('modprobe w1-gpio') 
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave' #ref temp location

#temp sensor defs
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 27  # BCM PIN (Board Pin is 13)
DSB_PIN = 17  # BCM PIN (Board Pin is 11)
airTemp = 0
airHum = 0
waterTemp = 0

#Prep display
disp.begin()
disp.clear()
disp.display()
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

#read dsb temps
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

#convert dsp temps
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

#main loop
while True:
    #get temps & time
    airHum, airTemp = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    waterTemp = read_temp()
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    #dump temps to console
    if airHum is not None and airTemp is not None and waterTemp is not None:
        print("Water Temp={0:0.1f}*C Air Temp={1:0.1f}*C Air Hum={2:0.1f}%".format(waterTemp, airTemp, airHum))
    else:
        print("Failed to retrieve data from humidity sensor")

    # Display data on oled
    draw.text((x, top),       timeString,  font=font, fill=255)
    draw.text((x, top+8),     "Air Temp:   %9.1f" % airTemp, font=font, fill=255)
    draw.text((x, top+16),    "Air Hum:    %9.1f" % airHum, font=font, fill=255)
    draw.text((x, top+25),    "Water Temp: %9.1f" % waterTemp, font=font, fill=255)

    # Display image (box)
    disp.image(image)
    disp.display()

    #write values to file
    file = open("data.txt", "w+")
    file.write("%2.1f\n" % airTemp)
    file.write("%2.1f\n" % airHum)
    file.write("%2.1f\n" % waterTemp)
    file.write(timeString)
    file.close()

    #sleep for a sec
    time.sleep(10)
