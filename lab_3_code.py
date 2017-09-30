##Authors: Whitney Huang, Mario Liu, Joe Zhang
##Lab 3

from pithy import *
import libMotorPhoton as lmp #motor photon interface
import libmae221
import numpy as np
from datetime import datetime as dt
import time

##############################################################
        
        
        #THIS IS DAN'S DATA, USING PHOTON NAMED "007"
        #time_start = 1478893676
        #time_end = 1478893922
        #date = 11/11/16
        
        
##############################################################



######################
##Variables/Constants#
######################
#Voltage supply = 10.00V

E1 = 60/11.62
E2 = 60/11.96
E3 = 60/11.69
ESyringeAvg = (E1+E2+E3)/3.
print "ESyringeAvg: %f" % (ESyringeAvg)
print ""

#cold water pump
E1pump1 = 200/22.31 #at 100 pwm
E2pump1 = 200/22.31 #at 100 pwm
E12pump1Avg = (E1pump1+E2pump1)/2.

E3pump1 = 200/13.30 #at 125 pwm
E4pump1 = 200/13.30 #at 125 pwm
E34pump1Avg = (E3pump1+E4pump1)/2.

E5pump1 = 200/10.12 #at 150 pwm
E6pump1 = 200/10.12 #at 150 pwm
E56pump1Avg = (E5pump1+E6pump1)/2.

E7pump1 = 200/8.26 #at 175 pwm
E8pump1 = 200/8.26 #at 175 pwm
E78pump1Avg = (E7pump1+E8pump1)/2.

E9pump1 = 200/7.47 #at 200 pwm
E10pump1 = 200/7.47 #at 200 pwm
E910pump1Avg = (E9pump1+E10pump1)/2.

print "Pumping at 20C"
print "E12pump1Avg: %f, \nE34pump1Avg: %f, \nE56pump1Avg: %f, \nE78pump1Avg: %f, \nE910pump1Avg: %f" % (E12pump1Avg, E34pump1Avg, E56pump1Avg, E78pump1Avg, E910pump1Avg)
print ""

pump1PWMarray = [100, 125, 150, 175, 200]
pump1FlowArray = [E12pump1Avg, E34pump1Avg, E56pump1Avg, E78pump1Avg, E910pump1Avg]
plot(pump1FlowArray, pump1PWMarray, label='Original Data Points')

#best-fit process
pump1PWM = np.array([100, 125, 150, 175, 200])

pump1flow = np.array([E12pump1Avg, E34pump1Avg, E56pump1Avg, E78pump1Avg, E910pump1Avg])

pump1corr = np.polyfit(pump1flow, pump1PWM, 2)

finalCorr1 = np.poly1d(pump1corr)
#print finalCorr1(PWM)
#78.2 hot
#86.4 cold

x1 = np.arange(0, 30)
y1 = finalCorr1(x1)
plt.plot(x1, y1, label='Quadratic Best Fit')
xlabel("Flow Rate (mL/s)")
ylabel("PWM (bits)")
title("Hot Water Flow")
legend(loc="best")
showme()
clf()


#cold water, not usable
#E1pump0 = 250/ #at 100 pwm
#E2pump0 = 250/ #at 100 pwm
#E3pump0 = 250/22.75 #at 125 pwm
#E4pump0 = 250/23.10 #at 125 pwm
#E5pump0 = 250/16.80 #at 150 pwm
#E6pump0 = 250/16.42 #at 150 pwm
#E7pump0 = 250/13.46 #at 175 pwm
#E8pump0 = 250/13.33 #at 175 pwm
#E9pump0 = 250/11.56 #at 200 pwm
#E10pump0 = 250/11.57 #at 200 pwm

#hot water pump
#new calibration data
#E1pump0 = 200/33.57 #at 100 pwm
#E2pump0 = 200/33.57 #at 100 pwm
#E12pump0Avg = (E1pump0+E2pump0)/2

#E3pump0 = 200/16.54 #at 125 pwm
#E4pump0 = 200/16.54 #at 125 pwm
#E34pump0Avg = (E3pump0+E4pump0)/2

#E5pump0 = 200/14.05 #at 150 pwm
#E6pump0 = 200/14.05 #at 150 pwm
#E56pump0Avg = (E5pump0+E6pump0)/2

