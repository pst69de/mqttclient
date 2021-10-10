# mqttclient
Scripts to install a raspberry pi zero as mqtt client with automated sensor discovery 

# Preparation
* Install a Raspberry Pi Os (Lite is sufficient) Image with rpi-imager on a microsd card
* put an ssh file (empty) to the resulting boot partition
* put a wpa_supplicant.conf with your wifi credentials to the resulting boot partition
* after start up connect user pi by ssh
* install git with sudo apt install git
* do a git clone https://github.com/pst69de/mqttclient.git
* cd mqttclient
* chmod 0744 rights.bash
* ./rights.bash
* ./install.bash
