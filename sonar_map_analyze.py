# Plots the sonar readings on a grayscale on the map of brickyard pond
# Black = deepest, white = shallowest
# Scale is set depending on the max and min values of the dataset
#NOTE: density plot or contour plot

import matplotlib.pyplot as plt
from pymongo import MongoClient
from lib.time_util import TimeUtil
from scipy.misc import imread
import lib.sensors.gps_tools as gt

mongo = MongoClient(host="localhost")

#print("Databases:\n" + str(mongo.database_names()))
#db = raw_input("DB Name: ")
db = 'AESR_20160629T185315'
#print("\nCollections:\n" + str(mongo[db].collection_names()))
#col = raw_input("Col Name: ")
col = 'data'

dbCol = (mongo[db])[col]

data = []
dataTime = []
dataLat = []
dataLon = []
randEpoch = None

plt.figure(1)
plt.clf()
# Enable autoscaling
plt.autoscale(True)

for index, ii in enumerate(dbCol.find({"atype":"SONAR"})):
    if ii["param"] < 750:
        data.append(ii["param"]/100*4.3)
        dataTime.append(ii["ts"])
    
    if index == 0:
        randEpoch = TimeUtil.EpochToDate(ii["ts"])

maxVal = max(data)
minVal = min(data)

''' Method for extracting lat and long values closest to the times of the data taken'''
gpsData = []
for ii in dbCol.find({"atype":"GPS"}):
    gpsData.append(ii)


for ii in dataTime:
    newGpsData = gt.nearestLocationFromTime(gpsData, ii, timeTag = "ts")
    dataLat.append(newGpsData["param"]["lat"])
    dataLon.append(newGpsData["param"]["lon"])

for i in range(len(data)):
    data[i] = 1- (data[i] - minVal)/(maxVal-minVal)
    
for j in range(len(dataLat)):
    plt.plot([dataLon[j]], [dataLat[j]], 'bo', c=str(data[j]))



plt.xlabel("Longitude (deg)")
plt.ylabel("Latitude (deg)")
plt.title(str(randEpoch) + ': Depth and Location')

# Disable autoscaling to stop images from affecting scale
plt.autoscale(False)

# Add Brick Yard Pond map
img = imread("maps/byp.jpg")
plt.imshow(img, zorder=0, extent=[-71.330371, -71.307692, 41.730781, 41.739235])

# LL 41.730781, -71.330371
# UR 41.739235, -71.307692


plt.show()