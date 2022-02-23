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

from gps import *
import threading

gpsd = None

class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd
    gpsd = gps(mode=WATCH_ENABLE)
    self.current_value = None
    self.running = True
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next()

gpsp = GpsPoller()
gpsp.start()

CurrentLat = 33.792641
CurrentLong = -118.115471

BackupLat = CurrentLat
BackupLong = CurrentLong

ScreenHeight = 640
ScreenWidth = 480

MiddleHeight = ScreenHeight/2
MiddleWidth = ScreenWidth/2

MapRadius = 25
MilesPerLat = 0.0145054945054945

SweepLocation = 0
AirplaneDict = {}

a = App(title="PiFlight Track", height=ScreenHeight, width=ScreenWidth)
a.full_screen = True

cmd = "/home/pi/Desktop/dump1090/dump1090 --quiet --write-json /home/pi/Desktop/JSONfolder"
JSONlocation = "/home/pi/Desktop/JSONfolder/aircraft.json"
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

CoolAirPlaneList = {
    'MF8' : 'Weird Military Aircraft',
    'NASA' : 'NASA Airplane',
    'OAE' : 'Government Contractor',
    'N628TS' : 'Elon Musk',
    'N758PB' : 'Jeff Bezos',
    'N271DV' : 'Jeff Bezos',
    'N744VG' : 'Virgin Launcher 747',
    'N9187' : 'Catalina Delivery',
    'N9680B' : 'Catalina Delivery',
    'SLAM' : 'Military Transport?',
    'KNIFE' : 'Military Helicopter?',
    'N140HP' : 'CHP',
    'STMPD' : 'Marine Core',
    'N66W' : 'Med Fly drop'
    #,'SWA' : 'Test'
    }

