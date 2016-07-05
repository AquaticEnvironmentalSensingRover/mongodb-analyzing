import numpy as np
import datetime
import time
import matplotlib.pyplot as plt
from pymongo import MongoClient
import matplotlib.dates as dates
from lib.time_util import TimeUtil
import lib.sensors.sonar_tools as st

scaleAirCmToWaterM = 1./100.*4.3

mongo = MongoClient(host="localhost")

from sonar_manual_data import *        

# Database Handling
dbName = 'AESR_20160629T185315'
colName = 'data'
dbCol = (mongo[dbName])[colName]

dataDepth = []
dataTime = []
randEpoch = None

for index, x in enumerate(dbCol.find({"atype":"SONAR"})):
    if x["param"] < 750: # Values >= 750 are bad read 
        dataDepth.append((x["param"]) * scaleAirCmToWaterM )
        dataTime.append(x["ts"])
    
        if index == 0:
            randEpoch = TimeUtil.EpochToDate(x["ts"])
                

finalDTime = []
finalDDepth = []

# For each hand sonar sounding find the 5 closest database sonar values
for x in mdataDateEpoch:
    
    t, d = st.closestSonar(dataTime, dataDepth, x )   
    
    for y in t:
        finalDTime.append(y)
        
    for y in d:
        finalDDepth.append(y)
             
        
plt.figure(1)
plt.clf()
plt.plot(finalDTime, finalDDepth, "bo")
plt.plot(mdataDateEpoch, mdataDepth, "ro")
plt.show()


