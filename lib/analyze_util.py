DEFAULTS = {"server":["localhost", "10.0.2.197", "192.168.42.50"]}

def serverAddressSelector():
    print("\nUse index number of IP address\nDefault server IP Addresses:\n" + str(DEFAULTS["server"]))
    ipAddress = raw_input("Server IP Address: ")
    
    try:
        return (DEFAULTS["server"])[int(ipAddress)]
    except ValueError:
        return ipAddress

def dbColSelector(mongo, dbNameStartFilter = "AESR_"):
    rawDbNames = sorted(mongo.database_names(), reverse=True)
    
    # Print databases filtering with the supplied argument
    # NOTE: Using enumerate() didn't pickup "local" in "rawDbNames" for some reason
    dbNames = []
    for ii in range(len(rawDbNames)):
        dbName = rawDbNames[ii]
        if dbName.startswith(dbNameStartFilter):
            dbNames.append(dbName)
        
    # Print filtered list of databases
    print("\nDatabases (newest -> oldest based on name):\n" + str(dbNames))
    dbInput = raw_input("DB Name (Index number of IP address): ")
    
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