# showPlotDates...py
# Demostrate use of datetime.datetime in plotting graphs
# 160702
#
# Move from date to datetime object
# datetime.datetime.fromtimestamp(1347517370)   =>  datetime.datetime(2012, 9, 13, 2, 22, 50)
#
import datetime
import random
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

formatter = DateFormatter('%H:%M:%S')

n = 10
# n = 1000

#x = [ (1000. * random.random(  ) ) for i in xrange(n) ]
#y = [ (1. * random.random(  ) ) for i in xrange(n) ]

# make up some data

# datetime.datetime.fromtimestamp(1347517370)
# => datetime.datetime(2012, 9, 13, 2, 22, 50)

x = [datetime.datetime.now() + datetime.timedelta(hours=i) for i in range(n)]
y = [i+random.gauss(0,1) for i,_ in enumerate(x)]

# plot

plt.figure(1)
plt.clf()
plt.plot( x , y , '.' )
#ax.xaxis_date()
plt.show()
#plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
plt.gcf().autofmt_xdate()


