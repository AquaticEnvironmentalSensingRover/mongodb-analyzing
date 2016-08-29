"""Contain methods useful when analyzing data."""
import numpy as np
import numbers
import database_util as du
import warnings
warnings.simplefilter('once', DeprecationWarning)


# Private:
def __raiseIfWrongType(value, valueName, *targetTypes):
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


def __convertToNPArray(value):
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
    __raiseIfWrongType(times, 'times', list, np.ndarray)
    times = __convertToNPArray(times)

    __raiseIfWrongType(targetTime, 'targetTime', numbers.Number)

    __raiseIfWrongType(maximumTimeDiff, 'maximumTimeDiff', numbers.Number,
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
    __raiseIfWrongType(targetTimes, 'targetTimes', list)
    if targetVals is not None:
        __raiseIfWrongType(targetVals, 'targetVals', list)
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
