import lib.analyze_util as au
from pymongo import MongoClient
import time

mongo = MongoClient(host=au.serverAddressSelector())

dbCol = au.dbColSelector(mongo)

atype = raw_input("\nMongoDB data atype: ")

while True:
    paramValue = None
    for ii in dbCol.find({"atype":atype}):
        paramValue = ii["param"]
        
    print paramValue
    
    time.sleep(1.5)