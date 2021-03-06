# -*- coding: utf-8 -*-
# example_analyze_data_RG.py
# THIS IS A HEAVILY MODIFED VERSION OF "all_data_analyze.py"
# 160703 v2 RG Changing format of date printout to help with analysis after data taking
#  Modify formats for arrays to Numpy Arrays to allow subsequent analysis interactively
# 160704 RG FUrther mods
# 160706 RG Push to Git
# 160707 RG Edited,comments for clarity
# 160717 PTAG Edit for Run 4
# 160911 Looking at dissolved Oxygen Corrected Data
#
#

import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient
import lib.analyze_util as au
from scipy.misc import imread
import time
import datetime
from matplotlib.dates import DateFormatter

# For multiple y-axes
# http://matplotlib.org/examples/axes_grid/demo_parasite_axes2.html
from mpl_toolkits.axes_grid1 import host_subplot 
import mpl_toolkits.axisartist as AA 
import matplotlib.pyplot as plt

# Luc's library for defining which Run sets and databases - see set_mongo_values.py
import lib.database_util as du



# PICK SERVER OR USE PRESET
#mongo = MongoClient(host=au.serverAddressSelector())
#mongo = MongoClient( ) # local
#mongo = MongoClient(host="10.0.2.197")
#mongo = MongoClient(host="172.16.0.2")
# PICK COLLECTION
#dbCol = au.dbColSelector(mongo)

# Run004
#runNum = 5.2


mongo = MongoClient( **du.getServerHost() )
runNum = du.getRunNumber()
dbCols = du.getDbsCol(mongo)

# Cut the data for only that when on the lake
# Epoch times for start and stop


if(runNum==4) :
    tStartRun = time.mktime( datetime.datetime(2016, 7, 16, 18, 40).timetuple() )
    tStopRun = time.mktime( datetime.datetime(2016, 7, 16, 19, 30).timetuple() )
    # dbCol = ( mongo['AESR_20160716T184018'] )['data']
elif( (runNum>=5) & (runNum<6) ) :
    tStartRun = time.mktime( datetime.datetime(2016, 7, 17, 0, 0 ).timetuple() )
    tStopRun = time.mktime( datetime.datetime(2016, 7, 17, 23, 59 ).timetuple() )
    #if runNum==5.1: dbCol = ( mongo['AESR_20160717T154442'] )['data'] 
    #if runNum==5.2: dbCol = ( mongo['AESR_20160717T165349'] )['data'] 
    #if runNum==5.3: dbCol = ( mongo['AESR_20160717T193309'] )['data'] 
    


# Used to format the date/time axis
# formatter = DateFormatter('%H:%M:%S')
formatter = DateFormatter('%H:%M')




# ======================ODO======================:
# Get optical dissolved oxygen ADC:
odoCorrTimeList = []
odoCorrAdcList = []
for dbCol in dbCols:
    for ii in dbCol.find({"atype": "ODO"}):
        odoCorrTimeList.append(ii['ts'])
        odoCorrAdcList.append(ii['param']['rawADC'])

odoCorrTime = np.asarray(odoCorrTimeList)
odoCorrAdc = np.asarray(odoCorrAdcList)




# ======================GPS======================
plt.figure(100)
plt.clf()
#plt.subplot(221)


#t0 = time.time()

# Get GPS data
#gpsList = [("GPS","bo"), ("IGPS","r-")]
gpsList = [ ("GPS","b.") ]
for ii in gpsList:
    gpsLon = []  # lists
    gpsLat = []
    gpsTime = []
    for dbCol in dbCols:
        for jj in dbCol.find({"atype":ii[0]}):
            gpsLon.append((jj["param"])["lon"])  # appending to list is very easy
            gpsLat.append((jj["param"])["lat"])
            gpsTime.append( jj["ts"] )
        
# Convert the lists to Numpy ndarray for later use
gpsLat = np.array( gpsLat )   # now convert to ndarray for later analysis
gpsLon = np.array( gpsLon )
gpsTime = np.array( gpsTime )

                
# Plot GPS data
plt.title("GPS (Run: %.2f)" % runNum  )
plt.xlabel("Longitude (deg)")
plt.ylabel("Latitude (deg)")

# Enable autoscaling
plt.autoscale(True)

# Plot the center of the house
# plt.plot( -71.343310 , 41.739910 , 'rd' ) 
        
plt.plot(gpsLon, gpsLat , 'b.' )

# Disable autoscaling to stop images from affecting scale
plt.autoscale(False)

