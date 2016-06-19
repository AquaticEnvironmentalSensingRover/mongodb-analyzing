# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient
import time

colors = ["r","g","b","c"]

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
    
t0 = time.time()

args=[]
for index, ii in enumerate(data):
    x, y=zip(*ii)
    args.append( np.add(x,-t0) )
    args.append(y)
    args.append(colors[index])
    
# Plot data
plt.figure(1)
plt.clf()
plt.plot(*args)
plt.title('Latest data %f' % t0 )
plt.axis([-100, 5, 22, 26])
plt.ylabel("Temperature (degC)")
plt.xlabel("Time (s)")
plt.show()