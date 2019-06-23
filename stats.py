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

from Adafruit_IO import Client
from ConfigParser import SafeConfigParser
import subprocess
import time

# Uses ConfigParser to grab Adafruit IO user name and key from config file.
config = SafeConfigParser()
config.read('aio.cfg')
ADAFRUIT_IO_USERNAME = config.get('aio', 'user')
ADAFRUIT_IO_KEY = config.get('aio', 'key')


# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)


while True:

    print (ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

    cmd = "top -bn1 | grep load | awk '{printf \"%.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True)
    cmd = "free -m | awk 'NR==2{printf \"%d\", $3}'"
    Mem = subprocess.check_output(cmd, shell=True)
    cmd = "df -h | awk '$NF==\"/\"{printf \"%.2f\", $3}'"
    Disk1 = subprocess.check_output(cmd, shell=True)
    cmd = "df -h | awk '$NF==\"/data\"{printf \"%.2f\", $3}'"
    Disk2 = subprocess.check_output(cmd, shell=True)
    cmd = "vcgencmd measure_temp | cut -d '=' -f 2 | head --bytes -3"
    Temp = subprocess.check_output(cmd, shell=True)

    aio.send_data('cpuLoad', CPU)
    aio.send_data('cpuTemp', Temp)
    aio.send_data('disk1', Disk1)
    aio.send_data('disk2', Disk2)
    aio.send_data('memUsage', Mem)

    time.sleep(5)
