#!/usr/bin/python3

# Author Patrick O. Ehrmann (POE)
# part of the https://github.com/pst69de/mqttclient project
# licensed by GPL v3, see full license in the LICENSE (text) file of the project repository  
#
# content:
# library script class to handle an ADS1x15 sensor
#   ADS1x15 is a group of ADC sensors 
#
# last changes fro newest to eldest
#
# 2021-10-10;POE;Initial code deploy

class ADS:
    def __init__(self,i2c):
        self.I2C = i2c
        #from adafruit_ads1x15 import ads1015 as ADS
        from adafruit_ads1x15 import ads1115 as ADS
        from adafruit_ads1x15.analog_in import AnalogIn
        #self.device = ADS.ADS1015(self.I2C)
        self.device = ADS.ADS1115(self.I2C)
        # +/- 2.048v 
        self.device.gain = 2 
        self.device.mode = ADS.Mode.SINGLE
        self.ch1 = AnalogIn(self.device, ADS.P0)
        self.ch2 = AnalogIn(self.device, ADS.P1)
        self.ch3 = AnalogIn(self.device, ADS.P2)
        self.ch4 = AnalogIn(self.device, ADS.P3)
        self.v1  = self.ch1.voltage
        self.v2  = self.ch2.voltage
        self.v3  = self.ch3.voltage
        self.v4  = self.ch4.voltage

        
    def readvalues(self):
        self.v1  = self.ch1.voltage
        self.v2  = self.ch2.voltage
        self.v3  = self.ch3.voltage
        self.v4  = self.ch4.voltage
        return '{0:0.3f}V {1:0.3f}V {2:0.3f}V {3:0.3f}V '.format(self.v1,self.v2,self.v3,self.v4)
        
    def publishvalues(self, mqtt, base):
        self.v1  = self.ch1.voltage
        mqtt.publish(topic=base+"/device/ADS/v1",payload='{0:0.3f}'.format(self.v1))
        self.v2  = self.ch2.voltage
        mqtt.publish(topic=base+"/device/ADS/v2",payload='{0:0.3f}'.format(self.v2))
        self.v3  = self.ch3.voltage
        mqtt.publish(topic=base+"/device/ADS/v3",payload='{0:0.3f}'.format(self.v3))
        self.v4  = self.ch4.voltage
        mqtt.publish(topic=base+"/device/ADS/v4",payload='{0:0.3f}'.format(self.v4))

