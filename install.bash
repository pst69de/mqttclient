#!/usr/bin/bash

# Author Patrick O. Ehrmann (POE)
# part of the https://github.com/pst69de/mqttclient project
# licensed by GPL v3, see full license in the LICENSE (text) file of the project repository  
#
# content:
# installation help script 
#   update system
#   install all components needed
#
# last changes fro newest to eldest
#
# 2021-10-10;POE;Initial code deploy

echo first step: change password, enable SSH, enable I2C 
echo do reboot at end of script run 
read -n 1 -s -r -p "Press a key to continue"
sudo raspi-config
echo update raspi 
read -n 1 -s -r -p "Press a key to continue"
sudo apt update
echo upgrade raspi 
read -n 1 -s -r -p "Press a key to continue"
sudo apt upgrade
echo install tools and python 
read -n 1 -s -r -p "Press a key to continue"
sudo apt install i2c-tools -y
sudo apt install python3-pip -y
pip3 install paho-mqtt
pip3 install psutil
pip3 install adafruit-circuitpython-ina219
pip3 install adafruit-circuitpython-sht31d
pip3 install adafruit-circuitpython-bh1750
pip3 install adafruit-circuitpython-ads1x15
#
echo install postfix as mail processor 
echo use a satellite system with FQDN as local host description and provide a,n internal, relay host
read -n 1 -s -r -p "Press a key to continue"
sudo apt install postfix -y
echo check postfix configuration 
read -n 1 -s -r -p "Press a key to continue"
sudo vi /etc/postfix/main.cf
chmod 0744 *.py
echo edit crontab 
echo with MAILTO: address
echo and job entry:
echo "00 *	* * *	pi	/home/pi/mqttclient/mqttclient.py"
read -n 1 -s -r -p "Press a key to continue"
sudo vi /etc/crontab
echo edit configuration mqttconnect.json file 
read -n 1 -s -r -p "Press a key to continue"
sudo vi mqttconnect.json
sudo reboot
