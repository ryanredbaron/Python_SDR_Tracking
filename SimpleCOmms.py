# -*- coding: utf-8 -*-
"""
Created on Mon May  3 22:26:45 2021

@author: Angus
"""
import sys
import subprocess
import time
import os

os.chdir("C:\\Users\\ryanr\\Documents\\GitHub\\Python_SDR_Tracking\\WinSDR")
cmd = "dump1090.bat"
try:
    os.system("taskkill /f /im  dump1090.exe")
    print("dump1090.exe running, shutting down")
except:
    pass

AirplaneDict = {}

OverallTimer = 0

process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
while True:
    OverallTimer = OverallTimer + 1
    if OverallTimer >> 10000:
        OverallTimer = 0
    try:
        output = (process.stdout.readline()).decode()
        ParseOutput = list(filter(None, output.split(" ")))
        if output:
            #Parse output into readable
            #Flight Alt Spd HDG Lat Long
            if output.startswith("Hex"):
                continue
            if output.startswith("-----------------------------------"):
                continue
            if len(ParseOutput) == 12 and ParseOutput[0] != "(INCLUDING" and ParseOutput[0] != "OF":
                SHex = ParseOutput[0]
                SMode = ParseOutput[1]
                SSqwk = ParseOutput[2]
                SFlight = ParseOutput[3]
                try:
                    SAlt = int(ParseOutput[4])
                except:
                    SAlt = 0
                SSpd = int(ParseOutput[5])
                SHdg = int(ParseOutput[6])
                SLat = float(ParseOutput[7])
                SLong = float(ParseOutput[8])
                SSig = ParseOutput[9]
                SMsds = ParseOutput[10]
                STi = ParseOutput[11]
                
                x, y = SLat, SLong
                LandingAirport = "nan"
                AirplaneDict.update({SFlight : [LandingAirport,SAlt,SSpd,SHdg,SLat,SLong,int(time.time())]})
            if OverallTimer % 250 == 0:
                print("\033[H\033[J")
                print("------------------------Full List------------------------")
                print("{:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format('FLight #','Alt','Spd','Head','Lat','Long'))
                for k, v in AirplaneDict.items():
                    print("{:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format(k, v[1], v[2], v[3], v[4], v[5]))
                print("")
                print("")
                #Clean up dictionary
                try:
                    CleanUpAirplaneDict = AirplaneDict
                    for key, value in CleanUpAirplaneDict.items():
                        if int(time.time()) - value[6] > 10:
                            AirplaneDict.pop(key)
                except:
                    pass
    except KeyboardInterrupt:
        print('Shutting Down')
        process.kill()
        process.terminate()
        os.system("taskkill /f /im  dump1090.exe")
        sys.exit(0)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        