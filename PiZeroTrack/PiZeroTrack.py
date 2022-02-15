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

a = App(title="PiFlight Track", height=ScreenHeight, width=ScreenWidth)

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
    d.image(0, 0, r"C:\Users\ryanr\Desktop\test9.png", height=ScreenHeight, width=ScreenWidth)
    RadarRing = 1
    d.oval((ScreenWidth/2)-((RadarRing*MapRadius)/2), (ScreenHeight/2)-((RadarRing*MapRadius)/2), (ScreenWidth/2)+((RadarRing*MapRadius)/2), (ScreenHeight/2)+((RadarRing*MapRadius)/2), color=None, outline=2, outline_color="red")
    RadarRing = 5
    d.oval((ScreenWidth/2)-((RadarRing*MapRadius)/2), (ScreenHeight/2)-((RadarRing*MapRadius)/2), (ScreenWidth/2)+((RadarRing*MapRadius)/2), (ScreenHeight/2)+((RadarRing*MapRadius)/2), color=None, outline=2, outline_color="red")
    RadarRing = 10
    d.oval((ScreenWidth/2)-((RadarRing*MapRadius)/2), (ScreenHeight/2)-((RadarRing*MapRadius)/2), (ScreenWidth/2)+((RadarRing*MapRadius)/2), (ScreenHeight/2)+((RadarRing*MapRadius)/2), color=None, outline=2, outline_color="red")
    RadarRing = 15
    d.oval((ScreenWidth/2)-((RadarRing*MapRadius)/2), (ScreenHeight/2)-((RadarRing*MapRadius)/2), (ScreenWidth/2)+((RadarRing*MapRadius)/2), (ScreenHeight/2)+((RadarRing*MapRadius)/2), color=None, outline=2, outline_color="red")
    RadarRing = 20
    d.oval((ScreenWidth/2)-((RadarRing*MapRadius)/2), (ScreenHeight/2)-((RadarRing*MapRadius)/2), (ScreenWidth/2)+((RadarRing*MapRadius)/2), (ScreenHeight/2)+((RadarRing*MapRadius)/2), color=None, outline=2, outline_color="red")
    RadarRing = 25
    d.oval((ScreenWidth/2)-((RadarRing*MapRadius)/2), (ScreenHeight/2)-((RadarRing*MapRadius)/2), (ScreenWidth/2)+((RadarRing*MapRadius)/2), (ScreenHeight/2)+((RadarRing*MapRadius)/2), color=None, outline=2, outline_color="red")

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
                        #set a max lat/long that you want to see and scale from there
                        #Max lat = Current lat * Miles
                        #ScaleLat = Airplanelat/MaxLat = % of max
                        #MaxMiles * ScaleLat
                        
                        #(ScreenWidth/2)-((RadarRing*MapRadius)/2)
                        DisplayLong = ScreenWidth+(ScreenWidth*(((CurrentLat - v[4])*69)/MapRadius))
                        DisplayLat = ScreenHeight-(ScreenHeight*(((CurrentLong - v[5])*69)/MapRadius))                  
                        
                        '''
                        DisplayLong =  (ScreenHeight/2) + ((CurrentLat - v[4]) * (MapRadius/MilesPerLat))
                        DisplayLat = (ScreenWidth/2) + ((CurrentLong - v[5]) * (MapRadius/MilesPerLat))
                        '''
                        print(DisplayLat)
                        print(DisplayLong)
                        print("---------")
                        d.text(DisplayLat-15,DisplayLong-25,k,size=8)
                        d.oval(DisplayLat-5, DisplayLong-5, DisplayLat+5, DisplayLong+5, color=None, outline=2, outline_color="blue")
                        SpeedRadius = v[2]/10
                        Heading = ((v[3]-90)%360)*(0.017453)
                        X1 = DisplayLat
                        Y1 = DisplayLong
                        X2 = (SpeedRadius)*(math.cos(Heading))+DisplayLat
                        Y2 = (SpeedRadius)*(math.sin(Heading))+DisplayLong
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
    

d = Drawing(a, height=ScreenHeight, width=ScreenWidth)
d.repeat(100, RTLData)

a.display()