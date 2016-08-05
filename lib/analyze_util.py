"""Contain methods useful when analyzing data."""
import numbers
import database_util as du
import warnings
warnings.simplefilter('once', DeprecationWarning)


# Private:
def __raiseIfWrongType(value, valueName, targetType):
    if not isinstance(value, targetType):
        raise TypeError("The '{}' value is required to be a '{}' type"
                        .format(valueName, targetType.__name__))


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
        times (list): The list of numeric time values used to find the closest.
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
    __raiseIfWrongType(times, 'times', list)
    __raiseIfWrongType(targetTime, 'targetTime', numbers.Number)

    if maximumTimeDiff is not None:
        __raiseIfWrongType(maximumTimeDiff, 'maximumTimeDiff', numbers.Number)

    closeTimeIndex = None

    for ii, time in enumerate(times):
        if (abs(time-targetTime) < maximumTimeDiff) or maximumTimeDiff is None:
            if closeTimeIndex is not None:
                if abs(times[closeTimeIndex]-targetTime) \
                        > abs(time-targetTime):
                    closeTimeIndex = ii
            else:
                closeTimeIndex = ii

    return closeTimeIndex


def nearestPairsFromTimes(baseVals, baseTimes, targetTimes,
                          maximumTimeDiff=None):
    """Return a list of values in baseVals that corrospond to the times lists.

    The closest 'base time' to each 'target time' is found, then an array
        containing the corrosponding 'base values' for the closest 'base times'
        is returned.

    The 'baseVals' and 'bastTimes' have to be the same length as they are the
        two 1D arrays of a 2D array.

    Args:
        baseVals (list): The list of data values to be returned.
        baseTimes (list): The list of numeric time values used to find the
            closest.
        targetTimes (list): The list of numeric time values used to find the
            closest 'baseVals'.
        maximumTimeDiff (None, numbers.Number): The maximum distance between
            the 'target time' and the closest value in 'baseTimes' (defaults to
            'None').

    Returns:
        None: If no closest time because of empty 'baseTimes' array or all
            values are further away then 'maximumTimeDiff'.
        list: The list of 'base values' that corrospond to 'targetTimes' using
            the 'baseTimes' list.
    """
    __raiseIfWrongType(baseTimes, 'baseTimes', list)
    __raiseIfWrongType(baseVals, 'baseVals', list)
    __raiseIfWrongType(targetTimes, 'targetTimes', list)
    if maximumTimeDiff is not None:
        __raiseIfWrongType(maximumTimeDiff, 'maximumTimeDiff', numbers.Number)

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
