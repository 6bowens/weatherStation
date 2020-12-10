#!/usr/bin/env python

import os
import blynklib
import time
import datetime
import time
import random

#blynk setup
from config import * # pull in blynk credentials
blynk = blynklib.Blynk(BLYNK_AUTH, server=server, port=port, heartbeat=60)

#vars
pubDur = 5
lastTime = 0
airTemp = 10
testVar = 0
waterTemp = 15
hum = 25

try:
 while True:
    blynk.run()

    airTemp = random.randint(10, 30)
    waterTemp = random.randint(10, 35)
    hum = random.randint(0, 100)

    blynk.virtual_write(1, airTemp)
    blynk.virtual_write(2, waterTemp)
    blynk.virtual_write(3, hum)

    lastTime = time.time() #reset pub interval
    print ('Publishing Temps')
    print (testVar)
    print (airTemp)

    time.sleep(60)

except KeyboardInterrupt:
	print('Exiting from ctrl c')
