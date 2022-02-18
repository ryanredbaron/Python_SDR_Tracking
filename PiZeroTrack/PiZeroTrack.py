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

ScreenHeight = 640
ScreenWidth = 480

MiddleHeight = ScreenHeight/2
MiddleWidth = ScreenWidth/2

MapRadius = 25
MilesPerLat = 0.0145054945054945

SweepLocation = 0

a = App(title="PiFlight Track", height=ScreenHeight, width=ScreenWidth)
a.full_screen = True

cmd = "~/Desktop/dump1090/dump1090 --net --interactive"

AirplaneDict = {}

process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

def RTLData():
    global AirplaneDict
    global process
    global SweepLocation
    
    d.clear()
    d.line(ScreenWidth/2, 0, ScreenWidth/2, ScreenHeight,color="green")
    d.line(0,ScreenHeight/2,ScreenWidth,ScreenHeight/2,color="green")
    SweepLocation = SweepLocation + 1
    if SweepLocation >> 360:
        SweepLocation = 0
    SweepX = (ScreenWidth/2)+(640)*(math.cos(math.radians(SweepLocation)))
    SweepY = (ScreenHeight/2)+(640)*(math.sin(math.radians(SweepLocation)))
    d.line(ScreenWidth/2,ScreenHeight/2,SweepX,SweepY,color="green")
    RadarRing = 1
    d.oval((ScreenWidth/2)-((RadarRing*MapRadius)/2), (ScreenHeight/2)-((RadarRing*MapRadius)/2), (ScreenWidth/2)+((RadarRing*MapRadius)/2), (ScreenHeight/2)+((RadarRing*MapRadius)/2), color=None, outline=2, outline_color="green")
    RadarRing = 5
    d.oval((ScreenWidth/2)-((RadarRing*MapRadius)/2), (ScreenHeight/2)-((RadarRing*MapRadius)/2), (ScreenWidth/2)+((RadarRing*MapRadius)/2), (ScreenHeight/2)+((RadarRing*MapRadius)/2), color=None, outline=2, outline_color="green")
    RadarRing = 10
    d.oval((ScreenWidth/2)-((RadarRing*MapRadius)/2), (ScreenHeight/2)-((RadarRing*MapRadius)/2), (ScreenWidth/2)+((RadarRing*MapRadius)/2), (ScreenHeight/2)+((RadarRing*MapRadius)/2), color=None, outline=2, outline_color="green")
    RadarRing = 15
    d.oval((ScreenWidth/2)-((RadarRing*MapRadius)/2), (ScreenHeight/2)-((RadarRing*MapRadius)/2), (ScreenWidth/2)+((RadarRing*MapRadius)/2), (ScreenHeight/2)+((RadarRing*MapRadius)/2), color=None, outline=2, outline_color="green")
    RadarRing = 20
    d.oval((ScreenWidth/2)-((RadarRing*MapRadius)/2), (ScreenHeight/2)-((RadarRing*MapRadius)/2), (ScreenWidth/2)+((RadarRing*MapRadius)/2), (ScreenHeight/2)+((RadarRing*MapRadius)/2), color=None, outline=2, outline_color="green")
    RadarRing = 25
    d.oval((ScreenWidth/2)-((RadarRing*MapRadius)/2), (ScreenHeight/2)-((RadarRing*MapRadius)/2), (ScreenWidth/2)+((RadarRing*MapRadius)/2), (ScreenHeight/2)+((RadarRing*MapRadius)/2), color=None, outline=2, outline_color="green")

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
                    try:
                        SSpd = int(ParseOutput[5])
                    except:
                        SSpd = 0
                    try:
                        SHdg = int(ParseOutput[6])
                    except:
                        SHdg = 0
                    try:
                        SLat = float(ParseOutput[7])
                    except:
                        SLat = 0
                    try:
                        SLong = float(ParseOutput[8])
                    except:
                        SLong = 0
                                                    #0    1     2   3     4   5       6
                    AirplaneDict.update({SFlight : [SHex,SAlt,SSpd,SHdg,SLat,SLong,int(time.time())]})
                   
                    for k, v in AirplaneDict.items():
                        DisplayLong = (ScreenHeight/2)+(ScreenWidth*(((CurrentLat - v[4])*69)/MapRadius))
                        DisplayLat = (ScreenWidth/2)-(ScreenHeight*(((CurrentLong - v[5])*69)/MapRadius))                  
                        d.oval(DisplayLat-5, DisplayLong-5, DisplayLat+5, DisplayLong+5, color=None, outline=2, outline_color="blue")

                        SpeedRadius = v[2]/10
                        Heading = ((v[3]-90)%360)*(0.017453)
                        X1 = DisplayLat
                        Y1 = DisplayLong
                        X2 = (SpeedRadius)*(math.cos(Heading))+DisplayLat
                        Y2 = (SpeedRadius)*(math.sin(Heading))+DisplayLong
                        d.line(X1,Y1,X2,Y2,color="orange",width=2)
                        
                        d.text(DisplayLat-15,DisplayLong-25,k,size=8,color="white")
                        d.text(DisplayLat-15,DisplayLong+10,"Spd-"+str(v[2]),size=8,color="white")
                        d.text(DisplayLat-15,DisplayLong+20,"Alt-"+str(v[1]),size=8,color="white")
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
    

d = Drawing(a, height=ScreenHeight, width=ScreenWidth)
d.bg = "black"
d.repeat(100, RTLData)

a.display()