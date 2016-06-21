import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from pymongo import MongoClient
import time

mongo = MongoClient(host="10.0.2.189")

print("Databases:\n" + str(mongo.database_names()))
db = raw_input("DB Name: ")
print("\nCollections:\n" + str(mongo[db].collection_names()))
col = raw_input("Col Name: ")

previousTime = time.time() # Used to find time spent on loading MongoDB server

dbCol = (mongo[db])[col]

data = []

for jj in dbCol.find({"atype":"GPS"}):
    data.append([ (jj["param"])["lon"], (jj["param"])["lat"] ])
    
print data

print ("==============================\n The Initialization and Read of the"
        + " database took " + str(time.time()-previousTime) + " seconds")

previousTime = time.time() # Used to find time rendering plot

x, y=zip(*data)
# Plot data
fig = plt.figure(1)
fig.clf()

themap = Basemap(projection = "gall",
                resolution = 'i', #detail level (C,L,M,H,F)
                area_thresh = 0,
                llcrnrlon = -71.5,           # lower-left corner longitude
                llcrnrlat = 41.3,            # lower-left corner latitude
                urcrnrlon = -71.1,            # upper-right corner longitude
                urcrnrlat = 41.9               # upper-right corner latitude
                )
              
themap.drawcoastlines()
themap.drawcountries()
themap.fillcontinents(color = 'gainsboro')
themap.drawmapboundary(fill_color='steelblue')

x, y = themap(x, y)
themap.plot(x, y, 
            'o',                    # marker shape
            color='Indigo',         # marker colour
            markersize=4            # marker size
            )


plt.show()

print("That plot took " + str(time.time()-previousTime) + " seconds")