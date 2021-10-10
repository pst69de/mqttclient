#!/usr/bin/python3

# Author Patrick O. Ehrmann (POE)
# part of the https://github.com/pst69de/mqttclient project
# licensed by GPL v3, see full license in the LICENSE (text) file of the project repository  
#
# content:
# library script class to handle an BH1750 sensor
#   BH1750 is a light intensity (illuminance) detecting sensor 
#
# last changes fro newest to eldest
#
# 2021-10-10;POE;Initial code deploy

class BH:
    def __init__(self,i2c):
        self.I2C = i2c
        from adafruit_bh1750 import BH1750
        self.device = BH1750(self.I2C)

        self.lux=self.device.lux
        
    def readvalues(self):
        self.lux=self.device.lux
        return '{0}lux'.format(self.lux)
        
    def publishvalues(self, mqtt, base):
        self.lux=self.device.lux
        mqtt.publish(topic=base+"/device/BH/illuminance",payload='{0:0.2f}'.format(self.lux))

