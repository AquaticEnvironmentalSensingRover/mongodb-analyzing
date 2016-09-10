"""Contain methods useful when analyzing data."""
from pymongo import MongoClient
import analyze_util as au
import numbers
import shelve
import os


DEFAULTS = {"server": ["localhost", "10.0.2.197", "192.168.42.50"]}
DB_KEY_NAME = 'DB'
COL_KEY_NAME = 'COL'
RUN_NUM_KEY_NAME = 'RUN_NUM'
SERVER_ADDR_KEY_NAME = 'ADDR'
SERVER_PORT_KEY_NAME = 'PORT'
SHELF_FILE = os.path.dirname(os.path.abspath(__file__)) + '/dbCol.shelf'


# Input selectors:
def serverAddressSelector():
    """Return selected server address.

    Default options are printed before input is asked for.

    Inputs:
        raw_input (str, int): Server address or the index number in the printed
            string

    Returns:
        str: The selected server address.
    """
    print("\n Use IP address or:\n\nUse index number of IP address in:"
          "\nDefault server IP Addresses:\n" + str(DEFAULTS["server"]))
    ipAddress = raw_input("Server IP Address: ")

    try:
        return (DEFAULTS["server"])[int(ipAddress)]
    except ValueError:
        return ipAddress


def dbColSelector(mongo, dbNameStartFilter="AESR_"):
    """Return inputted database and collection name.

    Avalable options are printed before input is asked for.

    Args:
        mongo (MongoClient): The 'pymongo.MongoClient' object of the MongoDB
            server.
        dbNameStartFilter (str): The database name print filter (defaults to
            'AESR_').

    Inputs:
        raw_input (str): The database name.
        raw_input (str): The collection name.

    Returns:
        Collection: The pymongo 'Collection' object based on the inputted
            MongoClient object, database name, and collection name.
    """
    rawDbNames = sorted(mongo.database_names(), reverse=True)

    # Print databases filtering with the supplied argument
    # NOTE: Using enumerate() didn't pickup "local" in "rawDbNames"
    dbNames = []
    for ii in range(len(rawDbNames)):
        dbName = rawDbNames[ii]
        if dbName.startswith(dbNameStartFilter):
            dbNames.append(dbName)

    # Print filtered list of databases
    print("\nDatabases (newest -> oldest based on name):\n" + str(dbNames))
    dbInput = raw_input("DB Name (Index number of DB or name): ")

    # Treat input as integer for an index,
    # but if something goes wrong, use the input as the database name
    try:
        db = (dbNames)[int(dbInput)]
    except ValueError:
        db = dbInput
    print "SELECTED Database: " + db

    # Print collection names in the given database
    print("\nCollections:\n" + str(sorted(mongo[db].collection_names())))
    col = raw_input("Col Name: ")

    # Return collection object using the database and collection names
    return (mongo[db])[col]


# Private:
def __listStringCheck(theList, listName):
    for ii in theList:
        if not isinstance(ii, basestring):
            raise ValueError("The '{}' list must contain only strings"
                             .format(listName))


def __listsSameLength(list1, list1Name, list2, list2Name):
    if not len(list1) == len(list2):
        raise ValueError("The lists '{}' and {}".format(list1Name, list2Name) +
                         " are not the same length")


# Other:
def dbColArgSelector(mongo, dbName, colName):
    """Return a 'pymongo' 'Collection' object from the inputted values.

    Args:
        mongo (MongoClient): The 'pymongo.MongoClient' object of the MongoDB
            server.
        dbName (str): The database name.
        colName (str): The collection name.

    Returns:
        Collection: The pymongo 'Collection' object based on the inputted
            MongoClient object, database name, and collection name.
    """
    # Return collection object using the database and collection names
    return (mongo[dbName])[colName]


# SAVE:
def setServerHost(addr, port):
    """Save inputted database and collection name into a shelve file.

    Args:
        addr (str): The server address.
        port (int): The server port.
    """
    if not isinstance(addr, basestring):
        raise ValueError("The 'addr' value is not a string")
    if not isinstance(port, int):
        raise ValueError("The 'port' value is not an int")

    try:
        d = shelve.open(SHELF_FILE)
        d[SERVER_ADDR_KEY_NAME] = addr
        d[SERVER_PORT_KEY_NAME] = port
    finally:
        d.close()


def setDbCol(db, col):
    """Save inputted database and collection name into a shelve file.

    Args:
        db (str, list[str]): The database name.
        col (str): The collection name.
    """
    au._raiseIfWrongType(db, 'db', basestring, list)
    au._raiseIfWrongType(col, 'col', basestring, list)

    if isinstance(db, list):
        __listStringCheck(db, 'db')
    if isinstance(col, list):
        __listStringCheck(col, 'col')

    if isinstance(db, list) and isinstance(col, list):
        if not len(db) == len(col):
            raise ValueError("The 'db' and 'col' arguments must have the same"
                             " length")
    try:
        d = shelve.open(SHELF_FILE)
        if isinstance(db, list):
            d[DB_KEY_NAME] = db
        else:
            d[DB_KEY_NAME] = [db]

        if isinstance(col, list):
            d[COL_KEY_NAME] = col
        else:
            d[COL_KEY_NAME] = [col]
    finally:
        d.close()