# Add map background
img = imread("maps/map.jpg")
plt.imshow(img, zorder=0, extent=[-180, 180, -90, 90])

# Add house image in specific position
if False:
    img = imread("maps/house.jpg")
    plt.imshow(img, zorder=0, extent=[-71.343431, -71.3424, 41.739744, 41.740059])

# Add zoomed-out house image in specific position
    img = imread("maps/house2.jpg")
    plt.autoscale(True)
    plt.imshow(img, zorder=0, extent=[-71.34516, -71.34072, 41.738835, 41.740670])
    plt.autoscale(False)

# UL 41.740657, -71.345162
# LL 41.738835, -71.345169
# UR 41.740670, -71.340646
# LR 41.738851, -71.340643

# Add Brick Yard Pond map
img = imread("maps/byp.jpg")
plt.imshow(img, zorder=0, extent=[-71.330371, -71.307692, 41.730781, 41.739235])

# LL 41.730781, -71.330371
# UR 41.739235, -71.307692

# ZOOM IN 

if runNum==4 :
    plt.figure(1000)
    plt.clf()
    
    tStartRunline = time.mktime( datetime.datetime(2016, 7, 16, 18, 55).timetuple() )
    tStopRunline = time.mktime( datetime.datetime(2016, 7, 16, 19, 13).timetuple() )
    
    cut = (     ( gpsTime >= tStartRun )    &     (gpsTime <= tStopRun)      ) # Make a cut
    plt.plot(gpsLon[cut], gpsLat[cut] , 'r.' )
    
    cut = (     ( gpsTime >= tStartRunline )    &     (gpsTime <= tStopRunline )      ) # Make a cut
    plt.plot(gpsLon[cut], gpsLat[cut] , 'y.' )


# ======================PRESSURE======================
t0 = time.time()

# Start with lists
pressrValue = []
pressrTime = []

for dbCol in dbCols:
    for ii in dbCol.find({"atype":"PRESR"}):
        pressrValue.append( (ii["param"])["mbar"])
        pressrTime.append( ii["ts"] )

# Convert the lists to Numpy ndarray for later use
pressrValue = np.array( pressrValue )
pressrTime = np.array( pressrTime )

plt.figure(14)
plt.clf()
plt.autoscale(True)
plt.title("Pressure vs. Time (Run: %f)" % runNum )
plt.ylabel("Pressure (mbar)")
plt.xlabel("Time (s)")

plt.plot(pressrTime, pressrValue, "ro")

# ======================PRESSUE HISTOGRAM======================

plt.figure(114); plt.clf( )
plt.hist( pressrValue , bins = 100 )
plt.title("Pressure vs. Time (Run: %f)" % runNum )
plt.xlabel("Pressure (mbar)")
plt.ylabel("Counts (s)")



# ======================SONAR======================
if False:
    plt.figure(15)
    plt.autoscale(True)
    t0 = time.time()
    plt.title("Depth/Distance vs. Time (Latest data: %f)" % t0 )
    plt.ylabel("Depth/Distance (cm)")
    plt.xlabel("Time (s)")
    
    depthValue = []
    depthTime = []
    
    for dbCol in dbCols:
        for ii in dbCol.find({"atype":"SONAR"}):
            depthValue.append(ii["param"])
            depthTime.append( ii["ts"] - t0)
    
    plt.plot(depthTime, depthValue, "mo")
    
    # Convert the lists to Numpy ndarray for later use
    depthValue = np.array( depthValue )
    depthTime = np.array( depthTime )


# ======================TEMPERATURE======================
#plt.figure(1)
#plt.subplot(224)
plt.figure(2)
plt.clf()

plt.autoscale(True)
t0 = time.time()
plt.title("Temperature (Run data: %.2f)" % runNum )
#plt.axis([-100, 5, 22, 26])
plt.ylabel("Temperature (degC)")
plt.xlabel("Time (s)")

colors = ["r-","g-","b-","c-","k-"]
# colors = ["ro","go","bo","co","ko"]

sensorAmount = 5

timeStamp = []
data = []

for ii in range(sensorAmount):  # Loop through all 5 thermometers
    newTimeStamp = []
    newData = []
    for dbCol in dbCols:
        for jj in dbCol.find({"atype":"TEMP", "itype":ii}):
            newTimeStamp.append(jj["ts"])
            newData.append(jj["param"])
    
    timeStamp.append(newTimeStamp)
    data.append(newData)
    
# Create ndarrays - each row is epoch time, temp # , or value
#tempTime = np.empty((0,),dtype=float)
#tempIndex = np.empty((0,),dtype=int)
#tempValue = np.empty((0,),dtype=float)

