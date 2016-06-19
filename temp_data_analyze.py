import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient

db = "test_data1"
col = "tempData"

sensorAmount = 4

mongo = MongoClient(host="10.0.2.81")

dbCol = (mongo[db])[col]

data = []

for ii in range(sensorAmount):
    newData = []
    for jj in dbCol.find({"atype":"TEMP", "itype":ii}):
        newData.append([ jj["ts"], jj["param"] ])
        
    data.append(newData)
    

args=[]
for ii in data:
    x, y=zip(*ii)
    args.append(x)
    args.append(y)
    args.append("b")
    
# Plot data
plt.plot(*args)
plt.show()