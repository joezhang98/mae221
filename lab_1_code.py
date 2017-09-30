##Authors: Whitney Huang, Mario Liu, Joe Zhang
##Date Started: 9/21/16
##Notes: This is the code for the students to start with.

from pithy import *
import libSimplePhoton as lsp #simple photon interface
##################
##Get the Photon##
p = lsp.simplePhoton("FeebleFennel") #Your Spark Name Here

################
##Get The Data##
data = p.getHistory('2016-09-21') #Enter Today's date or the date you want to see data for in the parentheses: 'YYYY-MM-DD'. Defaults to the latest file when no name entered.

#############################
##Do some data manipulation##

#This section of code re-zeros the start time of your data
#You may need this after you connect your thermocouple
#Uncomment as necessary
print time.time()
#time_start = 1474483971.02 #2:53 on 9/21/2016
#time_start = 1474484391.02 #3:00 on 9/21/16
#time_start = 1474486274.92 #3:31 on 9/21/16
#good calibration time: 1474483874.92, 2000 seconds
#time = 1475089139.87 9/28/16 2:59pm to 40C
#time = 1475090150.43 9/28/16 3:16pm test to 40C, 70s
#time = 1475091350.74 9/28/16 3:36pm test to 40C, 60s
#time = 1475091830.58 9/28/16 3:44pm test to 40C, 35s
#time = 1475092309.28 9/28/16 3:52pm test to 40C, 30s
#time = 1475092872.54 9/28/16 4:01pm 1st test to 40C, 22.2s
#time = 1475093286.23 9/28/16 4:08pm 2nd test to 40C, 21.5s
#time = 1475093649.63 9/28/16 4:14pm 1st test to 50C, 36.3s
#time = 1475094253.80 9/28/16 4:24pm 2nd test to 50C, 34.1s
#time = 1475094579.22 9/28/16 4:29pm 1st test to 70C, 62.2s
#time = 1475095233.20 9/28/16 4:40pm 2ndish test to 70C, 63.7s
#time = 1475095620.31 9/28/16 4:47pm 2nd test to 70C, 65.1s
#average volt from switch is 116.9 V
#average power is 1.414 kW
#time_start = 1474484574.92
time_start = 1474484274.92

time_end = time_start + 1800
data = data[data['time']>time_start]
data = data[data['time']<time_end]

#############################
##Simple plotting function###
#############################
t = data['time']-data['time'].iloc[0]
a0 = data['a0']
Tc = data['temp']

#print Tc

R2 = 10000.
Vmax = 4095.
Rt = (Vmax*R2 - a0*R2)/a0

plot(t,Tc)
ylabel("Temperature (C)")
xlabel("Time (s)")
title("Thermocouple Temperature vs. Time")
showme()
clf()

plot(t,data['a0'])
ylabel("Vout (bits)")
xlabel("Time (s)")
title("Thermistor Vout vs. Time")
showme()
clf()

plot(Tc,Rt)
ylabel("Resistance of Thermistor (ohms)")
xlabel("Temperature (C)")
title("Thermistor Resistance vs. Thermocouple Temperature")
showme()
clf()

import scipy.optimize as optimization
def Steinhart_Hart(R,A,B,C,D):
    T = 1/(A+B*log(R) + C*log(R)**2 + D*log(R)**3)
    return T
    
x0 = array([1, 1, 1, 1]) #initial guesses

SH = optimization.curve_fit(Steinhart_Hart, Rt, Tc, x0)[0]
#print "\nCurrent SH Parameters:", SH, "\n\n"

# SH Parameters: [ 9.20375773 -3.74086232  0.50667014 -0.02283337]

#SHfinal = array([9.20375773, -3.74086232,  0.50667014, -0.02283337])

def epcos6850(R):
    T = Steinhart_Hart(R, SH[0], SH[1], SH[2], SH[3])
    return T

plot(t, epcos6850(Rt))
plot(t, Tc)
ylabel("Temperature (Celsius)")
xlabel("Time (s)")
title("Thermocouple Temperature and Steinhart-Hart vs. Time")
showme()
clf()

plot(Tc, epcos6850(Rt))
ylabel("Steinhart-Hart Temperature (Celsius)")
xlabel("Measured Temperature (Celsius)")
title("Steinhart-Hart Temperature vs Measured Thermocouple")
showme()
clf()

#print "Current time at start of experiment: "
#print time.time()

#p.setOutput(0, 0)
#time.sleep(5)

#p.setOutput(0, 1)
#time.sleep(65.1)
#p.setOutput(0, 0)