# tempIndex
# 0 - Short Cable with ODO
# 1 - 1m next to pressure
# 2 - Air temperature
    
# Make Numpy version    
tempTime = []
tempIndex = []
tempValue = []

for dbCol in dbCols:
    for ii in dbCol.find({"atype":"TEMP"}):
        tempTime.append( ii["ts"])
        tempIndex.append(ii["itype"])
        tempValue.append(ii["param"])

# Convert the lists to Numpy ndarray for later use
tempTime = np.array( tempTime )
tempValue = np.array( tempValue )
tempIndex = np.array( tempIndex )



for index, ii in enumerate(data):
    # Usual plot in seconds from now
    # plt.plot(np.add(timeStamp[index],-t0), ii, colors[index]
    #        , label=("Temp: " + str(index)))

    # Plot with date stamp
    plt.plot( [ datetime.datetime.fromtimestamp(x) for x in timeStamp[index] ]
    , ii 
    , colors[index] 
    , label=("Temp: " + str(index))
    )
    plt.gcf().axes[0].xaxis.set_major_formatter(formatter)

# Add legend to subplot
plt.legend()


# ======================ADC/ODO Sensor======================
plt.figure(3)
plt.clf()
plt.subplot(111)
plt.autoscale(True)
t0 = time.time()
plt.title("ODO (Latest data: %f)" % t0 )
plt.ylabel("Dat value (mg/L)")
plt.xlabel("Time (s)")

odoConcentration = [] # mg/L
odoTime = []

for dbCol in dbCols:
    for ii in dbCol.find({"atype":"ODO"}):
        odoConcentration.append(ii["param"]["mgL"])
        odoTime.append( ii["ts"] - t0)

plt.plot(odoTime, odoConcentration, "g-")


plt.show()



# =============== NEW ADDITIONAL PLOTS WITH NEW NP VARIABLES ===============
# DEMONSTRATES USE OF CUTS IN DATA

# 160704 RG 

# global gpsLat,gpsLon,gpsTime

# print np.shape( gpsLat )
# Force them to be numpy arrays - logic below won't work on simple lists
#gpsLat = np.array( gpsLat )
#gpsLon = np.array( gpsLon )
#gpsTime = np.array( gpsTime )

formatter = DateFormatter('%H:%M:%S')


# Show all the gps data
plt.figure(14) 
if False :
    plt.clf()
    plt.plot( [ datetime.datetime.fromtimestamp(x) for x in gpsTime ], gpsLat , 'r.' )
    plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
    plt.title("Latitude (Latest data: %f)" % t0 )
    plt.ylabel("Latitude")
    plt.xlabel("Time (s)")
else :
    plt.close(14)


# Show  the gps data within a certain time range
plt.figure(15)
if False :
    plt.clf()
    cut = ( ( gpsTime >= tStartRun ) & (gpsTime <= tStopRun) ) # Make a cut
    plt.plot(  [ datetime.datetime.fromtimestamp(x) for x in (gpsTime[ cut ]) ]  , gpsLat[  cut ]  , 'r.' )
    plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
    plt.title("Latitude (Latest data: %f)" % t0 )
    plt.ylabel("Latitude")
    plt.xlabel("Time (s)")
else :
    plt.close(15)

# Show the 1 m temperature data and the pressure depth
plt.figure(16)
if False :
    plt.clf()
    
    plt.subplot('211')
    plt.title("Temperature & Pressure (Run: %.2f)" % runNum )

    # Temperature
    cutTime = ( ( tempTime >= tStartRun ) & (tempTime <= tStopRun) ) # Make a cut

    cut = cutTime & (tempIndex == 1) # 1 m depth data
    plt.plot(  [ datetime.datetime.fromtimestamp(x) for x in (tempTime[ cut ]) ]  , tempValue[  cut ]  , 'r.' , markersize = 1 )

    cut = cutTime & (tempIndex == 0) # Surface
    plt.plot(  [ datetime.datetime.fromtimestamp(x) for x in (tempTime[ cut ]) ]  , tempValue[  cut ]  , 'g.' , markersize = 1 )

    plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
    plt.xlabel("Time")
    plt.ylabel("T (degC)")

    plt.subplot('212')
    # Depth Pressure
    cut = ( ( pressrTime >= tStartRun ) & (pressrTime <= tStopRun) ) # Make a cut
    plt.plot(  [ datetime.datetime.fromtimestamp(x) for x in (pressrTime[ cut ]) ]  , -(pressrValue[  cut ]-1020)/100  , 'b.' , markersize = 1 )
    plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
    plt.xlabel("Time")
    # plt.ylabel("P (mbar)")
    plt.ylabel("Depth (m)")
      
