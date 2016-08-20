import lib.database_util as du
from pymongo import MongoClient

DEFAULTS = {"SERVER_HOST": ["localhost", "10.0.2.197", "192.168.42.50"],
            "SERVER_PORT": 27017}
DB_START_FILTER = "AESR_"

# Server setting =============================================================:
#   Server IP setting:
print("\n Use IP address or:\n\nUse index number of IP address in:"
      "\nDefault server IP Addresses:\n" + str(DEFAULTS["SERVER_HOST"]))
ipAddress = raw_input("Server IP Address: ")

try:
    ipAddress = (DEFAULTS["SERVER_HOST"])[int(ipAddress)]
except ValueError:
    pass

#   Server port setting:
ipPort = raw_input("\nServer port (Leave blank for {}): "
                   .format(str(DEFAULTS["SERVER_PORT"])))

if ipPort == "":
    ipPort = DEFAULTS["SERVER_PORT"]
ipPort = int(ipPort)

# DbCol setting ==============================================================:
mongo = MongoClient(ipAddress, ipPort)


def __num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

#   Preset DbCol:
runNum = raw_input("\nRun number (Leave blank for none): ")

manualEntry = True
if not runNum == '':
    manualEntry = False
    runNum = __num(runNum)
    col = 'data'

    if runNum == 4:
        db = 'AESR_20160716T184018'
    elif runNum == 5.1:
        db = 'AESR_20160717T154442'
    elif runNum == 5.2:
        db = 'AESR_20160717T165349'
    elif runNum == 5.3:
        db = 'AESR_20160717T193309'
    else:
        print "\nThe inputted run number doesn't exist"
        manualEntry = True
else:
    runNum = None

#   Text input DbCol:
if manualEntry:
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
    db = raw_input("DB Name (Index number of DB or name): ")

    # Treat input as integer for an index,
    # but if something goes wrong, use the input as the database name
    try:
        db = (dbNames)[int(db)]
        print db
    except ValueError:
        pass

    # Print collection names in the given database
    print("\nCollections:\n" + str(sorted(mongo[db].collection_names())))
    col = raw_input("Col Name: ")


# Value writing
print "\nSELECTED Server address: " + ipAddress
print "SELECTED Server port: " + str(ipPort)
du.setServerHost(ipAddress, ipPort)

print "\nSELECTED Database: " + db
print "SELECTED Collection: " + col
du.setDbCol(db, col)

print "\nSELECTED Run number: " + str(runNum)
du.setRunNumber(runNum)
