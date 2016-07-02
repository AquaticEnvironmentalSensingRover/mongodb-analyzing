DEFAULTS = {"server":["localhost", "10.0.2.197", "192.168.42.50"]}

def serverAddressSelector():
    print("\nUse index number of IP address\nDefault server IP Addresses:\n" + str(DEFAULTS["server"]))
    ipAddress = raw_input("Server IP Address: ")
    
    try:
        return (DEFAULTS["server"])[int(ipAddress)]
    except ValueError:
        return ipAddress

def dbColSelector(mongo):
    print("Databases:\n" + str(sorted(mongo.database_names())))
    db = raw_input("DB Name: ")
    print("\nCollections:\n" + str(sorted(mongo[db].collection_names())))
    col = raw_input("Col Name: ")
    return (mongo[db])[col]