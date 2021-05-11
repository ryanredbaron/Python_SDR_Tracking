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
import winsound

MappingMode = 0
if MappingMode == 1:
    #https://towardsdatascience.com/easy-steps-to-plot-geographic-data-on-a-map-python-11217859a2db
    import matplotlib.pyplot as plt
    BBox = (-118.4772, -117.8188, 33.6341, 34.1078)
    ruh_m = plt.imread('C:\\Users\\Angus\\Documents\\GitHub\\Python_SDR_Tracking\\boundingmap.JPG')
    fig, ax = plt.subplots(figsize = (8,7))
    ax.set_title('Long Beach Map')
    ax.set_xlim(BBox[0],BBox[1])
    ax.set_ylim(BBox[2],BBox[3])
    ax.imshow(ruh_m, zorder=0, extent = BBox, aspect= 'equal')
    plt.pause(1)

os.chdir("C:\\Users\\Angus\\Documents\\GitHub\\Python_SDR_Tracking\\WinSDR")
cmd = "dump1090.bat"
try:
    os.system("taskkill /f /im  dump1090.exe")
except:
    pass
pp = pprint.PrettyPrinter(depth=10)

AirplaneDict = {}
LAXList = {}
LGBList = {}
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
    'KNIFE' : 'Military Helicopter',
    'N140HP' : 'CHP',
    'STMPD' : 'Marine Core',
    'N66W' : 'Med Fly drop'
    #,'SWA' : 'Test'
    }

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
                #https://boundingbox.klokantech.com/
                LandingAirport = "-"
                x, y = SLat, SLong
                #--------------Long Beach Landing Box--------------
                y1 , x1 , y2 , x2 = -118.163238,33.630198,-117.94984,33.815526
                if (x > x1 and x < x2 and y > y1 and y < y2
                    and SAlt < 2000 and SAlt > 250
                    and SHdg < 330 and SHdg > 300):
                    LandingAirport = "LGB"
                    LGBList.update({SFlight : [LandingAirport,SAlt,SSpd,SHdg,SLat,SLong,int(time.time())]})
                else:
                    try:
                        LGBList.pop(SFlight)
                    except:
                        pass
                #--------------------------------------------------------
                #--------------LAX landing box--------------
                y1 , x1 , y2 , x2 = -118.4445,33.8982,-117.7501,34.0794
                if (x > x1 and x < x2 and y > y1 and y < y2
                    and SHdg < 330 and SHdg > 230):
                    LandingAirport = "LAX"
                    LAXList.update({SFlight : [LandingAirport,SAlt,SSpd,SHdg,SLat,SLong,int(time.time())]})
                else:
                    try:
                        LAXList.pop(SFlight)
                    except:
                        pass
                #------------------------------------------
                AirplaneDict.update({SFlight : [LandingAirport,SAlt,SSpd,SHdg,SLat,SLong,int(time.time())]})
            if OverallTimer % 250 == 0:
                print("\033[H\033[J")
                print("------------------------LGBList------------------------")
                print("{:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format('FLight #','Alt','Spd','Head','Lat','Long'))
                for k, v in LGBList.items():
                    print("{:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format(k, v[1], v[2], v[3], v[4], v[5]))
                print("")
                print("")
                print("------------------------LAXList------------------------")
                print("{:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format('FLight #','Alt','Spd','Head','Lat','Long'))
                for k, v in LAXList.items():
                    print("{:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format(k, v[1], v[2], v[3], v[4], v[5]))
                print("")
                print("")
                print("------------------------Full List------------------------")
                print("{:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format('FLight #','Alt','Spd','Head','Lat','Long'))
                for k, v in AirplaneDict.items():
                    if v[2] > 600:
                        print("~~~~~~~~FAST AIRPLANE~~~~~~~~")
                    for coolplane in CoolAirPlaneList:
                        if k.startswith(coolplane):
                            print("~~~~~~~~COOL PLANE - "+CoolAirPlaneList[coolplane]+"~~~~~~~~")
                            #PlaySound('not.mp3', winsound.SND_FILENAME)
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
                try:
                    CleanUpAirplaneDict = LGBList
                    for key, value in CleanUpAirplaneDict.items():
                        if int(time.time()) - value[6] > 10:
                            LGBList.pop(key)
                except:
                    pass
                try:
                    CleanUpAirplaneDict = LAXList
                    for key, value in CleanUpAirplaneDict.items():
                        if int(time.time()) - value[6] > 10:
                            LAXList.pop(key)
                except:
                    pass
                if MappingMode == 1:
                    plt.pause(0.01)
                    ax.scatter([x[5] for x in list(AirplaneDict.values())], [x[4] for x in list(AirplaneDict.values())], zorder=1, c='b', s=25)
                    plt.pause(0.01)
    except KeyboardInterrupt:
        print('Shutting Down')
        process.kill()
        process.terminate()
        os.system("taskkill /f /im  dump1090.exe")
        sys.exit(0)        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        