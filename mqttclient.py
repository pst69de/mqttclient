#!/usr/bin/python3

# Author Patrick O. Ehrmann (POE)
# part of the https://github.com/pst69de/mqttclient project
# licensed by GPL v3, see full license in the LICENSE (text) file of the project repository  
#
# content:
# mqtt client base script
#   configuration by mqttconnect.json 
#   imports mqttINA.py if needed for handling INA219 sensors
#   imports mqttSHT.py if needed for handling SHT3x sensors
#   imports mqttBH.py if needed for handling BH1750 sensors
#   imports mqttADS.py if needed for handling ADS1x15 sensors
#
# last changes fro newest to eldest
#
# 2021-10-10;POE;Initial code deploy

from RPi import GPIO as GPIO
import time as time
from time import sleep

from board import SCL,SDA
from busio import I2C

from paho.mqtt import client as mqtt
from paho.mqtt import subscribe as subscribe

import os
import socket
import signal
import psutil
import json

PORTOUT1 = 5
PORTOUT2 = 6
PORTOUT3 = 7
PORTOUT4 = 8
MQTT = "mqtt-server.domain.tld"
USERNAME = "USERNAME"
PASSWORD = "PASSWORD"
# load configuration here
with open('mqttconnect.json') as f:
    d = json.load(f)
    MQTT = d["HOST"]
    USERNAME = d["USERNAME"]
    PASSWORD = d["PASSWORD"]
print( 'HOST {0} USERNAME {1}'.format(MQTT,USERNAME))
CLIENTNAME = socket.gethostname()
CHECKI2CDEVICES = { 0x40: "mqttINA", 0x44: "mqttSHT", 0x23:"mqttBH", 0x48:"mqttADS"}
DEVICES = []

# Hup predecessor
for proc in psutil.process_iter(['pid', 'name', 'username', 'cmdline']):
    if proc.info['name'] == 'mqttclient4.py': 
        print(proc.info)
        #proc.terminate()
        if proc.info['pid'] != os.getpid():
            os.kill(proc.info['pid'],signal.SIGHUP)
            print("Hup'ed")

# init timing
tick = 5
endtime = 3595
#endtime = 55 #... testing
nextstep = 0
starttime = time.time()

# var inits (GPIO)
sw1="OFF"
sw2="OFF"
sw3="OFF"
sw4="OFF"

# GPIO configuration
GPIO.setmode(GPIO.BCM)
# GPIO5 is our switch port 1 (output)
GPIO.setup(PORTOUT1, GPIO.OUT)
if GPIO.input(PORTOUT1) == 0:
    sw1="OFF"
else:
    sw1="ON"
print("GPIO 1 init %s on %i" % (sw1,PORTOUT1))
# GPIO6 is our switch port 2 (output)
GPIO.setup(PORTOUT2, GPIO.OUT)
if GPIO.input(PORTOUT2) == 0:
    sw2="OFF"
else:
    sw2="ON"
print("GPIO 2 init %s on %i" % (sw2,PORTOUT2))
# GPIO7 is our switch port 4 (output)
GPIO.setup(PORTOUT3, GPIO.OUT)
if GPIO.input(PORTOUT3) == 0:
    sw3="OFF"
else:
    sw3="ON"
print("GPIO 3 init %s on %i" % (sw3,PORTOUT3))
# GPIO8 is our switch port 4 (output)
GPIO.setup(PORTOUT4, GPIO.OUT)
if GPIO.input(PORTOUT4) == 0:
    sw4="OFF"
else:
    sw4="ON"
#GPIO.output(PORTOUT, GPIO.LOW)
print("GPIO 4 init %s on %i" % (sw4,PORTOUT4))

# https://learn.adafruit.com/circuitpython-basics-i2c-and-spi/i2c-devices
# get i2c devices
i2c = I2C(SCL, SDA)
# [hex(x) for x in i2c.scan()]
for dev in i2c.scan():
    if dev in CHECKI2CDEVICES.keys():
        print('{0} in DEVICES {1}'.format(hex(dev),CHECKI2CDEVICES[dev]))
        if CHECKI2CDEVICES[dev] == "mqttINA":
            from mqttINA import INA
            DEVICES.append(INA(i2c))
        if CHECKI2CDEVICES[dev] == "mqttBH":
            from mqttBH import BH
            DEVICES.append(BH(i2c))
        if CHECKI2CDEVICES[dev] == "mqttSHT":
            from mqttSHT import SHT
            DEVICES.append(SHT(i2c))
            #pass
        if CHECKI2CDEVICES[dev] == "mqttADS":
            from mqttADS import ADS
            DEVICES.append(ADS(i2c))
            #pass
    else:
        print('{0} unknown device'.format(hex(dev)))

