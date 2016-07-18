from pymongo import MongoClient
import lib.analyze_util as au
import matplotlib.pyplot as plt
from lib.time_util import TimeUtil
import lib.sensors.gps_tools as gt
import time
import datetime


mongo = MongoClient(host=au.serverAddressSelector())

dbCol = au.dbColSelector(mongo)

plt.figure(1)
plt.clf()

date = None

tStartRun004line = time.mktime( datetime.datetime(2016, 7, 16, 18, 55).timetuple() )
tStopRun004line = time.mktime( datetime.datetime(2016, 7, 16, 19, 13).timetuple() )

# extract GPS data from database and place in GPSData array
GPSData = []
for index, data in enumerate(dbCol.find({"atype":"GPS"})):
    GPSData.append(data)
    
    if index == 0:
        date = TimeUtil.EpochToDate(data["ts"])
    
# ============== Temperature ===============
# extract temp data - one array for each i type
# extract time for each temp data point
# using gps_tools create 3 new arrays with the lat points with the closest ts values

#plt.subplot(221)
plt.title(str(date) + ": Comparing Data at Same Lat Values, Shallow Water Temp")
plt.autoscale(True)

tempData0 = []
time0 = []
tempData1 = []
time1 = []
tempData2 = []
time2 = []

for temp in dbCol.find({"atype":"TEMP"}):
    tt = temp["ts"]
    if (tt >= tStartRun004line and tt <= tStopRun004line):
        if temp["itype"] == 0:
            tempData0.append(temp["param"])
            time0.append(temp["ts"])
        elif temp["itype"] == 1:
            tempData1.append(temp["param"])
            time1.append(temp["ts"])
        elif temp["itype"] == 2:
            tempData2.append(temp["param"])
            time2.append(temp["ts"])
          
lat0 = []
lat1 = []
lat2 = []

for tt in time0:
    lat0.append((gt.nearestLocationFromTime(GPSData, tt, timeTag = "ts")["param"]["lat"]))

for tt in time1:
    lat1.append((gt.nearestLocationFromTime(GPSData, tt, timeTag = "ts")["param"]["lat"]))
    
for tt in time2:
    lat2.append((gt.nearestLocationFromTime(GPSData, tt, timeTag = "ts")["param"]["lat"]))

#plt.title("Temp vs. Lat")
plt.xlabel("Latitude (deg)")
plt.ylabel("Temperature (C)")

#plt.plot(lat0, tempData0, 'ro', lat1, tempData1, 'bo', lat2, tempData2, 'go')
plt.plot(lat0, tempData0, 'r-')
plt.show()

plt.figure(2)
plt.clf()
plt.title(str(date) + ": Comparing Data at Same Lat Values, Air Temperature")
plt.autoscale(True)
plt.xlabel("Latitude (deg)")
plt.ylabel("Temperature (C)")
plt.plot(lat2, tempData2, 'b-')
plt.show()

plt.figure(3)
plt.clf()
plt.title(str(date) + ": Comparing Data at Same Lat Values, Deep Water Temperature")
plt.autoscale(True)
plt.xlabel("Latitude (deg)")
plt.ylabel("Temperature (C)")
plt.plot(lat1, tempData1, 'g-')
plt.show()


# ============= ODO ========================

# ============= Pressure ===================
presrData = []
presrTime = []

for data in dbCol.find({"atype":"PRESR"}):
    tt = data["ts"]
    if (tt >= tStartRun004line and tt <= tStopRun004line):
        presrData.append(data["param"]["mbar"])
        presrTime.append(data["ts"])
        
presrLat = []
for tt in presrTime:
    presrLat.append((gt.nearestLocationFromTime(GPSData, tt, timeTag = "ts")["param"]["lat"]))
    
plt.figure(4)
plt.clf()
plt.title(str(date) + ": Comparing Data at Same Lat Values, Pressure")
plt.autoscale(True)
plt.xlabel("Latitude (deg)")
plt.ylabel("Pressure (mbar)")
plt.plot(presrLat, presrData, 'm-')
plt.show()