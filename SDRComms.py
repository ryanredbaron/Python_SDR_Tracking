# -*- coding: utf-8 -*-
"""
Created on Mon May  3 22:26:45 2021

@author: Angus
"""
import sys
import subprocess
import time
import os
import pprint

os.chdir(os.getcwd()+"//WinSDR")
cmd = "PYdump.bat"
os.system("taskkill /f /im  dump1090.exe")

AirplaneDict = {}
pp = pprint.PrettyPrinter(depth=10)

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
                SAlt = int(ParseOutput[4])
                SSpd = int(ParseOutput[5])
                SHdg = int(ParseOutput[6])
                SLat = float(ParseOutput[7])
                SLong = float(ParseOutput[8])
                SSig = ParseOutput[9]
                SMsds = ParseOutput[10]
                STi = ParseOutput[11]
                #https://boundingbox.klokantech.com/
                LandingAirport = "-"
                x, y = SLat, SLong
                #--------------Long Beach Landing Box--------------
                y1 , x1 , y2 , x2 = -118.168339,33.669071,-117.997795,33.815526
                if (x > x1 and x < x2 and y > y1 and y < y2 
                    and SAlt < 1400 and SAlt > 200
                    and SHdg < 360 and SHdg > 270):
                    LandingAirport = "LGB"
                #--------------------------------------------------------
                #--------------LAX landing box--------------
                y1 , x1 , y2 , x2 = -118.445989,33.927158,-118.095114,33.995785
                if (x > x1 and x < x2 and y > y1 and y < y2):
                    LandingAirport = "LAX"
                #------------------------------------------
                AirplaneDict.update({SFlight : [LandingAirport,SAlt,SSpd,SHdg,SLat,SLong,int(time.time())]})
            if OverallTimer % 100 == 0:
                print("\033[H\033[J")
                print("  Flight # ,Altitude,Speed, Heading ,Latitude , Longitude , Unix Time")
                pp.pprint(AirplaneDict)
                #Clean up dictionary
                try:
                    for key, value in AirplaneDict.items():
                        if int(time.time()) - value[6] > 60:
                            AirplaneDict.pop(key)
                except:
                    pass

    except KeyboardInterrupt:
        print('Shutting Down')
        process.kill()
        process.terminate()
        os.system("taskkill /f /im  dump1090.exe")
        sys.exit(0)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        