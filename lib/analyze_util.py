"""
Contain methods useful when analyzing data.

160911 RG Include Oxygen Saturation Function

"""
from geopy.distance import vincenty
import numpy as np
import numbers
import database_util as du
import warnings
warnings.simplefilter('once', DeprecationWarning)


# Private:
def _raiseIfWrongType(value, valueName, *targetTypes):
    isType = False
    for targetType in targetTypes:
        if isinstance(value, targetType):
            isType = True
            break

    if not isType:
        if len(targetTypes) == 1:
            errorMessage = ("The '{}' value is required to be a '{}' type"
                            .format(valueName, targetTypes[0].__name__))
        else:
            errorMessage = ("The '{}' value is required to be a "
                            .format(valueName))
            for ii, targetType in enumerate(targetTypes):
                if ii == len(targetTypes)-1:
                    newString = "or '{}'"
                else:
                    newString = "'{}', "

                errorMessage += newString.format(targetType)

        raise TypeError(errorMessage)


def _convertToNPArray(value):
    if not isinstance(value, np.ndarray):
        value = np.asarray(value)
    return value


# Deprecated redirects:
def serverAddressSelector(*args, **kwargs):
    """Return output of 'database_util.serverAddressSelector'.

    This keeps backwards compatibilty.
    """
    warnings.warn("Please use 'database_util' directly", DeprecationWarning)
    return du.serverAddressSelector(*args, **kwargs)


def dbColSelector(*args, **kwargs):
    """Return output of 'database_util.dbColSelector'.

    This keeps backwards compatibilty.
    """
    warnings.warn("Please use 'database_util' directly", DeprecationWarning)
    return du.dbColSelector(*args, **kwargs)


# Other:
def nearestIndexTime(times, targetTime, maximumTimeDiff=None):
    """Return the index in the 'times' list that was closest to 'targetTime'.

    The index of the closest value in 'times' to 'targetTime' is returned,
        unless 'maximumTimeDiff' was specified and the closest time value was
        further away from the 'targetTime' than it specified. In that case,
        None is returned.

    Args:
        times (list, numpy.array): The list of numeric time values used to find
            the closest.
        targetTime (numbers.Number): The time value that is being used to find
            the closest value in 'times'.
        maximumTimeDiff (None, numbers.Number): The maximum distance between
            the 'targetTime' and the closest value in 'times' (defaults to
            'None').

    Returns:
        None: If no closest time because of empty 'times' array or all
            values are further away then 'maximumTimeDiff'.
        int: The index in the 'times' array of the closest value.
    """
    _raiseIfWrongType(times, 'times', list, np.ndarray)
    times = _convertToNPArray(times)

    _raiseIfWrongType(targetTime, 'targetTime', numbers.Number)

    _raiseIfWrongType(maximumTimeDiff, 'maximumTimeDiff', numbers.Number,
                      type(None))

    diffArray = np.abs(times-targetTime)
    valueIndex = diffArray.argmin()

    if diffArray[valueIndex] <= maximumTimeDiff or maximumTimeDiff is None:
        return valueIndex
    else:
        return None


def nearestPairsFromTimes(baseTimes, baseVals, targetTimes,
                          maximumTimeDiff=None):
    """Return a list of values in baseVals that corrospond to the times lists.

    The closest 'base time' to each 'target time' is found, then an array
        containing the corrosponding 'base values' for the closest 'base times'
        is returned.

    The 'bastTimes' and 'baseVals' have to be the same length as they are the
        two 1D arrays of a 2D array.

    Args:
        baseTimes (list): The list of numeric time values used to find the
            closest.
        baseVals (list): The list of data values to be returned.
        targetTimes (list): The list of numeric time values used to find the
            closest 'baseVals'.
        maximumTimeDiff (None, numbers.Number): The maximum distance between
            the 'target time' and the closest value in 'baseTimes' (defaults to
            'None').

    Returns:
        list: The list of 'base values' that corrospond to 'targetTimes' using
            the 'baseTimes' list.
            None: If no closest time because all values are further away then
                'maximumTimeDiff'.
            object: If a closest time value was found.
    """
    _raiseIfWrongType(baseTimes, 'baseTimes', list)
    _raiseIfWrongType(baseVals, 'baseVals', list)
    _raiseIfWrongType(targetTimes, 'targetTimes', list)
    if maximumTimeDiff is not None:
        _raiseIfWrongType(maximumTimeDiff, 'maximumTimeDiff', numbers.Number)

    if not len(baseTimes) == len(baseVals):
        raise ValueError("The 'baseTimes' and 'baseVals' lists must have the"
                         " same length")

    returnVals = []
    for ii, targetTime in enumerate(targetTimes):
        minimumTimeBaseIndex = None

        minimumTimeBaseIndex = nearestIndexTime(baseTimes, targetTime,
                                                maximumTimeDiff)

        if minimumTimeBaseIndex is None:
            newVal = None
        else:
            newVal = baseVals[minimumTimeBaseIndex]

        returnVals.append(newVal)

    return returnVals


