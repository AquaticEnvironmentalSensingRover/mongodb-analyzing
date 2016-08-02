# Plots the sonar readings on a grayscale on the map of brickyard pond
# Black = deepest, white = shallowest
# Scale is set depending on the max and min values of the dataset
#NOTE: density plot or contour plot
#
# 160700 PTAG Show map look up
# 160802 RG Minor mods, make it work for Run 5 and look at temperature
#


import matplotlib.pyplot as plt
from pymongo import MongoClient
import lib.time_util as TimeUtil
from scipy.misc import imread
import lib.sensors.gps_tools as gt

import time
import datetime
from matplotlib.dates import DateFormatter

# Specify the run number you are looking at
runNumLoad = 5.2

# Assumes you use
# %run -i "/Users/gaitskel/GitHub/AESR/mongodb-analyzing/sonar_map_analyze.py"
# to rerun code to make use of existing data that is loaded

if ( ('runNum' in locals()) & ( runNum == runNumLoad) & ('data' in locals()) & ( size( data ) > 0 ) ) : # Shortcut - don't keep reloading data

    runNum = runNumLoad
    
    # Load a specific run, specified above
    mongo = MongoClient(host="localhost")
    if(runNum==0) :
        #print("Databases:\n" + str(mongo.database_names()))
        #db = raw_input("DB Name: ")
        db = 'AESR_20160629T185315'
        #print("\nCollections:\n" + str(mongo[db].collection_names()))
        #col = raw_input("Col Name: ")
        col = 'data'
        dbCol = (mongo[db])[col]
    elif(runNum==4) :
        tStartRun = time.mktime( datetime.datetime(2016, 7, 16, 18, 40).timetuple() )
        tStopRun = time.mktime( datetime.datetime(2016, 7, 16, 19, 30).timetuple() )
        dbCol = ( mongo['AESR_20160716T184018'] )['data']
    elif( (runNum>=5) & (runNum<6) ) :
        tStartRun = time.mktime( datetime.datetime(2016, 7, 17, 0, 0 ).timetuple() )
        tStopRun = time.mktime( datetime.datetime(2016, 7, 17, 23, 59 ).timetuple() )
        if runNum==5.1: dbCol = ( mongo['AESR_20160717T154442'] )['data'] 
        if runNum==5.2: dbCol = ( mongo['AESR_20160717T165349'] )['data'] 
        if runNum==5.3: dbCol = ( mongo['AESR_20160717T193309'] )['data'] 
        
    data = []
    dataTime = []
    dataLat = []
    dataLon = []
    randEpoch = None
    
    
    # Prepare the data from database
    if( runNum==0 ):
        for index, ii in enumerate(dbCol.find({"atype":"SONAR"})):
            if ii["param"] < 750:
                data.append(ii["param"]/100*4.3)
                dataTime.append(ii["ts"])        
            if index == 0:
                randEpoch = TimeUtil.EpochToDate(ii["ts"])
    elif( (runNum>=5) & (runNum<6) ) :
        for index, ii in enumerate(   dbCol.find({"atype":"TEMP" , "itype": 1})     ):
            data.append( ii["param"] )
            dataTime.append(ii["ts"])        
            if index == 0:
                randEpoch = TimeUtil.EpochToDate(ii["ts"])
            
    maxVal = max(data)
    minVal = min(data)
    
    ''' Method for extracting lat and long values closest to the times of the data taken'''
    gpsData = []
    for ii in dbCol.find({"atype":"GPS"}):
        gpsData.append(ii)
    
    
    for ii in dataTime:
        newGpsData = gt.nearestLocationFromTime(gpsData, ii, timeTag = "ts")
        dataLat.append(newGpsData["param"]["lat"])
        dataLon.append(newGpsData["param"]["lon"])
    
    for i in range(len(data)):
        data[i] = 1- (data[i] - minVal)/(maxVal-minVal)
        

# PLOT THE DATA ON A MAP

plt.figure(1)
plt.clf()
# Enable autoscaling
plt.autoscale(True)

for j in range(len(dataLat)):
    plt.plot( [dataLon[j]] , [dataLat[j]] , 'b.' , c=str(data[j]) )

plt.xlabel("Longitude (deg)")
plt.ylabel("Latitude (deg)")

if( runNum==0 ):
    plt.title(str(randEpoch) + ': Depth and Location')
#elif( (runNum>=5) & (runNum<6) ) :
#    plt.title('Run %.2f '%runNum + str(randEpoch) + ': Temperature Map')
    
# Disable autoscaling to stop images from affecting scale
plt.autoscale(False)

# Add Brick Yard Pond map
img = imread("maps/byp.jpg")
plt.imshow(img, zorder=0, extent=[-71.330371, -71.307692, 41.730781, 41.739235])

# LL 41.730781, -71.330371
# UR 41.739235, -71.307692


plt.show()
