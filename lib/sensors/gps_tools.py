# gps_tools.py
# 
# 160802 RG Started adding time pairing method, but Luc has provided new routine
#
#

def nearestLocationFromTime(gpsData, time, timeTag = "ts"):
    minimumTimeData = None
    for ii in gpsData:
        if not minimumTimeData == None:
            if abs(minimumTimeData[timeTag]-time) > abs(ii[timeTag]-time):
                minimumTimeData = ii
        else:
            minimumTimeData = ii
        
    return minimumTimeData
    
# time1, time2 is 1D array of times
# value1,value2 is 1D array of corresponding measurements, respectively
# Returns simple 1D arrays of piared data closest in time value1out and value2out    
# Data has to be closer than minTime to be paired
# 160802 RG
#
#def pairDataFromTime(time1, value1 , time2 , value2 , minTime):
#    value1out = [] ; value2out = []

#    for (i1,t1) in enumerate(time1):
#       minPairTime = abs( time2[0] - t1 )
#        minPairIndex = abs( time2[0] - t1 )
        
#        for t2 in time2:
#            if abs( t2-t1 ) < minTimePair:
#                minimumTimeData = ii
#        else:
#            minimumTimeData = ii
        
#    return ( timeOut . value1Out , value2Out )

