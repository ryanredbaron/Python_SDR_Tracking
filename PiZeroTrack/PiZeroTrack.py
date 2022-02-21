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
import json

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
AirplaneDict = {}

CreatedList = []

a = App(title="PiFlight Track", height=ScreenHeight, width=ScreenWidth)
a.full_screen = True

cmd = "/home/pi/Desktop/dump1090/dump1090 --quiet --write-json /home/pi/Desktop/JSONfolder"
JSONlocation = "/home/pi/Desktop/JSONfolder/aircraft.json"
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

try:
    def RTLData():
        global AirplaneDict
        global SweepLocation
        global d
        
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
            JsonFile = open(JSONlocation)
            JSONLoad = json.load(JsonFile)
            for SingleAircraft in JSONLoad['aircraft']:
                SHex = ""
                SFlight = ""
                SAlt = 0
                SSpd = 0
                SHdg = 0
                SLat = 0.0
                SLong = 0.0
                try: 
                    SHex = SingleAircraft['hex']
                except:
                    pass
                
                try:
                    SFlight = SingleAircraft['flight']
                except:
                    pass
                
                try: 
                    SAlt = int(SingleAircraft['alt_baro'])
                except:
                    pass
                
                try:
                    SSpd = int(SingleAircraft['gs'])
                except:
                    pass
                
                try:
                    SHdg = int(SingleAircraft['track'])
                except:
                    pass
                
                try:
                    SLat = float(SingleAircraft['lat'])
                except:
                    pass
                
                try:
                    SLong = float(SingleAircraft['lon'])
                except:
                    pass
                
                AirplaneDict.update({SHex : [SFlight,SAlt,SSpd,SHdg,SLat,SLong,int(time.time())]})
            JsonFile.close()
                        
            for k, v in AirplaneDict.items():
                print(k)
                print("------")
                print(v)
                print("-------------")
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
            try:
                CleanUpAirplaneDict = AirplaneDict
                for key, value in CleanUpAirplaneDict.items():
                    if int(time.time()) - value[6] > 10:
                        AirplaneDict.pop(key)
            except:
                pass
                Processing = False
        
    
    d = Drawing(a, height=ScreenHeight, width=ScreenWidth)
    d.bg = "black"
    d.repeat(250, RTLData)
    
    a.display()

except KeyboardInterrupt:
    print('Shutting Down')
    process.kill()
    process.terminate()
    os.system('pkill dump1090')
    sys.exit(0)