try:
    def RTLData():
        global AirplaneDict
        global SweepLocation
        global d
        global CurrentLat
        global CurrentLong
        
        d.clear()
        SweepLocation = SweepLocation + 1
        if SweepLocation >> 360:
            SweepLocation = 0
        SweepX = (ScreenWidth/2)+(640)*(math.cos(math.radians(SweepLocation)))
        SweepY = (ScreenHeight/2)+(640)*(math.sin(math.radians(SweepLocation)))
        d.text(ScreenWidth/2,0,"N",size=20,color="green")
        d.text(ScreenWidth/2,ScreenHeight-24,"S",size=20,color="green")
        d.text(ScreenWidth-20,(ScreenHeight/2)-25,"E",size=20,color="green")
        d.text(0,(ScreenHeight/2)-24,"W",size=20,color="green")
        
        d.line(ScreenWidth/2,ScreenHeight/2,SweepX,SweepY,color="green")
        
        RadarRing = 1
        d.oval((ScreenWidth/2)-((RadarRing*MapRadius)/2), (ScreenHeight/2)-((RadarRing*MapRadius)/2), (ScreenWidth/2)+((RadarRing*MapRadius)/2), (ScreenHeight/2)+((RadarRing*MapRadius)/2), color=None, outline=2, outline_color="green")
        d.text((ScreenWidth/2)+((RadarRing*MapRadius)/2),ScreenHeight/2,RadarRing,size=20,color="green")
        RadarRing = 5
        d.oval((ScreenWidth/2)-((RadarRing*MapRadius)/2), (ScreenHeight/2)-((RadarRing*MapRadius)/2), (ScreenWidth/2)+((RadarRing*MapRadius)/2), (ScreenHeight/2)+((RadarRing*MapRadius)/2), color=None, outline=2, outline_color="green")
        d.text((ScreenWidth/2)+((RadarRing*MapRadius)/2),ScreenHeight/2,RadarRing,size=20,color="green")
        RadarRing = 10
        d.oval((ScreenWidth/2)-((RadarRing*MapRadius)/2), (ScreenHeight/2)-((RadarRing*MapRadius)/2), (ScreenWidth/2)+((RadarRing*MapRadius)/2), (ScreenHeight/2)+((RadarRing*MapRadius)/2), color=None, outline=2, outline_color="green")
        d.text((ScreenWidth/2)+((RadarRing*MapRadius)/2),ScreenHeight/2,RadarRing,size=20,color="green")
        RadarRing = 15
        d.oval((ScreenWidth/2)-((RadarRing*MapRadius)/2), (ScreenHeight/2)-((RadarRing*MapRadius)/2), (ScreenWidth/2)+((RadarRing*MapRadius)/2), (ScreenHeight/2)+((RadarRing*MapRadius)/2), color=None, outline=2, outline_color="green")
        d.text((ScreenWidth/2)+((RadarRing*MapRadius)/2),ScreenHeight/2,RadarRing,size=20,color="green")
        RadarRing = 20
        d.oval((ScreenWidth/2)-((RadarRing*MapRadius)/2), (ScreenHeight/2)-((RadarRing*MapRadius)/2), (ScreenWidth/2)+((RadarRing*MapRadius)/2), (ScreenHeight/2)+((RadarRing*MapRadius)/2), color=None, outline=2, outline_color="green")
        d.text((ScreenWidth/2)+((RadarRing*MapRadius)/2),ScreenHeight/2,RadarRing,size=20,color="green")
        RadarRing = 25
        d.oval((ScreenWidth/2)-((RadarRing*MapRadius)/2), (ScreenHeight/2)-((RadarRing*MapRadius)/2), (ScreenWidth/2)+((RadarRing*MapRadius)/2), (ScreenHeight/2)+((RadarRing*MapRadius)/2), color=None, outline=2, outline_color="green")
        d.text((ScreenWidth/2)+((RadarRing*MapRadius)/2),ScreenHeight/2,RadarRing,size=20,color="green")
        
        d.line(ScreenWidth/2, 0, ScreenWidth/2, ScreenHeight,color="green")
        d.line(0,ScreenHeight/2,ScreenWidth,ScreenHeight/2,color="green")
        
        Processing = True
        while Processing == True:
            JsonFile = open(JSONlocation)
            JSONLoad = json.load(JsonFile)
            for SingleAircraft in JSONLoad['aircraft']:
                SHex = ''
                SFlight = ''
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
                #                     k     v   0      1    2   3     4     5        6
                AirplaneDict.update({SHex : [SFlight,SAlt,SSpd,SHdg,SLat,SLong,int(time.time())]})
            JsonFile.close()
            try:
                if math.isnan(gpsd.fix.latitude) or gpsd.fix.latitude == 0:
                    CurrentLat = BackupLat
                else:
                    CurrentLat = gpsd.fix.latitude
            except:
                CurrentLat = 0
            try:
                if math.isnan(gpsd.fix.longitude) or gpsd.fix.longitude == 0:
                    CurrentLong = BackupLong
                else:
                    CurrentLong = gpsd.fix.longitude
            except:
                CurrentLong = 0
            for k, v in AirplaneDict.items():
                try:
                    if k and v[1] != 0 and  v[2] != 0 and  v[3] != 0 and  v[4] != 0 and  v[5] != 0 and CurrentLong and CurrentLat:
                        DisplayLong = (ScreenHeight/2)+(ScreenWidth*(((CurrentLat - v[4])*69)/MapRadius))
                        DisplayLat = (ScreenWidth/2)-(ScreenHeight*(((CurrentLong - v[5])*69)/MapRadius))
                        if v[0] == '':
                            FlightName = k
                        else:
                            FlightName = v[0]
                        CoolPlane = 0
                        for coolplane in CoolAirPlaneList or v[2] > 590:
                            if FlightName.startswith(coolplane):
                                CoolPlane = 1
                                continue
                            else:
                                CoolPlane = 0
                        if CoolPlane == 1:
                            d.oval(DisplayLat-10, DisplayLong-10, DisplayLat+10, DisplayLong+10, color=None, outline=4, outline_color="red")
                        else:
                            d.oval(DisplayLat-5, DisplayLong-5, DisplayLat+5, DisplayLong+5, color=None, outline=2, outline_color="blue")
            
                        SpeedRadius = v[2]/8
                        Heading = ((v[3]-90)%360)*(0.017453)
                        X1 = DisplayLat
                        Y1 = DisplayLong
                        X2 = (SpeedRadius)*(math.cos(Heading))+DisplayLat
                        Y2 = (SpeedRadius)*(math.sin(Heading))+DisplayLong
                        d.line(X1,Y1,X2,Y2,color="orange",width=2)
                        
                        d.text(DisplayLat-15,DisplayLong-25,FlightName,size=8,color="white")
                        d.text(DisplayLat-15,DisplayLong+10,"Spd-"+str(v[2]),size=8,color="white")
                        d.text(DisplayLat-15,DisplayLong+20,"Alt-"+str(v[1]),size=8,color="white")
                except:
                    print("error")
                    pass
            AirplaneDict = {}
            Processing = False
        
    d = Drawing(a, height=ScreenHeight, width=ScreenWidth)
    d.bg = "black"
    d.repeat(500, RTLData)
    
    a.display()

except KeyboardInterrupt:
    print('Shutting Down')
    process.kill()
    process.terminate()
    os.system('pkill dump1090')
    sys.exit(0)