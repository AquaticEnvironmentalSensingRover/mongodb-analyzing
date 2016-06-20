import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from pymongo import MongoClient

db = "test_data4"
col = "readData"

mongo = MongoClient(host="10.0.2.81")

dbCol = (mongo[db])[col]

data = []

for jj in dbCol.find({"atype":"GPS"}):
    data.append([ (jj["param"])["lon"], (jj["param"])["lat"] ])
    
print data
x, y=zip(*data)
# Plot data
fig = plt.figure()


'''
         llcrnrlon = 41.730556,           # lower-left corner longitude
         llcrnrlat = -71.346944,            # lower-left corner latitude
         urcrnrlon =41.745278,            # upper-right corner longitude
         urcrnrlat = -71.310833,               # upper-right corner latitude
         Coordinates for string below \/ - currently breaks map
'''
themap = Basemap(projection = "gall",
         resolution = 'i', #detail level (C,L,M,H,F)
         area_thresh = 0, #
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