def setRunNumber(runNum):
    """Save inputted run number into a shelve file.

    If inputted 'runNum' is 'None', then it is removed from the shelf.

    Args:
        runNum (numbers.Number): The run number or 'None'.
    """
    try:
        d = shelve.open(SHELF_FILE)

        if runNum is None:
            try:
                del d[RUN_NUM_KEY_NAME]
            except KeyError:
                pass
        else:
            if not isinstance(runNum, numbers.Number):
                raise ValueError("The 'runNum' value is not a number "
                                 "(or None)")

            d[RUN_NUM_KEY_NAME] = runNum
    finally:
        d.close()


# GET:
def getServerHost(createMongoClient=False):
    """Return address and port of the server saved in the shelve file.

    Args:
        createMongoClient (bool): If this is 'True', a 'pymongo.MongoClient'
            object is returned (defaults to 'False').

    Returns:
        if createMongoClient is True:
            pymongo.MongoClient: A 'pymongo.MongoClient' object, created using
                the stored address and port.
        else:
            dict:
                {
                    'host' (str): The stored server address.
                    'port' (int): The stored server port.
                }
    """
    try:
        d = shelve.open(SHELF_FILE)
        addr = d.get(SERVER_ADDR_KEY_NAME, None)
        port = d.get(SERVER_PORT_KEY_NAME, None)
    finally:
        d.close()

    if addr is None or port is None:
        raise ValueError("Please use the 'saveDbCol' function, to set \
                         'addr' and 'port'")

    if createMongoClient is True:
        return MongoClient(addr, port)
    else:
        return {'host': addr, 'port': port}


def getDbsCol(mongo=None):
    """Return database and collection names saved in the shelve file.

    Args:
        mongo (pymongo.MongoClient): If a value is supplied, a 'Collection'
            object will be returned instead (defaults to 'None').

    Returns:
        if mongo is not None:
            Collection: A list of 'pymongo' 'Collection' objects selected using
                the database and collection names, and the
                'pymongo.MongoClient' object.
        else:
            dict:
                {
                    'db' (list[str]): The stored database name.
                    'col' (str): The stored collection name.
                }

    """
    if not (isinstance(mongo, MongoClient) or mongo is None):
        raise ValueError("Please supply a 'pymongo.MongoClient' object for"
                         "argument 'mongo'")
    try:
        d = shelve.open(SHELF_FILE)
        db = d.get(DB_KEY_NAME, None)
        col = d.get(COL_KEY_NAME, None)
    finally:
        d.close()

    if db is None or col is None:
        raise ValueError("Please use the 'saveDbCol' function, to set the 'db' \
            and 'col' values")

    if (len(db) > 1 and len(col) > 1):
        __listsSameLength(db, 'db', col, 'col')

    # Db + Col lists:
    if mongo is not None:
        dbCols = []
        if (len(db) > 1 and len(col) > 1):
            for ii in range(len(db)):
                dbCols.append(mongo[db[ii]][col[ii]])
            return dbCols

        elif len(db) > 1:
            for eachDb in db:
                dbCols.append((mongo[eachDb])[col[0]])
            return dbCols

        else:
            for eachCol in col:
                dbCols.append((mongo[db[0]])[eachCol])
            return dbCols

    return {'db': db, 'col': col}


def getDbCol(mongo=None, *args, **kwargs):
    """Return database and collection name saved in the shelve file.

    NOTE: Function is kept to keep backwards compatibilty with single dbCol
        scripts.

    Args:
        mongo (pymongo.MongoClient): If a value is supplied, a 'Collection'
            object will be returned instead (defaults to 'None').

    Returns:
        if mongo is not None:
            Collection: A 'pymongo' 'Collection' object selected using the
                database and collection name, and the 'pymongo.MongoClient'
                object.
        else:
            dict:
                {
                    'db' (str): The stored database name.
                    'col' (str): The stored collection name.
                }

    """
    value = getDbsCol(*args, mongo=mongo, **kwargs)
    if mongo is None:
        db = value['db']
        del value['db']
        value['db'] = db[0]
        return value
    else:
        return value[0]


def getServerDbCol():
    """Return a 'pymongo' 'Collection' object using the stored values.

    The stored server address values are used to create a
        'pymongo.MongoClient' object. This and the stored database and
        collection values are used to make the 'pymongo' 'Collection' object.
    """
    mongo = getServerHost(createMongoClient=True)
    return getDbCol(mongo)


def getRunNumber():
    """Return the stored 'run number'."""
    try:
        d = shelve.open(SHELF_FILE)
        runNum = d.get(RUN_NUM_KEY_NAME, None)
    finally:
        d.close()

    if runNum is None:
        raise ValueError("Please use the 'setRunNumber' function, to set the"
                         "'runNum' values")

    return runNum
