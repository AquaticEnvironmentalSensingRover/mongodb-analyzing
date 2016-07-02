def dbColSelector(mongo):
    print("Databases:\n" + str(sorted(mongo.database_names())))
    db = raw_input("DB Name: ")
    print("\nCollections:\n" + str(sorted(mongo[db].collection_names())))
    col = raw_input("Col Name: ")
    return (mongo[db])[col]