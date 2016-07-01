import matplotlib.pyplot as plt
import matplotlib.dates as dates
from pymongo import MongoClient
import time
from lib.time_util import TimeUtil
from matplotlib.dates import DateFormatter

mongo = MongoClient(host="localhost")
formatter = DateFormatter('%H:%M:%S')

print("Databases:\n" + str(mongo.database_names()))
db = raw_input("DB Name: ")
print("\nCollections:\n" + str(mongo[db].collection_names()))
col = raw_input("Col Name: ")

dbCol = (mongo[db])[col]

t0 = time.time()

dataDepth = []
dataTime = []
randEpoch = None

for index, ii in enumerate(dbCol.find({"atype":"SONAR"})):
    dataDepth.append((ii["param"])/100*4.3)
    dataTime.append(dates.datestr2num(TimeUtil.EpochToTime(ii["ts"])))
    
    if index == 0:
        randEpoch = TimeUtil.EpochToDate(ii["ts"])

# Plot data
plt.figure(1)
plt.clf()
plt.autoscale(True)
plt.title(str(randEpoch) + ': Depth vs. Time')
plt.ylabel("Depth (m)")
plt.xlabel("Time")
plt.gcf().axes[0].xaxis.set_major_formatter(formatter)  
plt.xticks(rotation=45)

plt.plot_date(dataTime, dataDepth, "ko")

plt.show()