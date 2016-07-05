import matplotlib.pyplot as plt
from pymongo import MongoClient
from scipy.misc import imread
import lib.analyze_util as au


mongo = MongoClient(host=au.serverAddressSelector())

dbCol = au.dbColSelector(mongo)

data = []

for jj in dbCol.find({"atype":"IGPS"}):
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
plt.imshow(img, zorder=0, extent=[-180, 180, -90, 90])

img = imread("maps/house.jpg")
plt.imshow(img, zorder=0, extent=[-71.343431, -71.342690, 41.739744, 41.740059])

#Center of the house should be located at   X -71.343310 , Y 41.739910,


#UL: 41.740019, -71.343472
#LL: 41.739744, -71.343431
#LR: 41.739802, -71.342680
#UR: 41.740059, -71.342690

# Plot the center of the house
plt.plot( -71.343310 , 41.739910 , 'rd' ) 

x, y=zip(*data)
plt.plot(x, y, "bo")
'''ax = plt.gca()
ax.invert_yaxis()'''

plt.show()