else :
    plt.close(16)

plt.show()



# Show the 1 m temperature data and the pressure depth on same graph
ff = 17

plt.figure(ff)
if False :
    plt.clf()
    
    # http://matplotlib.org/examples/axes_grid/demo_parasite_axes2.html
    host = host_subplot(111, axes_class=AA.Axes)
    plt.subplots_adjust(right=0.75)

# y-axis on right
    par1 = host.twinx()

# If we need a third y-axis
#    par2 = host.twinx()

#    offset = 60
#    new_fixed_axis = par2.get_grid_helper().new_fixed_axis
#    par2.axis["right"] = new_fixed_axis(loc="right",
#                                        axes=par2,
#                                        offset=(offset, 0))

#    par2.axis["right"].toggle(all=True)

    plt.title("Temperature & Pressure (Run: %.2f)" % runNum )

#    host.set_xlim(0, 2)
#    host.set_ylim(0, 2)

    host.set_xlabel("Time")
    host.set_ylabel("Temperature")
    par1.set_ylabel("Depth")
#    par2.set_ylabel("Velocity")

#    par1.set_ylim(0, 4)
#    par2.set_ylim(1, 65)

    # Temperature
    cutTime = ( ( tempTime >= tStartRun ) & (tempTime <= tStopRun) ) # Make a cut

    cut = cutTime & (tempIndex == 1) # 1 m depth data
    plt.plot(  [ datetime.datetime.fromtimestamp(x) for x in (tempTime[ cut ]) ]  , tempValue[  cut ]  , 'r.' , markersize = 1 )

    p1, = host.plot( 
        [ datetime.datetime.fromtimestamp(x) for x in (tempTime[ cut ]) ]  
        , tempValue[  cut ] 
        , label="T (degC)"
        )

#    p3, = par2.plot([0, 1, 2], [50, 30, 15], label="Velocity")


#    cut = cutTime & (tempIndex == 0) # Surface
#    plt.plot(  [ datetime.datetime.fromtimestamp(x) for x in (tempTime[ cut ]) ]  , tempValue[  cut ]  , 'g.' , markersize = 1 )


    # Depth Pressure
    cut = ( ( pressrTime >= tStartRun ) & (pressrTime <= tStopRun) ) # Make a cut
    p2, = par1.plot( 
        [ datetime.datetime.fromtimestamp(x) for x in (pressrTime[ cut ]) ]  
        , -(pressrValue[  cut ]-1020)/100 
        , label="Depth (m)"
        )
#    plt.plot(  [ datetime.datetime.fromtimestamp(x) for x in (pressrTime[ cut ]) ]  , -(pressrValue[  cut ]-1020)/100  , 'b.' , markersize = 1 )
#    plt.ylabel("Depth (m)")

    #plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
    
    plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
    plt.xlabel("Time")
    plt.ylabel("T (degC)")
    
    host.legend()

    host.axis["left"].label.set_color(p1.get_color())
    par1.axis["right"].label.set_color(p2.get_color())
#    par2.axis["right"].label.set_color(p3.get_color())
      
else :
    plt.close(ff)

plt.draw()
plt.show()

#plt.savefig("Test")





# Using - nearestPairsFromTimes(baseTimes, baseVals, targetTime , maximumTimeDiff=None):
# Show the 1 m temperature data and the pressure depth
ff = 18
plt.figure(ff)
if False :
    plt.clf()
    
    plt.title("Temperature & Pressure (Run: %.2f)" % runNum )

    # Temperature
    #cutTime = ( ( tempTime >= tStartRun ) & (tempTime <= tStopRun) ) # Make a cut

    #cut = cutTime & (tempIndex == 1) # 1 m depth data
    #plt.plot(  [ datetime.datetime.fromtimestamp(x) for x in (tempTime[ cut ]) ]  , , 'r.' , markersize = 1 )

    # Depth Pressure
    cut = ( ( pressrTime >= tStartRun ) & (pressrTime <= tStopRun) ) # Make a cut
    tt = pressrTime[ cut ]
    d =  -(pressrValue[  cut ]-1020)/100

    cut = (tempIndex == 1) # 1 m depth data
    temp = au.nearestPairsFromTimes( tempTime[cut].tolist() , tempValue[cut].tolist() , tt.tolist() , 3 )
    plt.plot(  temp  , d  , 'b.' , markersize = 3 )

    plt.ylabel("Depth (m)")
    plt.xlabel("T (degC)")
      
