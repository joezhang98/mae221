##Authors: Whitney Huang, Mario Liu, Joe Zhang
##Date Started: 
##Notes: 

##Pressure sensor data-sheet website: http://www.mouser.com/ds/2/187/honeywell-sensing-trustability-ssc-series-standard-740340.pdf

from pithy import *
import libSimplePhoton as lsp #simple photon interface
import libmae221

#potentiometer = 10.55k ohms

##################
##Get the Photon##
p = lsp.simplePhoton("FeebleFennel") #Your Spark Name Here
################
##Get The Data##

data = p.getHistory('2016-10-12') #Enter Today's date or the date you want to see data for in the parentheses: 'YYYY-MM-DD'. Defaults to the latest file when no name entered.

print "Time now = "
print time.time()

##This section of code re-zeros the start time of your data
##You may need this after you connect your thermocouple
#time_start = 1476298200.04 #10/12/16 exp. 1, var vol
#time_end = 1476299500.04

time_start = 1476301600.04 #10/12/16 exp. 2, const vol = 2.2 mL
time_end = 1476302750.04

#time_start = 1476298000.04 #This is the UNIX time of your 'start' time.
#time_end = 1476299500.04
data = data[data['time']>time_start]
data = data[data['time']<time_end]

########################
##Start time at 0 from the first reading of the day
########################
psiToPascal = 6894.76 #Pa/psi
volThermoc = 0.5 #cm^3

t = data['time'] - data['time'].iloc[0]


#########################
##Convert bits to voltage:
#########################
a0 = data['a0']
a1 = data['a1']
a2 = data['a2']
a3 = data['a3']

potenPin = a1
pSensorPin = a2
tempPinInSyringe = a0
tempPinOutside = a3

levels = 4095. #2^12 max value on ADC
Vmax = 2.50381
Vmin = 0.000806
Vsupply = 3.3
R = 10000 #resistance in voltage divider
volMin = 2.2
volMax = 10.
Prange = 30.
Patm = 1.013e5

V_pot = (Vsupply/levels)* potenPin
#0.000806 V at fully extended (10 mL)
#2.50381 V at fully contracted (2.2 mL)
volGas = ((volMax-volMin)/(Vmax-Vmin))*(Vmax-V_pot)+volMin - volThermoc

Pmax = 15*psiToPascal
Pmin = -15*psiToPascal
Papp = ((pSensorPin/levels)*Prange - 15)*psiToPascal #press applied

#pressure = (V_pressure - 1.65) / 0.088
V_pressure = (0.8*Vsupply)*(Papp-Pmin)/(Pmax-Pmin) + (0.10*Vsupply)

pressure1 = ((Prange/(0.8*Vsupply))*V_pressure - 18.75)*psiToPascal

Tin = libmae221.epcos6850(tempPinInSyringe,R)
Tout = libmae221.epcos6850(tempPinOutside,R)
Tc = data['temp']

#T0 = 18 + 273
V0 = (volMin - volThermoc)
#D0 = stater('T',T0,'V',V0,'air')['D']
n = 1.6/22400 * V0
R = ((pressure1 + Patm)*(volGas/1e6))/((Tin+273.15)*n)

print R

print "\nAverage R value:" 
print sum(R)/len(R)
print "\n"

#print (Papp*volGas/Tin) #calculate R
# print p.getState()['a0']
# print V_put

plot(t,R,label='R')
legend(loc="best")
xlabel("Time (s)")
ylabel("R (Pa * m^3 / K * mol")
title("Estimated Value of R vs. Time")
showme()
clf()

plot(t,V_pot,label='Voltage_Potentiometer')
plot(t,V_pressure,label='Voltage_Pressure')
legend(loc="best")
xlabel("Time (s)")
ylabel("Voltage (V)")
title("Voltage of Potentiometer and Pressure Sensor vs. Time")
showme()
clf()

plot(t,volGas,label='Volume of Air')
legend(loc="best")
xlabel("Time (s)")
ylabel("Volume (cm^3)")
ylim(0, 10)
title("Volume of Air inside Syringe vs. Time")
showme()
clf()

plot(t,pressure1,label='Gauge Pressure')
legend(loc="best")
xlabel("Time (s)")
ylabel("Gauge Pressure (Pa)")
title("Pressure inside Syringe vs. Time")
showme()
clf()

plot(t,Tin,label='Temperature Inside Syringe')
plot(t,Tout,label='Temperature Outside Syringe')
plot(t,Tc,label='Temperature Inside Hot Pot')
legend(loc="best")
xlabel("Time (s)")
ylabel("Temperature (Degrees C)")
title("Temperature Measurements vs. Time")
showme()
clf()

plot(Tin,pressure1, label='Pressure vs. Temperature')
legend(loc="best")
xlabel("Temperature (C)")
ylabel("Gauge Pressure (Pa)")
title("Pressure vs. Temperature of Syringe")
showme()
clf()
