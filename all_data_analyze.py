import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient
import lib.analyze_util as au
from scipy.misc import imread
import time

<<<<<<< Updated upstream
mongo = MongoClient(host=au.serverAddressSelector())
=======
mongo = MongoClient(host="10.0.2.197")
#mongo = MongoClient(host="172.16.0.2")
>>>>>>> Stashed changes

dbCol = au.dbColSelector(mongo)

plt.figure(1)
plt.clf()

# ======================GPS======================
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
gpsList = [("GPS","bo"), ("IGPS","r-")]
for ii in gpsList:
    lon = []
    lat = []
    for jj in dbCol.find({"atype":ii[0]}):
        lon.append((jj["param"])["lon"])
        lat.append((jj["param"])["lat"])
    
    # Plot GPS data
    plt.plot(lon, lat, ii[1])

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

# ======================PRESSURE======================
plt.subplot(222)
plt.autoscale(True)
t0 = time.time()
plt.title("Pressure vs. Time (Latest data: %f)" % t0 )
plt.ylabel("Pressure (mbar)")
plt.xlabel("Time (s)")

dataPressr = []
dataTime = []

for ii in dbCol.find({"atype":"PRESR"}):
    dataPressr.append( (ii["param"])["mbar"])
    dataTime.append( ii["ts"] - t0)

plt.plot(dataTime, dataPressr, "ro")


# ======================SONAR======================
plt.subplot(223)
plt.autoscale(True)
t0 = time.time()
plt.title("Depth/Distance vs. Time (Latest data: %f)" % t0 )
plt.ylabel("Depth/Distance (cm)")
plt.xlabel("Time (s)")

dataDepth = []
dataTime = []

for ii in dbCol.find({"atype":"SONAR"}):
    dataDepth.append(ii["param"])
    dataTime.append( ii["ts"] - t0)

plt.plot(dataTime, dataDepth, "mo")


# ======================TEMPERATURE======================
plt.subplot(224)
plt.autoscale(True)
t0 = time.time()
plt.title("Temperature (Latest data: %f)" % t0 )
#plt.axis([-100, 5, 22, 26])
plt.ylabel("Temperature (degC)")
plt.xlabel("Time (s)")

colors = ["ro","go","bo","co","ko"]

sensorAmount = 5

timeStamp = []
data = []

for ii in range(sensorAmount):
    newTimeStamp = []
    newData = []
    for jj in dbCol.find({"atype":"TEMP", "itype":ii}):
        newTimeStamp.append(jj["ts"])
        newData.append(jj["param"])
    
    timeStamp.append(newTimeStamp)
    data.append(newData)
    
for index, ii in enumerate(data):
    plt.plot(np.add(timeStamp[index],-t0), ii, colors[index]
            , label=("Temp: " + str(index)))

# Add legend to subplot
plt.legend()


# ======================ADC/ODO Sensor======================
plt.figure(2)
plt.clf()
plt.subplot(111)
plt.autoscale(True)
t0 = time.time()
plt.title("ODO (Latest data: %f)" % t0 )
plt.ylabel("Dat value (idk)")
plt.xlabel("Time (s)")

dataReading = []
dataTime = []

for ii in dbCol.find({"atype":"ODO"}):
    dataReading.append(ii["param"])
    dataTime.append( ii["ts"] - t0)

plt.plot(dataTime, dataReading, "g-")


plt.show()