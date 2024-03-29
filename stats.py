# Copyright (c) 2019
# Author: Mike Paxton
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Mod Date: 06/24/19

# TODO:  Find a way to read the config file from the current directory of the python script.

from Adafruit_IO import Client
from ConfigParser import SafeConfigParser
import subprocess
import time
import os

# Uses ConfigParser to grab parameters from file
config = SafeConfigParser()
config.read('/home/pi/projects/RPi_AdafruitIO_SysStats/aio.cfg')
ADAFRUIT_IO_USERNAME = config.get('aio', 'user')
ADAFRUIT_IO_KEY = config.get('aio', 'key')
dashboard = config.get('aio', 'dashboard')
sleep = config.get('default', 'sleep')

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)


while True:

    # Shell scripts for system monitoring from here:
    # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-$
    # Added if statement to check if an external disk is attached at /dev/sda1 and if true gathers its info as Disk2
    cmd = "top -bn1 | grep load | awk '{printf \"%.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True)
    cmd = "vcgencmd measure_temp | cut -d '=' -f 2 | head --bytes -3"
    Temp = subprocess.check_output(cmd, shell=True)
    cmd = "df -h | awk '$NF==\"/\"{printf \"%.2f\", $3}'"
    Disk1 = subprocess.check_output(cmd, shell=True)
    if os.path.exists("/dev/sda1"):
        cmd = "df -h | awk '$NF==\"/data\"{printf \"%.2f\", $3}'"
        Disk2 = subprocess.check_output(cmd, shell=True)
    cmd = "free -m | awk 'NR==2{printf \"%d\", $3}'"
    Mem = subprocess.check_output(cmd, shell=True)

    # send_data grabs dashboard from config file then combines all of it into a string.
    # Each Feed must use the Feed Key not just the name of the Feed.
    # The Feed Key is in the format of dashboard.feedname
    aio.send_data(dashboard + str('.') + str('cpuload'), CPU)
    aio.send_data(dashboard + str('.') + str('cputemp'), Temp)
    aio.send_data(dashboard + str('.') + str('disk1'), Disk1)
    if os.path.exists("/dev/sda1"):
        aio.send_data(dashboard + str('.') + str('disk2'), Disk2)
    aio.send_data(dashboard + str('.') + str('memusage'), Mem)

    time.sleep(float(sleep))
