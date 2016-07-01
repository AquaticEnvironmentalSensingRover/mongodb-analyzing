import time
import datetime

class TimeUtil:
    '''Static functions for converting time related functions'''
    
    # method for converting between epoch time to datetime format (Y-M-D H:M:S.s)
    # epoch: number of seconds since January 0th, 1970, T00:00
    @staticmethod
    def EpochToDateTime(epoch):
        return datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S.%f')
    
    # method for converting between epoch time to a standard time format (H:M:S.s)
    # use only if data is mentioned in analysis method
    @staticmethod    
    def EpochToTime(epoch):
        return datetime.datetime.fromtimestamp(epoch).strftime('%H:%M:%S.%f')
    
    # method for converting between datetime and epoch form  
    @staticmethod
    def DateTimeToEpoch(dateTime):
        return time.mktime(dateTime.timetuple()) + dateTime.microsecond * 1e-6