import matplotlib.pyplot as plt
from pymongo import MongoClient
from scipy.misc import imread

db = "test_data3"
col = "gpsData"

mongo = MongoClient(host="10.0.2.81")

dbCol = (mongo[db])[col]

data = []

for jj in dbCol.find({"atype":"GPS"}):
    print(jj)
    data.append([ (jj["param"])["lon"], (jj["param"])["lat"] ])
    
# Plot data
plt.figure(1)
plt.autoscale(True)
plt.clf()
plt.title("Latest data")
#plt.axis([-180, 180, -90, 90])
plt.xlabel("Longitude (deg)")
plt.ylabel("Latitude (deg)")

img = imread("maps/map.jpg")
plt.imshow(img, zorder=0, extent=[-180, 180, 90, -90])

x, y=zip(*data)
plt.plot(x, y, "bo")
ax = plt.gca()
ax.invert_yaxis()

plt.show()