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
dbCols = du.getDbsCol(mongo)


# Used to format the date/time axis
# formatter = DateFormatter('%H:%M:%S')
formatter = DateFormatter('%H:%M')


# ==============================SENSOR VALUES=================================:
# ======================GPS======================:
# Get GPS data
# gpsList = [("GPS","bo"), ("IGPS","r-")]
gpsList = [("GPS", "b.")]
gpsLonList = []
gpsLatList = []
gpsTimeList = []
for ii in gpsList:
    for dbCol in dbCols:
        for jj in dbCol.find({"atype": ii[0]}):
            gpsLonList.append((jj["param"])["lon"])
            gpsLatList.append((jj["param"])["lat"])
            gpsTimeList.append(jj["ts"])


# Convert the lists to Numpy ndarray for later use
gpsLon = np.array(gpsLonList)   # now convert to ndarray for later analysis
gpsLat = np.array(gpsLatList)
gpsTime = np.array(gpsTimeList)

# =====================PRESR=====================:
# Get pressure data:
pressureTimeList = []
pressureDataList = []
for dbCol in dbCols:
    for ii in dbCol.find({"atype": "PRESR"}):
        pressureTimeList.append(ii['ts'])
        pressureDataList.append(ii['param']['mbar'])

pressureTime = np.asarray(pressureTimeList)
pressureData = np.asarray(pressureDataList)

# ======================TEMP=====================:
# Get temperaturer data:

temperatureTimeList = []
temperatureDataList = []
for dbCol in dbCols:
    for ii in dbCol.find({"atype": "TEMP"}):
        temperatureTimeList.append(ii['ts'])
        temperatureDataList.append(ii['param'])

temperatureTime = np.asarray(temperatureTimeList)
temperatureData = np.asarray(temperatureDataList)


# ======================ODO======================:
# Get optical dissolved oxygen data:
odoTimeList = []
odoDataList = []
for dbCol in dbCols:
    for ii in dbCol.find({"atype": "ODO"}):
        odoTimeList.append(ii['ts'])
        odoDataList.append(ii['param']['mgL'])

odoTime = np.asarray(odoTimeList)
odoData = np.asarray(odoDataList)


# ===========================PLOTTING FUNCTIONS===============================:
def gpsDataPlot(times, data, colorBarLabel=None,
                invertColorBar=False, timeMarkInterval=30, **kwargs):
    newGpsDataList, newTimeList, newDataList = \
                                            au.nearestPairsFromTimesDelNone(
                                                gpsTime.tolist(),
                                                zip(gpsLon.tolist(),
                                                    gpsLat.tolist()),
                                                times.tolist(), data.tolist(),
                                                maximumTimeDiff=None
                                            )

    newGpsLonList, newGpsLatList = zip(*newGpsDataList)
    newGpsLon = np.asarray(newGpsLonList)
    newGpsLat = np.asarray(newGpsLatList)
    newGpsLonList = newGpsLatList = newGpsDataList = None

    # newTime = np.asarray(newTimeList)
    # newTimeList = None
    newData = np.asarray(newDataList)
    newDataList = None

    # Plot GPS data
    plt.title("GPS (Run: %.2f)" % runNum)
    plt.xlabel("Longitude (deg)")
    plt.ylabel("Latitude (deg)")

    # Enable autoscaling
    plt.autoscale(True)

    plt.scatter(newGpsLon, newGpsLat, c=newData, marker='.', edgecolors='face',
                **kwargs)

    gpsPressureColorBar = plt.colorbar()
    if invertColorBar:
        gpsPressureColorBar.ax.invert_yaxis()
    if isinstance(colorBarLabel, str):
        gpsPressureColorBar.ax.set_ylabel(colorBarLabel, rotation=270,
                                          labelpad=20)

    plt.xlabel("Longitude (deg)")
    plt.ylabel("Latitude (deg)")

    # Plot time markers
    # 'timeMarkInterval' is an input
    timeMarkTime = tStartRun
    timeMarkTimes = []
    while timeMarkTime < tStopRun:
        timeMarkTimes.append(timeMarkTime)
        timeMarkTime += timeMarkInterval  # seconds

    gpsVals, timeMarkTimes = au.nearestPairsFromTimesDelNone(
                                                        gpsTime.tolist(),
                                                        zip(gpsLon.tolist(),
                                                            gpsLat.tolist()),
                                                        timeMarkTimes,
                                                        maximumTimeDiff=10
                                                            )

    if not len(gpsVals) == 0:
        plt.scatter(*zip(*gpsVals), c=range(len(gpsVals)), marker='+', s=100,
                    cmap=cm.seismic)

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


# ==================================PLOTS=====================================:
# ======================PRESR======================:
# Pressure GPS plot:
plt.figure(100)
plt.clf()

gpsDataPlot(pressureTime, pressureData, cmap=cm.jet_r,
            colorBarLabel='Pressure (mbar)', invertColorBar=True)
# =======================TEMP======================:
# Temperature GPS plot:
plt.figure(200)
plt.clf()

gpsDataPlot(temperatureTime, temperatureData,
            colorBarLabel='Temperature (degC) [vmin=26]', cmap=cm.jet, vmin=26)

# =======================ODO=======================:
# Optical Dissolved Oxygen GPS plot:
plt.figure(300)
plt.clf()

gpsDataPlot(odoTime, odoData, colorBarLabel='Dissolved Oxygen (mgL) [vmin=9]',
            cmap=cm.jet, vmin=9)

# PLOT:
plt.show()
