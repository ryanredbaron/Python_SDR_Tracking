# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 15:40:43 2022

@author: ryanr
"""

import sys
import subprocess
import time
import os
import math

from guizero import App, Drawing
CurrentLat = 33.792641
CurrentLong = -118.115471

SquareSize = 500
a = App(title="My app", height=SquareSize, width=SquareSize)

os.chdir("C:\\Users\\ryanr\\Documents\\GitHub\\Python_SDR_Tracking\\WinSDR")
cmd = "dump1090.bat"
try:
    os.system("taskkill /f /im  dump1090.exe")
except:
    pass

AirplaneDict = {}

process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

def RTLData():
    global AirplaneDict
    global process
    
    d.clear()
    d.image(0, 0, r"C:\Users\ryanr\Desktop\test7.png", width=SquareSize, height=SquareSize)
    d.oval((SquareSize/2)-10, (SquareSize/2)-10, (SquareSize/2)+10, (SquareSize/2)+10, color=None, outline=2, outline_color="red")

    
    Processing = True
    
    while Processing == True:
        try:
            output = ""
            output = (process.stdout.readline()).decode()
            ParseOutput = list(filter(None, output.split(" ")))
            if output:
                if output.startswith("Hex"):
                    continue
                if output.startswith("-----------------------------------"):
                    continue
                if len(ParseOutput) == 12 and ParseOutput[0] != "(INCLUDING" and ParseOutput[0] != "OF":
                    SHex = ParseOutput[0]
                    SFlight = ParseOutput[3]
                    try:
                        SAlt = int(ParseOutput[4])
                    except:
                        SAlt = 0
                    SSpd = int(ParseOutput[5])
                    SHdg = int(ParseOutput[6])
                    SLat = float(ParseOutput[7])
                    SLong = float(ParseOutput[8])

                    AirplaneDict.update({SFlight : [SHex,SAlt,SSpd,SHdg,SLat,SLong,int(time.time())]})
                   
                    for k, v in AirplaneDict.items():
                        DisplayLong = (SquareSize/2) + ((CurrentLat - v[4]) * 1000)
                        DisplayLat = (SquareSize/2) - ((CurrentLong - v[5]) * 1000)
                        d.text(DisplayLat-15,DisplayLong-25,k,size=8)
                        d.oval(DisplayLat-5, DisplayLong-5, DisplayLat+5, DisplayLong+5, color=None, outline=2, outline_color="blue")
                        
                        Radius = v[2]/10
                        Heading = ((v[3]-90)%360)*(0.017453)
                        X1 = DisplayLat
                        Y1 = DisplayLong
                        X2 = (Radius)*(math.cos(Heading))+DisplayLat
                        Y2 = (Radius)*(math.sin(Heading))+DisplayLong
                        d.line(X1,Y1,X2,Y2,color="black",width=2)
                #Clean up dictionary
                    try:
                        CleanUpAirplaneDict = AirplaneDict
                        for key, value in CleanUpAirplaneDict.items():
                            if int(time.time()) - value[6] > 10:
                                AirplaneDict.pop(key)
                    except:
                        pass
                    Processing = False
        except KeyboardInterrupt:
            print('Shutting Down')
            process.kill()
            process.terminate()
            os.system("taskkill /f /im  dump1090.exe")
            sys.exit(0)
    

d = Drawing(a, width=SquareSize, height=SquareSize)
d.repeat(100, RTLData)

a.display()