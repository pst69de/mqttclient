#!/usr/bin/python3

# Author Patrick O. Ehrmann (POE)
# part of the https://github.com/pst69de/mqttclient project
# licensed by GPL v3, see full license in the LICENSE (text) file of the project repository  
#
# content:
# help script to switch off (do low) on project standard port 4 (GPIO 8)
#
# last changes fro newest to eldest
#
# 2021-10-10;POE;Initial code deploy

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(8, GPIO.OUT)

GPIO.output(8, GPIO.LOW)

