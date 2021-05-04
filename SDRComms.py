# -*- coding: utf-8 -*-
"""
Created on Mon May  3 22:26:45 2021

@author: Angus
"""
import sys
import subprocess
import os
os.chdir(os.getcwd()+"//WinSDR")
cmd = "PYdump.bat"

AirplaneDict = {}

process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
while True:
    try:
        output = (process.stdout.readline()).decode()
        ParseOutput = output.split(" ")
        if output:
            #Parse output into readable
            #Flight Alt Spd HDG Lat Long
            if output.startswith("Hex"):
                continue
            if output.startswith("-----------------------------------"):
                continue
            print(output)
            #print(ParseOutput)
            print(len(ParseOutput))
            try:
                #print(ParseOutput[4])
                #print(ParseOutput[5])
                #print(ParseOutput[6])
                #print(ParseOutput[7])
                #print(ParseOutput[8])
                pass
            except:
                pass
            
    except KeyboardInterrupt:
        print('Shutting Down')
        process.kill()
        process.terminate()
        os.system("taskkill /f /im  dump1090.exe")
        sys.exit(0)