import lib.database_util as du
from pymongo import MongoClient
import math

DEFAULTS = {"SERVER_HOST": ["localhost", "10.0.2.197", "192.168.42.50"],
            "SERVER_PORT": 27017}
DB_START_FILTER = "AESR_"


def printGap(length=60):
    printLine = ''
    for ii in range(length):
        printLine += '='
    print printLine


printGap()
# Server setting =============================================================:
#   Server IP setting:
print("\nUse IP address or index number of IP address in:"
      "\n\nDefault server IP Addresses:\n" + str(DEFAULTS["SERVER_HOST"]))
ipAddress = raw_input("Server IP Address: ")

try:
    ipAddress = (DEFAULTS["SERVER_HOST"])[int(ipAddress)]
except ValueError:
    pass

printGap()
#   Server port setting:
ipPort = raw_input("Server port (Leave blank for {}): "
                   .format(str(DEFAULTS["SERVER_PORT"])))

if ipPort == "":
    ipPort = DEFAULTS["SERVER_PORT"]
ipPort = int(ipPort)

printGap()
# DbCol setting ==============================================================:
mongo = MongoClient(ipAddress, ipPort)


def __num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

#   Preset DbCol:
runNum = raw_input("Run number (Leave blank for none): ")

manualEntry = True
if not runNum == '':
    manualEntry = False
    runNum = __num(runNum)
    col = 'data'

    db = []
    if runNum == 4:
        db = ['AESR_20160716T184018']
    elif math.floor(runNum) == 5:
        dbs = ['AESR_20160717T154442', 'AESR_20160717T165349',
               'AESR_20160717T193309']
        if runNum == 5:
            db = dbs
        elif runNum == 5.1:
            db = [dbs[0]]
        elif runNum == 5.2:
            db = [dbs[1]]
        elif runNum == 5.3:
            db = [dbs[2]]
        else:
            print "\nThe inputted sub-run number of '5' does not exist"
    else:
        print "\nThe inputted run number doesn't exist"
        manualEntry = True
else:
    runNum = None


#   Text input DbCol:
if manualEntry:
    db = []
    col = []

entryLoopNum = -1
while manualEntry:
    printGap()

    entryLoopNum += 1
    print "\nManual entry loop:", entryLoopNum
    rawDbNames = sorted(mongo.database_names(), reverse=True)

    # Print databases filtering with the supplied argument
    # NOTE: Using enumerate() didn't pickup "local" in "rawDbNames"
    dbNames = []
    for ii in range(len(rawDbNames)):
        dbName = rawDbNames[ii]
        if dbName.startswith(DB_START_FILTER):
            dbNames.append(dbName)

    # Print filtered list of databases
    print("\nDatabases (newest -> oldest based on name):\n" + str(dbNames))
    newDb = raw_input("DB Name (Index number of DB or name [leave blank to" +
                      " finish]): ")

    # Treat input as integer for an index,
    # but if something goes wrong, use the input as the database name
    try:
        newDb = (dbNames)[int(newDb)]
        print newDb
    except ValueError:
        pass

    if newDb == '':
        break
    db.append(newDb)

    printGap(10)
    # Print collection names in the given database
    print("\nCollections:\n" + str(sorted(mongo[newDb].collection_names())))
    newCol = raw_input("Col Name: ")
    if newCol == '':
        raise ValueError('Collection name was empty')
    col.append(newCol)

printGap()

if len(db) == 0:
    raise ValueError("No database/collection pairs specified")

# Value writing
print "\nSELECTED Server address: " + ipAddress
print "SELECTED Server port: " + str(ipPort)
du.setServerHost(ipAddress, ipPort)

print "\nSELECTED Database: " + str(db)
print "SELECTED Collection: " + str(col)
du.setDbCol(db, col)

print "\nSELECTED Run number: " + str(runNum)
du.setRunNumber(runNum)
