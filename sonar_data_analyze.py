import matplotlib.pyplot as plt
from pymongo import MongoClient
import time
import lib.analyze_util as au


mongo = MongoClient(host=au.serverAddressSelector())

dbCol = au.dbColSelector(mongo)

t0 = time.time()

dataDepth = []
dataTime = []

for ii in dbCol.find({"atype":"SONAR"}):
    dataDepth.append(ii["param"])
    dataTime.append( ii["ts"] - t0)


# Plot data
plt.figure(1)
plt.clf()
plt.autoscale(True)
plt.title('Latest data %f: Depth/Distance vs. Time' % t0 )
plt.ylabel("Depth/Distance (cm)")
plt.xlabel("Time (s)")

plt.plot(dataTime, dataDepth, "mo")

plt.show()