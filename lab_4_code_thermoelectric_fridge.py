##Authors: Whitney Huang, Mario Liu, Joe Zhang
##Lab 4
##Thermoelectric fridge data

from pithy import *
import libMotorPhoton as lmp #motor photon interface
import libmae221
import numpy as np
import time
from pylab import *
from scipy.optimize import curve_fit

##################
##Get the Photon##
##################
b = lmp.motorPhoton("FeebleFennel") #Your Spark Name Here


##################################
#Data/Time Manipulation Functions#
##################################
#You probably want to bring in all the data/time manipulation functions
#that you used in labs 1 & 2
#ie rezero data. remove data before a given time etc

print "Time now = ", time.time(), "\n"

##getData() pulls the latest reading from your spark.
#print b.getData()

#getHistory pulls all of that day's history from your spark.
#data = b.getHistory('2016-10-19')
data = b.getHistory('2016-11-16') #'2016-11-16'

time_start = 1479330403.08 #start time for water cooling
time_end = 1479331796.63
data = data[data['time']>time_start]
data = data[data['time']<time_end]
t = data['time']-data['time'].iloc[0]

#t = data['time'] - data['time'].iloc[0]

##############
#Control Code#
##############
resistor = 1000.
plot(t, libmae221.epcos6850(data['a0'],resistor), label='Water Temperature', linewidth=1.5)

print "\n"
legend(loc='best')
xlabel("Time (s)")
ylabel("Temperature (C)")
title("Temperature of Water vs. Time\n")
showme()
clf()

#############
#tiny fridge#
#############
m_water = 0.13 - 0.074
cp_water = 4184. #J/(kg*K)

T_water = libmae221.epcos6850(data['a0'],resistor)
T_water_insta = libmae221.epcos6850(b.getData()['a0'],resistor)
print "Instantaneous Water Temperature: ", T_water_insta

power = 42.4
t_elapsed = time_end - time_start

T_water_i = 21.88
T_water_f = T_water[19535]

COP_graph = (m_water*cp_water*(T_water_i - T_water))/(power*(data['time'] - time_start))

x = t
y = COP_graph

def func(x, a, b, c, d):
    return a*np.exp(-c*(x-b))+d

popt, pcov = curve_fit(func, x, y)
print popt

#plot(x,y)
#x=linspace(400,6000,10000)
#plot(x,func(x,*popt))
#show()

plot(t, COP_graph)
plot(x,y)
xlabel("Time (s)")
ylabel("COP")
ylim(0,0.5)
title("COP of Thermoelectric Fridge vs. Time")
showme()
clf()

T_water_avg = mean(T_water)
W_cycle_avg = t_elapsed * power

# COP_avg = (m_water * cp_water * (T_water_f - T_water_i)) / W_cycle_avg

# print "Average COP: ", COP_avg

COP_avg2 = COP_graph.iloc[1350]

print "Average COP: ", COP_avg2