else :
    plt.close(ff)

plt.show()



# ==========================================================
# MAKE A CORRECTION TO   ODO  DUE TO ADC INPUT MISTAKE
# 
 
ff = 19
plt.figure(ff)
if False :
    plt.clf()
    plt.title("ADC (Run: %.2f)" % runNum )

    # ADC
    cutTime = ( ( odoCorrTime >= tStartRun ) & (odoCorrTime <= tStopRun) ) # Make a cut
    cut = cutTime

    plt.plot( [ datetime.datetime.fromtimestamp(x) for x in (odoCorrTime[ cut ]) ]  , odoCorrAdc[ cut ] , 'r.' )
    plt.ylabel("ADC")
    plt.xlabel("Time")
      
else :
    plt.close(ff)

# 160910 LCOG / RG
# Linear correction of ADC reading into volts needs to create that reading 
# (when ADC is incorrectly set to Diff Input FS +/-4.0V but only INPUT0 is connected with INPUT1 floating)
# See Google Spreadsheet   https://docs.google.com/spreadsheets/d/1cGLoH5cN5xOTv3Kym1i6xxTGEeZmTAHXD81e3mx0zYE/edit#gid=2060652824
m = 1. / ( 7.808 )  # 7.808 ADC bins/mV
c = 573.46 # 573.46 mV for an ADC reading of 0
odoCorrVolt = m * odoCorrAdc + c

# 160910 LCOG / RG
# Voltage to mg/L value
# http://www.vernier.com/manuals/odo-bta/#section7
# Default software calibration values (mg/L)
#slope: 4.444
#intercept: –0.4444
m = 4.444e-3  # 4.444e-3 (mg/L) / millivolt
c = -0.4444 # (mg/L)
odoCorrConcentration = m * odoCorrVolt + c   #(mg/L)

# 160910 LCOG / RG
# Temperature corresponding to ODO measurement and the expected Saturated ODO for that temperature
#   https://docs.google.com/spreadsheets/d/1YGhftt8NhKRW-xAtrbqHCD3r475q2NzWm7DT7LLnwFs/edit#gid=0
#   http://www.vernier.com/files/manuals/odo-bta.pdf
#
#


ff = 20
plt.figure(ff)
if True :
    plt.clf()
    plt.title("ADC (Run: %.2f)" % runNum )

    # ADC
    cutTime = ( ( odoCorrTime >= tStartRun ) & (odoCorrTime <= tStopRun) ) # Make a cut
    cut = cutTime
    plt.xlabel("Time")

    if False:
        plt.plot( [ datetime.datetime.fromtimestamp(x) for x in (odoCorrTime[ cut ]) ]  , odoCorrAdc[ cut ] , 'r.' )
        plt.ylabel("ADC")

    if True:
        plt.plot( [ datetime.datetime.fromtimestamp(x) for x in (odoCorrTime[ cut ]) ]  , odoCorrConcentration[ cut ] , 'r.' )
        plt.ylabel("Corrected Concentration (mg/L)")
            
else :
    plt.close(ff)

plt.show()




# Using - nearestPairsFromTimes(baseTimes, baseVals, targetTime , maximumTimeDiff=None):
# Use ODO temperature
ff = 21
plt.figure(ff)
if True :
    plt.clf()
    
    plt.title("Temperature & DO (Run: %.2f)" % runNum )

    # Temperature sensor next to ODO
    cutT = ( ( tempTime >= tStartRun ) & (tempTime <= tStopRun) ) # Make a cut of useful Run data
    cutO = ( ( odoCorrTime >= tStartRun ) & (odoCorrTime <= tStopRun) ) # Make a cut of useful Run data

    # Find the temperatures at the times of the ODO
    temp = au.nearestPairsFromTimes( 
        tempTime[cutT & (tempIndex == 0)].tolist() # All avaialble temp times
        , tempValue[cutT & (tempIndex == 0)].tolist() # All avaialble temp vallues
        , odoCorrTime[cutO].tolist() # Times of the ODO data we want find temperature values for
        , 3 )
    
    # 100% Oxygen Reference
    # au.concDisOxySaturated(740.,20.)

    plt.plot(  odoCorrTime[cutO]  , [ au.concDisOxySaturated(760., x ) for x in temp ] , 'b.' , markersize = 3 )

    plt.ylabel("Concentration 100% (mg/L)")
    plt.ylabel("T (degC)")
    plt.xlabel("Date")
      
else :
    plt.close(ff)

plt.show()
