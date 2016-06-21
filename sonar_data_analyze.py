import matplotlib.pyplot as plt
from pymongo import MongoClient
import time

mongo = MongoClient(host="10.0.2.189")

print("Databases:\n" + str(mongo.database_names()))
db = raw_input("DB Name: ")
print("\nCollections:\n" + str(mongo[db].collection_names()))
col = raw_input("Col Name: ")

dbCol = (mongo[db])[col]

dataDepth = []
dataTime = []

t0 = time.time()

for ii in dbCol.find({"atype":"SONAR"}):
    dataDepth.append(ii["param"])
    dataTime.append( ii["ts"] - t0)

    
t0 = time.time()

# Plot data
plt.figure(1)
plt.clf()
plt.autoscale(True)
plt.title('Latest data %f: Depth/Distance vs. Time' % t0 )
plt.ylabel("Depth/Distance (cm)")
plt.xlabel("Time (s)")

plt.plot(dataTime, dataDepth, "mo")

plt.show()