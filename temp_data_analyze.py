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
    
x=[]
y=[]
# Create x and y - Array with arrays of the individual sensor readings
for ii in data:
    newX, newY=zip(*ii)
    x.append(newX)
    y.append(newY)

args=[]
for ii in range(len(data)):
    args.append(x[ii])
    args.append(y[ii])
    args.append("b")
    
# Plot data
plt.plot(*args)
plt.show()