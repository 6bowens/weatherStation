#!/bin/bash

/bin/sleep 10
/usr/bin/python3 /home/pi/weatherStation/main.py &
/usr/bin/python3 /home/pi/weatherStation/web.py &

