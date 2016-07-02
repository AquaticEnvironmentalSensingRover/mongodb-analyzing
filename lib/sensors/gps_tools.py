def nearestLocationFromTime(gpsData, time, timeTag = "ts"):
    minimumTimeData = None
    for ii in gpsData:
        if not minimumTimeData == None:
            if abs(minimumTimeData[timeTag]-time) > abs(ii[timeTag]-time):
                minimumTimeData = ii
        else:
            minimumTimeData = ii
        
    return minimumTimeData