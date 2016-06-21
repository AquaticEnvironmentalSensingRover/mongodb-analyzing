# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient
import time

colors = ["r","g","b","c","k"]

db = input("DB Name: ")
col = input("Col Name: ")

sensorAmount = 5

mongo = MongoClient(host="10.0.2.189")

dbCol = (mongo[db])[col]

data = []

for ii in range(sensorAmount):
    newData = []
    for jj in dbCol.find({"atype":"TEMP", "itype":ii}):
        newData.append([ jj["ts"], jj["param"] ])
        
    data.append(newData)
    
t0 = time.time()

# Plot data
plt.figure(1)
plt.clf()
plt.title('Latest data %f' % t0 )
plt.axis([-100, 5, 22, 26])
plt.ylabel("Temperature (degC)")
plt.xlabel("Time (s)")

for index, ii in enumerate(data):
    x, y=zip(*ii)
    plt.plot(np.add(x,-t0), y, colors[index], label=("Temp: " + str(index)))
    
plt.legend()
plt.show()