# initial values print
print('@ {0} {1} {2} {3} {4}'.format(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()), sw1, sw2, sw3, sw4))
for dev in DEVICES:
    print(dev.readvalues())

# MQTTclient connection subroutine
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(CLIENTNAME+"/device/#")

# MQTTclient messaging subroutine
def on_message(client, userdata, message):
    global sw1,sw2,sw3,sw4,GPIO
    #print("message topic=",message.topic)
    #print("message received " ,str(message.payload.decode("utf-8")))
    if message.topic==CLIENTNAME+"/device/switch/switch1":
        newsw=str(message.payload.decode("utf-8"))
        if sw1!=newsw:
            if newsw=="ON":
                GPIO.output(PORTOUT1, GPIO.HIGH)
            if newsw=="OFF":
                GPIO.output(PORTOUT1, GPIO.LOW)
        sw1=str(message.payload.decode("utf-8"))
    if message.topic==CLIENTNAME+"/device/switch/switch2":
        newsw=str(message.payload.decode("utf-8"))
        if sw2!=newsw:
            if newsw=="ON":
                GPIO.output(PORTOUT2, GPIO.HIGH)
            if newsw=="OFF":
                GPIO.output(PORTOUT2, GPIO.LOW)
        sw2=str(message.payload.decode("utf-8"))
    if message.topic==CLIENTNAME+"/device/switch/switch3":
        newsw=str(message.payload.decode("utf-8"))
        if sw3!=newsw:
            if newsw=="ON":
                GPIO.output(PORTOUT3, GPIO.HIGH)
            if newsw=="OFF":
                GPIO.output(PORTOUT3, GPIO.LOW)
        sw3=str(message.payload.decode("utf-8"))
    if message.topic==CLIENTNAME+"/device/switch/switch4":
        newsw=str(message.payload.decode("utf-8"))
        if sw4!=newsw:
            if newsw=="ON":
                GPIO.output(PORTOUT4, GPIO.HIGH)
            if newsw=="OFF":
                GPIO.output(PORTOUT4, GPIO.LOW)
        sw4=str(message.payload.decode("utf-8"))
    #print("message qos=",message.qos)
    #print("message retain flag=",message.retain)

# MQTTclient configuration 
client = mqtt.Client(client_id=CLIENTNAME, clean_session=True, protocol=mqtt.MQTTv311, transport="tcp")
client.on_connect=on_connect
client.on_message=on_message
client.username_pw_set( username=USERNAME, password=PASSWORD)

# finally connect the client 
print("connect client")
client.connect( host=MQTT, port=1883, keepalive=60, bind_address="")

client.loop_start()
try:
    while 1:
        nextstep += tick
        for dev in DEVICES:
            dev.publishvalues(mqtt=client, base=CLIENTNAME)
        client.publish(topic=CLIENTNAME+"/device/switch/switch1",payload='{0}'.format(sw1))
        client.publish(topic=CLIENTNAME+"/device/switch/switch2",payload='{0}'.format(sw2))
        client.publish(topic=CLIENTNAME+"/device/switch/switch3",payload='{0}'.format(sw3))
        client.publish(topic=CLIENTNAME+"/device/switch/switch4",payload='{0}'.format(sw4))
        if nextstep>endtime:
            raise Exception("End of Script time")
        while time.time() < starttime + nextstep:
            sleep(0.1)
        
except KeyboardInterrupt:
    print ("\nCtrl-C pressed.  Program exiting...")
finally:
    client.loop_stop()
    # exit values print
    print('@ {0} {1} {2} {3} {4}'.format(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()), sw1, sw2, sw3, sw4))
    for dev in DEVICES:
        print(dev.readvalues())
    print ("exited")
