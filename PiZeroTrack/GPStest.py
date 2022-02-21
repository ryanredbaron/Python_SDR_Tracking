# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 13:10:53 2022

@author: ryanr
"""

from gps import *
import threading
import time

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

while True:
	print(gpsd.fix.Latitude)
	print(gpsd.fix.Longitude)
	time.sleep(1)