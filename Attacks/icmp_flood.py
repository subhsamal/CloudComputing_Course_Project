#!/usr/bin/python

import os

while True:
	cmd = 'ping -c 10 -i 1 192.168.1.10'
	os.system(cmd)

