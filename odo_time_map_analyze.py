import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient
import lib.analyze_util as au
from scipy.misc import imread
import time
from lib.time_util import TimeUtil
from matplotlib.dates import DateFormatter
import lib.sensors.gps_tools as gt


def convertMGL(adc):
    c = adc * (5/26665.8528646) #Converts to a 0-5V range
    output = (c * 4.444) - .4444 #Converts to mg/L based of Vernier's scale
        
    return output


mongo = MongoClient(host=au.serverAddressSelector())

dbCol = au.dbColSelector(mongo)

formatter = DateFormatter('%H:%M:%S')


# ===================ODO CONVERTED Time Plot ==================
plt.figure(1)
plt.clf()
#plt.subplot(111)
plt.autoscale(True)
t0 = time.time()

dataReading = []
dataTime = []
randEpoch = 0

for ii, val in enumerate(dbCol.find({"atype":"ODO"})):
    dataReading.append(val["param"])
    dataTime.append( val["ts"])
    
    if ii == 0:
        randEpoch = TimeUtil.EpochToDate(val["ts"])
        
mdataStandardDate = np.array( [ TimeUtil.EpochToTime(tt) for tt in dataTime ] )

dataReading = np.array( [ convertMGL(val) for val in dataReading ] )


plt.title(str(randEpoch) + ": Dissolved Oxygen Levels")
plt.ylabel("mg/L")
plt.xlabel("Time)")


plt.plot(mdataStandardDate, dataReading, "g-")


plt.gcf().axes[0].xaxis.set_major_formatter(formatter)  
plt.show()


# ================ ODO Converted Map Plot ============
# Greater oxygen values are darker

plt.figure(2)
plt.clf()
plt.autoscale(True)

maxVal = max(dataReading)
minVal = min(dataReading)

dataLat = []
dataLon = []
colors = []

''' Method for extracting lat and long values closest to the times of the data taken'''
gpsData = []
for ii in dbCol.find({"atype":"GPS"}):
    gpsData.append(ii)


for ii in dataTime:
    newGpsData = gt.nearestLocationFromTime(gpsData, ii, timeTag = "ts")
    dataLat.append(newGpsData["param"]["lat"])
    dataLon.append(newGpsData["param"]["lon"])

for i in range(len(dataReading)):
    colors.append(1- (dataReading[i] - minVal)/(maxVal-minVal))
    
for j in range(len(dataLat)):
    plt.plot([dataLon[j]], [dataLat[j]], 'bo', c=str(colors[j]))



plt.xlabel("Longitude (deg)")
plt.ylabel("Latitude (deg)")
plt.title(str(randEpoch) + ': Oxygen Level and Location')

# Disable autoscaling to stop images from affecting scale
plt.autoscale(False)

# Add Brick Yard Pond map
img = imread("maps/byp.jpg")
plt.imshow(img, zorder=0, extent=[-71.330371, -71.307692, 41.730781, 41.739235])

# LL 41.730781, -71.330371
# UR 41.739235, -71.307692


plt.show()

