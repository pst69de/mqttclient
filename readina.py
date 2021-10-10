#!/usr/bin/python3

# Author Patrick O. Ehrmann (POE)
# part of the https://github.com/pst69de/mqttclient project
# licensed by GPL v3, see full license in the LICENSE (text) file of the project repository  
#
# content:
# help script to test INA219 device
#   TODO: migrate to use mqttINA.py library script
#
# last changes fro newest to eldest
#
# 2021-10-10;POE;Initial code deploy

from time import sleep
from ina219 import INA219

ina = INA219(shunt_ohms=0.1, max_expected_amps = 1.0, address=0x40)

ina.configure(voltage_range=ina.RANGE_32V, gain=ina.GAIN_AUTO, bus_adc=ina.ADC_128SAMP, shunt_adc=ina.ADC_128SAMP)

try:
    while 1:
        v = ina.voltage()
        i = ina.current()
        p = ina.power()
        print('{0:0.2f}V {1:0.1f}mA {2:0.2f}W'.format(v, i, p/1000))
        sleep(15)
        
except KeyboardInterrupt:
    print ("\nCtrl-C pressed.  Program exiting...")
finally:
    print ("exited")
