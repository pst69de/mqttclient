#!/usr/bin/python3

# Author Patrick O. Ehrmann (POE)
# part of the https://github.com/pst69de/mqttclient project
# licensed by GPL v3, see full license in the LICENSE (text) file of the project repository  
#
# content:
# library script class to handle an SHT3x sensor
#   SHT3x is a group of humidity and temperature sensors
#
# last changes fro newest to eldest
#
# 2021-10-10;POE;Initial code deploy

class SHT:
    def __init__(self,i2c):
        self.I2C = i2c
        from adafruit_sht31d import SHT31D
        self.device = SHT31D(self.I2C, 0x44)

        self.t=self.device.temperature
        self.rh=self.device.relative_humidity 
        
    def readvalues(self):
        self.t=self.device.temperature
        self.rh=self.device.relative_humidity 
        return '{0:0.1f}°C {1:0.1f}RH%'.format(self.t, self.rh)
        
    def publishvalues(self, mqtt, base):
        self.t=self.device.temperature
        mqtt.publish(topic=base+"/device/SHT/temperature",payload='{0:0.1f}'.format(self.t))
        self.rh=self.device.relative_humidity 
        mqtt.publish(topic=base+"/device/SHT/humidity",payload='{0:0.1f}'.format(self.rh))

