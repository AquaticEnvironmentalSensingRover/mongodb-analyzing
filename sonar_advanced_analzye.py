import matplotlib.pyplot as plt
import matplotlib.dates as dates
from pymongo import MongoClient
import time
import lib.time_util
from matplotlib.dates import DateFormatter

from sonar_manual_data import *        

mongo = MongoClient(host="localhost")
formatter = DateFormatter('%H:%M:%S')

#print("Databases:\n" + str(mongo.database_names()))
# db = raw_input("DB Name: ")
db = 'AESR_20160629T185315'
#print("\nCollections:\n" + str(mongo[db].collection_names()))
#col = raw_input("Col Name: ")
col = 'data'

dbCol = (mongo[db])[col]

# t0 = time.time()

scaleAirCmToWaterM = 1./100.*4.3
dataDepth = []
dataTime = []
randEpoch = None

for index, ii in enumerate(dbCol.find({"atype":"SONAR"})):
    
    if ii["param"] < 750: # Values >= 750 are bad read 
        dataDepth.append((ii["param"]) * scaleAirCmToWaterM )
        dataTime.append(TimeUtil.EpochToTime(ii["ts"]))
        
        if index == 0:
            randEpoch = TimeUtil.EpochToDate(ii["ts"])
            
 
mdataStandardDate = np.array( [ TimeUtil.EpochToTime(tt) for tt in mdataDateEpoch ] )    
                
            

# Plot data
plt.figure(1)
plt.clf()
plt.autoscale(True)
plt.title(str(randEpoch) + ': Depth vs. Time')
plt.ylabel("Depth (m)")
plt.xlabel("Time")
plt.gcf().axes[0].xaxis.set_major_formatter(formatter)  
plt.xticks(rotation=45)

mtop=25; mbot = 0
plt.plot_date(dataTime, dataDepth, "ko")
plt.plot_date(mdataStandardDate, mdataDepth, 'ro')
for x in mdataStandardDate :
    plt.plot_date([x , x], [mbot,mtop],'r--' ) 

plt.show()