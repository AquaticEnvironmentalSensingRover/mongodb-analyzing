import matplotlib.pyplot as plt
from pymongo import MongoClient
import time

mongo = MongoClient(host="10.0.2.189")

print("Databases:\n" + str(mongo.database_names()))
db = raw_input("DB Name: ")
print("\nCollections:\n" + str(mongo[db].collection_names()))
col = raw_input("Col Name: ")

dbCol = (mongo[db])[col]

data = []
dataPressr = []
dataTime = []

t0 = time.time()

for ii in db.find({"atype":"PRESR"}):
    dataPressr.append( (ii["param"])["mbar"])
    dataTime.append( ii["ts"] - t0)

data.append(dataPressr, dataTime)
    
t0 = time.time()

# Plot data
plt.figure(1)
plt.clf()
plt.title('Latest data %f: Pressure vs. Time' % t0 )
plt.axis([-100, 5, 22, 26])
plt.ylabel("Pressure (mbar)")
plt.xlabel("Time (s)")

plt.plot(data, "ro")

plt.show()