#E7pump0 = 200/12.98 #at 175 pwm
#E8pump0 = 200/12.98 #at 175 pwm
#E78pump0Avg = (E7pump0+E8pump0)/2

#E9pump0 = 200/12.39 #at 200 pwm
#E10pump0 = 200/12.39 #at 200 pwm
#E910pump0Avg = (E9pump0+E10pump0)/2

#old calibration data
E1pump0 = 250/60.90 #at 100 pwm
E2pump0 = 250/63.27 #at 100 pwm
E12pump0Avg = (E1pump0+E2pump0)/2

E3pump0 = 250/24.62 #at 125 pwm
E4pump0 = 250/25.88 #at 125 pwm
E34pump0Avg = (E3pump0+E4pump0)/2

E5pump0 = 250/16.50 #at 150 pwm
E6pump0 = 250/16.72 #at 150 pwm
E56pump0Avg = (E5pump0+E6pump0)/2

E7pump0 = 250/14.52 #at 175 pwm
E8pump0 = 250/14.49 #at 175 pwm
E78pump0Avg = (E7pump0+E8pump0)/2

E9pump0 = 250/12.92 #at 200 pwm
E10pump0 = 250/12.65 #at 200 pwm
E910pump0Avg = (E9pump0+E10pump0)/2

print "Pumping at 100C"
print "E12pump0Avg: %f, \nE34pump0Avg: %f, \nE56pump0Avg: %f, \nE78pump0Avg: %f, \nE910pump0Avg: %f" % (E12pump0Avg, E34pump0Avg, E56pump0Avg, E78pump0Avg, E910pump0Avg)
print ""

pump0PWMarray = [100, 125, 150, 175, 200]
pump0FlowArray = [E12pump0Avg, E34pump0Avg, E56pump0Avg, E78pump0Avg, E910pump0Avg]
plot(pump0FlowArray, pump0PWMarray, label='Original Data Points')

#best-fit process
pump0PWM = np.array([100, 125, 150, 175, 200])

pump0flow = np.array([E12pump0Avg, E34pump0Avg, E56pump0Avg, E78pump0Avg, E910pump0Avg])

pump0corr = np.polyfit(pump0flow, pump0PWM, 2)

finalCorr0 = np.poly1d(pump0corr)

x0 = np.arange(0, 30)
y0 = finalCorr0(x0)
plt.plot(x0, y0, label='Quadratic Best Fit')
xlabel("Flow Rate (mL/s)")
ylabel("PWM (bits)")
title("Cold Water Flow")
legend(loc="best")
showme()
clf()


##################
##Get the Photon##
##################
#b = lmp.motorPhoton("FeebleFennel") #Your Spark Name Here
b = lmp.motorPhoton("007")

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
#data = b.getHistory('2016-11-09')
data = b.getHistory('2016-11-11')

time_start = 1478893676
time_end = 1478893922

#time_start = 1476902468.63 #10/19/16
#time_start = 1478731738.08 #11/9/16 bit before

#time_start = 1478731768.08 #11/9/16 whole experiment
#time_end = 1478731908.08
data = data[data['time']>time_start]
data = data[data['time']<time_end]

t = data['time'] - data['time'].iloc[0]


#########################################
##This is the voltage divider resistance#
#########################################
resistor = 1000. #Set your resistor value here


############################################################
##Pull the data or history - You can set this up in the same way as lab 1/2.                                            #
############################################################
plot(data['d1'], label='PWM of Hot Water Pump', linewidth=1.3)
plot(data['d0'], label='PWM of Cold Water Pump', linewidth=1.3)
legend(loc="best")
xlabel("Time (s)")
ylabel("PWM")
title("PWM of Motors")
showme()
clf()






plot(libmae221.epcos6850(data['a0'],resistor), label='Cold Temperature', linewidth=1.5) #plot(libmae221.epcos6850(data['a1'],resistor), label='THot')
plot(libmae221.epcos6850(data['a1'],resistor), label='Hot Temperature', linewidth=1.5) 
plot(libmae221.epcos6850(data['a2'],resistor), label='Syringe Temperature', linewidth=1.5)
#plot(data['a4']) 
#plot(data['a5'])
legend(loc="upper left")
xlabel("Time (s)")
ylabel("Temperature (C)")
title("Three Measured Temperatures")
showme()
clf()


############################################
##Pulling the thermocouple temperature data#
############################################

