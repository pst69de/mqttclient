#!/usr/bin/python3

# Author Patrick O. Ehrmann (POE)
# part of the https://github.com/pst69de/mqttclient project
# licensed by GPL v3, see full license in the LICENSE (text) file of the project repository  
#
# content:
# help script to test a SHT3x device
#   TODO: migrate to use mqttSHT.py library script
#
# last changes fro newest to eldest
#
# 2021-10-10;POE;Initial code deploy

from time import sleep
from board import SCL,SDA
from busio import I2C
from adafruit_sht31d import SHT31D

i2c = I2C(SCL, SDA)
sht = SHT31D(i2c, 0x44)

try:
    while 1:
        t = sht.temperature
        rh = sht.relative_humidity
        print('{0:0.1f} °C {1:0.1f} RH%'.format(t, rh))
        sleep(5)
        
except KeyboardInterrupt:
    print ("\nCtrl-C pressed.  Program exiting...")
finally:
    print ("exited")
