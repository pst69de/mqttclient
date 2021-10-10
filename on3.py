#!/usr/bin/python3

# Author Patrick O. Ehrmann (POE)
# part of the https://github.com/pst69de/mqttclient project
# licensed by GPL v3, see full license in the LICENSE (text) file of the project repository  
#
# content:
# help script to switch on (do high) on project standard port 3 (GPIO 7)
#
# last changes fro newest to eldest
#
# 2021-10-10;POE;Initial code deploy

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(7, GPIO.OUT)

GPIO.output(7, GPIO.HIGH)