# Note this only works if you have a thermistor connected to each port
# Comment out the unnecessary lines.
# cold
T0 = libmae221.epcos6850(b.getData()['a0'],resistor);
#T1 = libmae221.epcos6850(b.getData()['a1'],resistor)
# hot
T2 = libmae221.epcos6850(b.getData()['a2'],resistor);
# syringe
T3 = libmae221.epcos6850(b.getData()['a3'],resistor);
#T4 = libmae221.epcos6850(b.getData()['a4'],resistor)
#T5 = libmae221.epcos6850(b.getData()['a5'],resistor)

#plot(T0)   
#plot(T1) 
#plot(T2)
#plot(T3)
#plot(data['a4']) 
#plot(data['a5'])
#xlabel("Time (s)")
#showme()
#clf()

#print "T0: %f, T1: %f, T2: %f, T3: %f" % (T0, T1, T2, T3) 
print "\nT0: %f, T2: %f, T3: %f" % (T0, T2, T3)

###########################
##Turning on and off motor#
###########################
#(motor number 0,1 or 2, on: 1 or off: 0, PWM value: 0 - 25

#40C
targetTemp = 40.
coldTemp = 20.
hotTemp = 100.
ESyringeAvg = 8.8 #flow rate through syringe

hotFlow = (targetTemp*(ESyringeAvg) - coldTemp*(ESyringeAvg))/(hotTemp - coldTemp)

#hotFlow = (ESyringeAvg*coldTemp)/(hotTemp-2*targetTemp+coldTemp)

coldFlow = ESyringeAvg - hotFlow

hotPWM = finalCorr1(hotFlow)
coldPWM = finalCorr0(coldFlow)

print "\nhotFlow40C = ", hotFlow, "mL/s"
print "coldFlow40C = ", coldFlow, "mL/s"

print "hotPWM40C = ", hotPWM
print "coldPWM40C = ", coldPWM

#b.setMotor(0,1,hotFlow) #hot
#b.setMotor(1,1,coldFlow) #cold

#time.sleep(20)

#30C
targetTemp = 30.

hotFlow = (targetTemp*(ESyringeAvg) - coldTemp*(ESyringeAvg))/(hotTemp - coldTemp)

coldFlow = ESyringeAvg - hotFlow

hotPWM = finalCorr1(hotFlow)
coldPWM = finalCorr0(coldFlow)

print "\nhotFlow30C = ", hotFlow, "mL/s"
print "coldFlow30C = ", coldFlow, "mL/s"

print "hotPWM30C = ", hotPWM
print "coldPWM30C = ", coldPWM

#b.setMotor(0,1,hotFlow) #hot
#b.setMotor(1,1,coldFlow) #cold

#time.sleep(10)

#60C
targetTemp = 60.

hotFlow = (targetTemp*(ESyringeAvg) - coldTemp*(ESyringeAvg))/(hotTemp - coldTemp)

coldFlow = ESyringeAvg - hotFlow

hotPWM = finalCorr1(hotFlow)
coldPWM = finalCorr0(coldFlow)

print "\nhotFlow60C = ", hotFlow, "mL/s"
print "coldFlow60C = ", coldFlow, "mL/s"

print "hotPWM60C = ", hotPWM
print "coldPWM60C = ", coldPWM

#b.setMotor(0,1,hotFlow) #hot
#b.setMotor(1,1,coldFlow) #cold

#time.sleep(10)

#80C
targetTemp = 80.

hotFlow = (targetTemp*(ESyringeAvg) - coldTemp*(ESyringeAvg))/(hotTemp - coldTemp)

coldFlow = ESyringeAvg - hotFlow

hotPWM = finalCorr1(hotFlow)
coldPWM = finalCorr0(coldFlow)

print "\nhotFlow80C = ", hotFlow, "mL/s"
print "coldFlow80C = ", coldFlow, "mL/s"

print "hotPWM80C = ", hotPWM
print "coldPWM80C = ", coldPWM

#b.setMotor(0,1,hotFlow) #hot
#b.setMotor(1,1,coldFlow) #cold

#time.sleep(10)

#stop
#b.setMotor(0,0,hotFlow) #hot
#b.setMotor(1,0,coldFlow) #cold

want = time.mktime((2016,11,9,12+4,20,0,0,0,0))

close = abs(data['time']-want).argmin()

print data.iloc[close]
