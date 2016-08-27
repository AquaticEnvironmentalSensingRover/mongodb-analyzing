# THIS IS A HEAVILY MODIFED VERSION OF "all_data_analyze.py"
# 160703 v2 RG Changing format of date printout to help with analysis after
#   data taking
# Modify formats for arrays to Numpy Arrays to allow subsequent analysis
#   interactively

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import lib.analyze_util as au
import lib.database_util as du
from scipy.misc import imread
import time
import datetime
import math
from matplotlib.dates import DateFormatter

# For multiple y-axes
# http://matplotlib.org/examples/axes_grid/demo_parasite_axes2.html
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA

# PICK SERVER OR USE PRESET
mongo = du.getServerHost(True)


# Cut the data for only that when on the lake
# Epoch times for start and stop

# Run004
runNum = du.getRunNumber()
print "Run number: {}".format(runNum)
if math.floor(runNum) == 4:
    tStartRun = time.mktime(datetime.datetime(2016, 7, 16, 18, 40).timetuple())
    tStopRun = time.mktime(datetime.datetime(2016, 7, 16, 19, 30).timetuple())
elif math.floor(runNum) == 5:
    tStartRun = time.mktime(datetime.datetime(2016, 7, 17, 0, 0).timetuple())
    tStopRun = time.mktime(datetime.datetime(2016, 7, 17, 23, 59).timetuple())
else:
    raise ValueError("No known run number")
dbCol = du.getDbCol(mongo)


# Used to format the date/time axis
# formatter = DateFormatter('%H:%M:%S')
formatter = DateFormatter('%H:%M')


# ======================GPS======================
plt.figure(100)
plt.clf()
# plt.subplot(221)


# t0 = time.time()

# Get GPS data
# gpsList = [("GPS","bo"), ("IGPS","r-")]
gpsList = [("GPS", "b.")]
for ii in gpsList:
    gpsLonList = []
    gpsLatList = []
    gpsTimeList = []
    for jj in dbCol.find({"atype": ii[0]}):
        gpsLonList.append((jj["param"])["lon"])
        gpsLatList.append((jj["param"])["lat"])
        gpsTimeList.append(jj["ts"])


# Convert the lists to Numpy ndarray for later use
gpsLon = np.array(gpsLonList)   # now convert to ndarray for later analysis
gpsLat = np.array(gpsLatList)
gpsTime = np.array(gpsTimeList)

# Get pressure data:
pressureDataList = []
pressureTimeList = []
for ii in dbCol.find({"atype": "PRESR"}):
    pressureDataList.append(ii['param']['mbar'])
    pressureTimeList.append(ii['ts'])


newGpsData, newPressureTimeList, newPressureDataList = \
                                            au.nearestPairsFromTimesDelNone(
                                                gpsTimeList,
                                                zip(gpsLonList, gpsLatList),
                                                pressureTimeList,
                                                pressureDataList,
                                                maximumTimeDiff=None
                                            )

newGpsLonList, newGpsLatList = zip(*newGpsData)

maxPressure = max(newPressureDataList)

minPressure = min(newPressureDataList)


# Plot GPS data
plt.title("GPS (Run: %.2f)" % runNum)
plt.xlabel("Longitude (deg)")
plt.ylabel("Latitude (deg)")

# Enable autoscaling
plt.autoscale(True)

# Plot the center of the house
# plt.plot(-71.343310, 41.739910, 'rd')

# Normal plotting:
normalPlot = False
if normalPlot:
    plt.scatter(gpsLonList, gpsLatList, c='b', marker='.', edgecolors='face')
else:
    plt.scatter(newGpsLonList, newGpsLatList, c=newPressureDataList,
                marker='.', cmap=cm.jet_r, edgecolors='face')
    gpsPressureColorBar = plt.colorbar()
    gpsPressureColorBar.ax.invert_yaxis()
    gpsPressureColorBar.ax.set_ylabel('Pressure (mbar)', rotation=270,
                                      labelpad=20)

plt.xlabel("Longitude (deg)")
plt.ylabel("Latitude (deg)")

# Plot time markers
timeMarkInterval = 30  # Seconds
timeMarkTime = tStartRun
timeMarkTimes = []
while timeMarkTime < tStopRun:
    timeMarkTimes.append(timeMarkTime)
    timeMarkTime += timeMarkInterval  # seconds

gpsVals, timeMarkTimes = au.nearestPairsFromTimesDelNone(gpsTimeList,
                                                         zip(gpsLonList,
                                                             gpsLatList),
                                                         timeMarkTimes,
                                                         maximumTimeDiff=10)

if not len(gpsVals) == 0:
    plt.plot(*zip(*gpsVals), color='r', linestyle='None', marker='+',
             markersize=10)

# Disable autoscaling to stop images from affecting scale
plt.autoscale(False)

# Add map background
img = imread("maps/map.jpg")
plt.imshow(img, zorder=0, extent=[-180, 180, -90, 90])

# Add house image in specific position
if False:
    img = imread("maps/house.jpg")
    plt.imshow(img, zorder=0, extent=[-71.343431, -71.3424, 41.739744,
                                      41.740059])

# Add zoomed-out house image in specific position
    img = imread("maps/house2.jpg")
    plt.autoscale(True)
    plt.imshow(img, zorder=0, extent=[-71.34516, -71.34072, 41.738835,
                                      41.740670])
    plt.autoscale(False)

# UL 41.740657, -71.345162
# LL 41.738835, -71.345169
# UR 41.740670, -71.340646
# LR 41.738851, -71.340643

# Add Brick Yard Pond map
img = imread("maps/byp.jpg")
plt.imshow(img, zorder=0, extent=[-71.330371, -71.307692, 41.730781,
                                  41.739235])

# LL 41.730781, -71.330371
# UR 41.739235, -71.307692

plt.show()
