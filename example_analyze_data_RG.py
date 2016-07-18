# THIS IS A HEAVILY MODIFED VERSION OF "all_data_analyze.py"
# 160703 v2 RG Changing format of date printout to help with analysis after data taking
#  Modify formats for arrays to Numpy Arrays to allow subsequent analysis interactively
# 160704 RG FUrther mods
# 160706 RG Push to Git
# 160707 RG Edited,comments for clarity
# 160717 PTAG Edit for Run 4


import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient
import lib.analyze_util as au
from scipy.misc import imread
import time
import datetime
from matplotlib.dates import DateFormatter


# Cut the data for only that when on the lake
# Epoch times for start and stop
tStartRun004 = time.mktime( datetime.datetime(2016, 7, 16, 18, 40).timetuple() )
tStopRun004 = time.mktime( datetime.datetime(2016, 7, 16, 19, 30).timetuple() )



# Used to format the date/time axis
formatter = DateFormatter('%H:%M:%S')

# PICK SERVER OR USE PRESET
#mongo = MongoClient(host=au.serverAddressSelector())
mongo = MongoClient( ) # local
#mongo = MongoClient(host="10.0.2.197")
#mongo = MongoClient(host="172.16.0.2")

# PICK COLLECTION
#dbCol = au.dbColSelector(mongo)
dbCol = ( mongo['AESR_20160716T184018'] )['data']

# COMBINED FIGURE FROM  "all_data_analyze.py"
plt.figure(1)
plt.clf()

# ======================GPS======================
plt.figure(1)
plt.subplot(221)
t0 = time.time()
plt.title("GPS (Latest data: %f)" % t0 )
plt.xlabel("Longitude (deg)")
plt.ylabel("Latitude (deg)")

# Enable autoscaling
plt.autoscale(True)

# Plot the center of the house
plt.plot( -71.343310 , 41.739910 , 'rd' ) 

# Get GPS data
#gpsList = [("GPS","bo"), ("IGPS","r-")]
gpsList = [ ("GPS","b.") ]
for ii in gpsList:
    gpsLon = []  # lists
    gpsLat = []
    gpsTime = []
    for jj in dbCol.find({"atype":ii[0]}):
        gpsLon.append((jj["param"])["lon"])  # appending to list is very easy
        gpsLat.append((jj["param"])["lat"])
        gpsTime.append( jj["ts"] )
        
    plt.plot(gpsLon, gpsLat , ii[1])
    
    # Plot GPS data

# Convert the lists to Numpy ndarray for later use
gpsLat = np.array( gpsLat )   # now convert to ndarray for later analysis
gpsLon = np.array( gpsLon )
gpsTime = np.array( gpsTime )

# Disable autoscaling to stop images from affecting scale
plt.autoscale(False)

# Add map background
img = imread("maps/map.jpg")
plt.imshow(img, zorder=0, extent=[-180, 180, -90, 90])

# Add house image in specific position
img = imread("maps/house.jpg")
plt.imshow(img, zorder=0, extent=[-71.343431, -71.3424, 41.739744, 41.740059])

# Add zoomed-out house image in specific position
img = imread("maps/house2.jpg")
plt.imshow(img, zorder=0, extent=[-71.34516, -71.34072, 41.738835, 41.740670])

# UL 41.740657, -71.345162
# LL 41.738835, -71.345169
# UR 41.740670, -71.340646
# LR 41.738851, -71.340643

# Add Brick Yard Pond map
img = imread("maps/byp.jpg")
plt.imshow(img, zorder=0, extent=[-71.330371, -71.307692, 41.730781, 41.739235])

# LL 41.730781, -71.330371
# UR 41.739235, -71.307692

# ZOOM IN 

plt.figure(1000)
plt.clf()

tStartRun004line = time.mktime( datetime.datetime(2016, 7, 16, 18, 55).timetuple() )
tStopRun004line = time.mktime( datetime.datetime(2016, 7, 16, 19, 13).timetuple() )

cut = (     ( gpsTime >= tStartRun004 )    &     (gpsTime <= tStopRun004)      ) # Make a cut
plt.plot(gpsLon[cut], gpsLat[cut] , 'r.' )

cut = (     ( gpsTime >= tStartRun004line )    &     (gpsTime <= tStopRun004line )      ) # Make a cut
plt.plot(gpsLon[cut], gpsLat[cut] , 'y.' )


# ======================PRESSURE======================
plt.figure(1)
plt.subplot(222)
plt.autoscale(True)
t0 = time.time()
plt.title("Pressure vs. Time (Latest data: %f)" % t0 )
plt.ylabel("Pressure (mbar)")
plt.xlabel("Time (s)")

# Start with lists
pressrValue = []
pressrTime = []

for ii in dbCol.find({"atype":"PRESR"}):
    pressrValue.append( (ii["param"])["mbar"])
    pressrTime.append( ii["ts"] - t0)

