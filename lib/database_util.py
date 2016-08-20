"""Contain methods useful when analyzing data."""
from pymongo import MongoClient
import shelve
import os


DEFAULTS = {"server": ["localhost", "10.0.2.197", "192.168.42.50"]}
DB_KEY_NAME = 'DB'
COL_KEY_NAME = 'COL'
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
        db (str): The database name.
        col (str): The collection name.
    """
    if not isinstance(db, basestring):
        raise ValueError("The 'db' value is not a string")
    if not isinstance(col, basestring):
        raise ValueError("The 'col' value is not a string")

    try:
        d = shelve.open(SHELF_FILE)
        d[DB_KEY_NAME] = db
        d[COL_KEY_NAME] = col
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
                    'addr' (str): The stored server address.
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
        return {'addr': addr, 'port': port}


def getDbCol(mongo=None):
    """Return database and collection name saved in the shelve file.

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
    try:
        d = shelve.open(SHELF_FILE)
        db = d.get(DB_KEY_NAME, None)
        col = d.get(COL_KEY_NAME, None)
    finally:
        d.close()

    if db is None or col is None:
        raise ValueError("Please use the 'saveDbCol' function, to set the 'db' \
            and 'col' values")

    if mongo is not None:
        return (mongo[db])[col]
    else:
        return {'db': db, 'col': col}


def getServerDbCol():
    """Return a 'pymongo' 'Collection' object using the stored values.

    The stored server address values are used to create a
        'pymongo.MongoClient' object. This and the stored database and
        collection values are used to make the 'pymongo' 'Collection' object.
    """
    mongo = getServerHost(createMongoClient=True)
    return getDbCol(mongo)
