#!/usr/bin/python3

# Author Patrick O. Ehrmann (POE)
# part of the https://github.com/pst69de/mqttclient project
# licensed by GPL v3, see full license in the LICENSE (text) file of the project repository  
#
# content:
# help script to find predecessor script execution and hang it up 
#   helpful when using crontab as executioner (hourly restart is proposed) 
#
# last changes fro newest to eldest
#
# 2021-10-10;POE;Initial code deploy

import os
import signal
import psutil

for proc in psutil.process_iter(['pid', 'name', 'username', 'cmdline']):
    if proc.info['name'] == 'mqttclient.py': 
        print(proc.info)
        #proc.terminate()
        if proc.info['pid'] != os.getpid():
            os.kill(proc.info['pid'],signal.SIGHUP)
            print("Dieser war's")