# Convert the lists to Numpy ndarray for later use
pressrValue = np.array( pressrValue )
pressrTime = np.array( pressrTime )

plt.plot(pressrTime, pressrValue, "ro")





# ======================SONAR======================
plt.figure(1)
plt.subplot(223)
plt.autoscale(True)
t0 = time.time()
plt.title("Depth/Distance vs. Time (Latest data: %f)" % t0 )
plt.ylabel("Depth/Distance (cm)")
plt.xlabel("Time (s)")

depthValue = []
depthTime = []

for ii in dbCol.find({"atype":"SONAR"}):
    depthValue.append(ii["param"])
    depthTime.append( ii["ts"] - t0)

plt.plot(depthTime, depthValue, "mo")

# Convert the lists to Numpy ndarray for later use
depthValue = np.array( depthValue )
depthTime = np.array( depthTime )


# ======================TEMPERATURE======================
#plt.figure(1)
#plt.subplot(224)
plt.figure(2)
plt.clf()

plt.autoscale(True)
t0 = time.time()
plt.title("Temperature (Latest data: %f)" % t0 )
#plt.axis([-100, 5, 22, 26])
plt.ylabel("Temperature (degC)")
plt.xlabel("Time (s)")

colors = ["r-","g-","b-","c-","k-"]
# colors = ["ro","go","bo","co","ko"]

sensorAmount = 5

timeStamp = []
data = []

for ii in range(sensorAmount):  # Loop through all 5 thermometers
    newTimeStamp = []
    newData = []
    for jj in dbCol.find({"atype":"TEMP", "itype":ii}):
        newTimeStamp.append(jj["ts"])
        newData.append(jj["param"])
    
    timeStamp.append(newTimeStamp)
    data.append(newData)
    
# Create ndarrays - each row is epoch time, temp # , or value
#tempTime = np.empty((0,),dtype=float)
#tempIndex = np.empty((0,),dtype=int)
#tempValue = np.empty((0,),dtype=float)
    
# Make Numpy version    
tempTime = []
tempIndex = []
tempValue = []

for ii in dbCol.find({"atype":"TEMP"}):
    tempTime.append( ii["ts"])
    tempIndex.append(ii["itype"])
    tempValue.append(ii["param"])

# Convert the lists to Numpy ndarray for later use
tempTime = np.array( tempTime )
tempValue = np.array( tempValue )
tempIndex = np.array( tempIndex )



for index, ii in enumerate(data):
    # Usual plot in seconds from now
    # plt.plot(np.add(timeStamp[index],-t0), ii, colors[index]
    #        , label=("Temp: " + str(index)))

    # Plot with date stamp
    plt.plot( [ datetime.datetime.fromtimestamp(x) for x in timeStamp[index] ]
    , ii 
    , colors[index] 
    , label=("Temp: " + str(index))
    )
    plt.gcf().axes[0].xaxis.set_major_formatter(formatter)

# Add legend to subplot
plt.legend()


# ======================ADC/ODO Sensor======================
plt.figure(3)
plt.clf()
plt.subplot(111)
plt.autoscale(True)
t0 = time.time()
plt.title("ODO (Latest data: %f)" % t0 )
plt.ylabel("Dat value (idk)")
plt.xlabel("Time (s)")

odoADC = []
odoTime = []

for ii in dbCol.find({"atype":"ODO"}):
    odoADC.append(ii["param"]["mgL"])
    odoTime.append( ii["ts"] - t0)

plt.plot(odoTime, odoADC, "g-")


plt.show()



# =============== NEW ADDITIONAL PLOTS WITH NEW NP VARIABLES ===============
# DEMONSTRATES USE OF CUTS IN DATA

# 160704 RG 

# global gpsLat,gpsLon,gpsTime

# print np.shape( gpsLat )
# Force them to be numpy arrays - logic below won't work on simple lists
#gpsLat = np.array( gpsLat )
#gpsLon = np.array( gpsLon )
#gpsTime = np.array( gpsTime )

formatter = DateFormatter('%H:%M:%S')

# Show all the gps data
plt.figure(14) ; plt.clf()
plt.plot( [ datetime.datetime.fromtimestamp(x) for x in gpsTime ], gpsLat , 'r.' )
plt.gcf().axes[0].xaxis.set_major_formatter(formatter)


# Show  the gps data within a certain time range
plt.figure(15) ; plt.clf()
cut = ( ( gpsTime >= tStartRun004 ) & (gpsTime <= tStopRun004) ) # Make a cut
plt.plot(  [ datetime.datetime.fromtimestamp(x) for x in (gpsTime[ cut ]) ]  , gpsLat[  cut ]  , 'r.' )
plt.gcf().axes[0].xaxis.set_major_formatter(formatter)

