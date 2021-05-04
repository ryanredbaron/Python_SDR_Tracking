# -*- coding: utf-8 -*-
"""
Created on Mon May  3 22:26:45 2021

@author: Angus
"""
import subprocess
import os
os.chdir(os.getcwd())
cmd = "PYdump.bat"

process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
while True:
    output = process.stdout.readline()
    if output == '' and process.poll() is not None:
        break
    if output:
        print(output.decode())