import numpy as np
import datetime
import time

mdata = [['6-29-2016/17:56:00',  5.5],['6-29-2016/18:09:00', 8.0],['6-29-2016/18:14:00', 10.8],['6-29-2016/18:23:00', 8.6],['6-29-2016/19:11:00', 6.8],['6-29-2016/19:16:45', 10.0],['6-29-2016/19:20:25',  17.8],['6-29-2016/19:22:50', 17.0],['6-29-2016/19:25:40', 70.3],
['6-29-2016/19:30:00', 70.3],['6-29-2016/19:33:45', 9.8],['6-29-2016/19:39:40', 10.8],['6-29-2016/19:44:50', 79.0],['6-29-2016/19:53:25', 73.4],['6-29-2016/19:57:30', 73.3],['6-29-2016/20:04:00', 9.5]]

# Create np arrays for data
mdataDate =  np.array( zip(*mdata)[0] )
mdataDepth =  0.3048 * np.array( zip(*mdata)[1] )  # Depth in meters

# Drop first four points
mdataDate = mdataDate[4:]
mdataDepth = mdataDepth[4:]

mdataDateEpoch = np.array( [ 
    time.mktime( datetime.datetime.strptime( date , '%m-%d-%Y/%H:%M:%S').timetuple() ) 
        for date in mdataDate ] )