def nearestPairsFromTimesDelNone(baseTimes, baseVals, targetTimes,
                                 targetVals=None, maximumTimeDiff=None):
    """Return 'nearestPairsFromTimes' and other lists with removed 'None's.

    If a 'None' appears in the 'nearestPairsFromTimes' list output, the same
        indexed position in 'targetVals', 'targetTimes', and the main function
        output are removed, then returned.

    Args:
        baseTimes (list): Passed.
        baseVals (list): Passed.
        targetTimes (list): Passed. Corrosponding elements are removed.
        targetVals (list): Corrosponding elements are removed [optional]
            (defaults to 'None').
        maximumTimeDiff (None, numbers.Number): Passed.

    Returns:
        tuple: (
            list: Return value of 'nearestPairsFromTimes()' with removed 'None'
                values.
            list: Inputted 'targetTimes' with removed elements at the same
                index.
            list: Inputted 'targetVals' with removed elements at the same
                index [Not returned if targetVals is 'None'].
        )
    """
    _raiseIfWrongType(targetTimes, 'targetTimes', list)
    if targetVals is not None:
        _raiseIfWrongType(targetVals, 'targetVals', list)
        if not len(targetTimes) == len(targetVals):
            raise ValueError("The 'targetTimes' and 'targetVals' lists must "
                             "have the same length")

    returnVals = nearestPairsFromTimes(baseTimes, baseVals, targetTimes,
                                       maximumTimeDiff)

    returnArrays = [returnVals, targetTimes]
    if targetVals is not None:
        returnArrays.append(targetVals)
    returnArrays = tuple(returnArrays)

    for ii in reversed(range(len(returnVals))):
        if returnVals[ii] is None:
            for delList in returnArrays:
                del delList[ii]

    return returnArrays


def meterDistance(loc1, loc2=None, preset=None):
    """Return meter distance between two coordinates.

    A known preset name can be supplied for a saved 'loc2' value.

    Preset Values:
        'start1': (41.737356, -71.319894)

    Args:
        loc1 (tuple): Coordinate pair 1.
        loc2 (tuple, None): Coordinate pair 2 (Defaults to 'None').
        preset (None, basestring): A valid preset name.

    Returns:
        int: Distance between 'loc1' and 'loc2' in meters.
    """
    if (loc2 is None and preset is None) \
            and (loc2 is not None and preset is not None):
        raise ValueError("Please supply 'loc2' or 'preset' argument")

    # Presets:
    if preset == 'start1':
        loc2 = (41.737356, -71.319894)
    else:
        return ValueError("Inputted 'preset' value unknown")

    return vincenty(loc1, loc2).meters


#----------------------------------------------------------------
# Function that provides the mg/L levels for 
# 100% dissolved oxygen at a given temperature
#    concDisOxySaturated(pressure in mmHg , Temperature in degC )
#
# 160910 RG
#

from scipy import interpolate

def concDisOxySaturated(pressure_mmHg , Temperature_degC ):
    # Calibration Table
    # 160910
    # http://www.vernier.com/files/manuals/odo-bta/odo-bta.pdf
    # 100% SATURATED VALUES
    
    x_pressmmHg = [770. , 760. , 750. , 740. ]  # PRESSURE mmHg
    x_pressmmHg = np.array(x_pressmmHg)
    
    y_degC = [0.,1.,2.,3.,4.,5.,6.,7.,8.,9.,10.,11.,12.,14.,16.,18.,20.,22.,24.,26.,28.,30.,32.,34.]   # TEMPERATURE degC
    y_degC = np.array(y_degC)
    
    
    z_mgPerL = [ # 770 , 760 , 750 ,740
    [14.76,	14.57,	14.38,	14.19], # 0 degC
    [14.38,	14.19,	14,	13.82], # 1
    [14.01,	13.82,	13.64,	13.46], # 2
    [13.65,	13.47,	13.29,	13.12], # 3
    [13.31,	13.13,	12.96,	12.79], # 4
    [12.97,	12.81,	12.64,	12.47], # 5
    [12.66,	12.49,	12.33,	12.16], # 6
    [12.35 , 12.19 , 12.03 , 11.87],# 7 
    [12.05 , 11.90 , 11.74 , 11.58],# 8
    [11.77,11.62,11.46,11.31], #9
    [11.50,11.35,11.20,11.05], #10
    [11.24,11.09,10.94,10.80], #11
    [10.98,10.84,10.70,10.56], #12
    [10.51,10.37,10.24,10.10], #14
    [10.07,9.94,9.81,9.68], #16
    [9.67,9.54,9.41,9.29], #18
    [9.29,9.17,9.05,8.93], #20
    [8.94,8.83,8.71,8.59], #22
    [8.62,8.51,8.40,8.28], #24
    [8.32,8.21,8.10,7.99], #26
    [8.04,7.93,7.83,7.72], #28
    [7.77,7.67,7.57,7.47], #30
    [7.51,7.42,7.32,7.22], #32
    [7.27,7.17,7.08,6.98], #34
    ]
    z_mgPerL = np.array(z_mgPerL)
    
    # scipy.interpolate.interp2d
    #  http://docs.scipy.org/doc/scipy-0.13.0/reference/generated/scipy.interpolate.interp2d.html
    #
    
    # Define function to call
    _concDisOxySaturated = interpolate.interp2d( x_pressmmHg, y_degC, z_mgPerL , kind='linear')
    
    x = _concDisOxySaturated( pressure_mmHg , Temperature_degC )
    
    return np.tolist()
#    return np.array( x , dtype = 'float64' )
    
    # To use function    concDisOxySaturated(pressure in mmHg , Temperature in degC )
    
