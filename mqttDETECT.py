#!/usr/bin/python3

# Author Patrick O. Ehrmann (POE)
# part of the https://github.com/pst69de/mqttclient project
# licensed by GPL v3, see full license in the LICENSE (text) file of the project repository
#
# content:
# library script class to detect by i2c toolset
#
# last changes fro newest to eldest
#
# 2021-10-15;POE;Initial code deploy

class I2CDEV:
    def __init__(self):
        import os
        import subprocess
        import re
        p = subprocess.Popen(['i2cdetect', '-y','1'],stdout=subprocess.PIPE,)
        alldev = ''
        for i in range(0,9):
            line = str(p.stdout.readline())
            #print(line)
            if (i > 0):
                alldev += line[6:54]
        #print(alldev)
        self.splice = [alldev[i:i+3] for i in range(0, len(alldev),3)]

    def isdev(self,num):
        return ('{0:2x} '.format(num) == self.splice[num])

