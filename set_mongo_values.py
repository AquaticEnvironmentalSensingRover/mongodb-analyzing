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
print("\nUse IP address or:\nKeep blank for default:\n"
      + str(DEFAULTS["SERVER_PORT"]))
ipPort = raw_input("Server port: ")
if ipPort == "":
    ipPort = DEFAULTS["SERVER_PORT"]
ipPort = int(ipPort)

# DbCol setting ==============================================================:
mongo = MongoClient(ipAddress, ipPort)
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
except ValueError:
    pass
print "SELECTED Database: " + db

# Print collection names in the given database
print("\nCollections:\n" + str(sorted(mongo[db].collection_names())))
col = raw_input("Col Name: ")


# Value writing
du.setServerHost(ipAddress, ipPort)
du.setDbCol(db, col)
