import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient
from scipy.misc import imread
import time

mongo = MongoClient(host="10.0.2.189")

print("Databases:\n" + str(mongo.database_names()))
db = raw_input("DB Name: ")
print("\nCollections:\n" + str(mongo[db].collection_names()))
col = raw_input("Col Name: ")

dbCol = (mongo[db])[col]

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
lon = []
lat = []
for jj in dbCol.find({"atype":"GPS"}):
    lon.append((jj["param"])["lon"])
    lat.append((jj["param"])["lat"])

# Plot GPS data
plt.plot(lon, lat, "bo")

# Disable autoscaling to stop images from affecting scale
plt.autoscale(False)

# Add map background
img = imread("maps/map.jpg")
plt.imshow(img, zorder=0, extent=[-180, 180, -90, 90])

# Add house image in specific position
img = imread("maps/house.jpg")
plt.imshow(img, zorder=0, extent=[-71.343431, -71.342690, 41.739744, 41.740059])


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
    dataPressr.append( (ii["param"])["pressure"])
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

colors = ["r","g","b","c","k"]

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


# Show plot
plt.show()