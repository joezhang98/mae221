##Authors: Whitney Huang, Mario Liu, Joe Zhang
##Notes: Lab 4 
##Vapor compression refrigeration cycles

from pithy import *
import libMotorPhoton as lmp #motor photon interface
import libmae221

#Pull data for 2 sparks - 1 measures the water input temperature
b = lmp.motorPhoton('007') #Your Spark Name Here
c = lmp.motorPhoton('VelvetMonkey')

print time.time()

resistor = 1000. #Set your resistor value here
cp = 4184. # J/kg K


########Pressure & Time Readings
##Put your values here
P1 = 38.  # +/- 5 kPa gauge pressure (blue - evaporator)
P2 = 980. # +/- 10 kPa gauge pressure (red - condenser)
mR = 10.  # +/- 1 kg/hr mass flow rate of refrigerant
mC = 21.  # +/- 5 kg/hr mass flow rate of condenser
mE = 102. # +/- 5 kg/hr mass flow rate of evaporator
# VelvetMonkey - inlet temperature of water TS
# 007 - outlet, temperature of water/refrigerant

#SI units
P1 = 38.*1000. + 1.013e5
P2 = 980.*1000. + 1.013e5
mR = 10./3600.
mC = 21./3600.
mE = 102./3600.
#Unix time taken at: 

################
##Pull the history - You can set this up in the same way as lab 1/2.
################
#print b.getData()
data = b.getHistory('2016-11-30') #Date format: 'YYYY-MM-DD'
t0 = data['time'].iloc[0]
data['time'] = data['time'] - t0

#Pull in data from the second spark
data_2 = c.getHistory('2016-11-30') #Date format: 'YYYY-MM-DD'
data_2['time'] = data_2['time'] - t0


time_start = 0.
time_end = 10000.
data = data[data['time']>time_start]
data = data[data['time']<time_end]

data_2 = data_2[data_2['time']>time_start]
data_2 = data_2[data_2['time']<time_end]

TS = libmae221.epcos6850(data_2['a0'],resistor)
print "TS:", TS.iloc[-1]

# exit()

#################
##Pulling the thermocouple temperature data
#################

T1 = libmae221.epcos6850(data['a0'],resistor) #Freon low pressure
T2 = libmae221.epcos6850(data['a1'],resistor) #Freon high pressure
T3 = libmae221.epcos6850(data['a2'],resistor) #Freon after condensor
T4 = libmae221.epcos6850(data['a3'],resistor) #Freon before evap
TC = libmae221.epcos6850(data['a4'],resistor) #Water outlet hot side
TE = libmae221.epcos6850(data['a5'],resistor) #Water outlet cold side

print "T1: %.1f, T2: %.1f, T3: %.1f, T4: %.1f, TC: %.1f, TE: %.1f, TS: %.1f" % (T1.iloc[-1], T2.iloc[-1], T3.iloc[-1], T4.iloc[-1], TC.iloc[-1], TE.iloc[-1],TS.iloc[-1])

title("Temperature Readings throughout Commercial Unit")
plot(data['time'],T1,label="T1: Freon low pressure")
plot(data['time'],T2,label="T2: Freon high pressure")
plot(data['time'],T3,label="T3: Freon after cond")
plot(data['time'],T4,label="T4: Freon before evap")
plot(data['time'],TC,label="TC: water hot side")
plot(data['time'],TE,label="TE: Water cold side")
plot(data_2['time'],TS,label="TS: Water temperature in")
legend(loc="best",prop={'size':10})
xlabel("Time (s)")
ylabel("Temperature (C)")

showme(dpi=300)
clf()

#print "T0: %f, T1: %f, T2: %f" % (T0, T1, T2)  
# recorded constants
# T1: 10.0, T2: 95.8, T3: 19.5, T4: -22.1, TC: 36.8, TE: 9.3, TS: 13.6

# COP calculation
Qin = mE*cp*(TS.iloc[-1] - TE.iloc[-1])
Qout = mC*cp*(TC.iloc[-1] - TS.iloc[-1])
print "Qin (J/s): ", Qin
print "Qout (J/s): ", Qout

Wtotal = 469. # J/s
Wfan = 26. # J/s
# calculation for efficiency
print "Excess: ", (Qin-Qout+Wtotal-Wfan)
percentPowereff = ((Wtotal-Wfan)- (Qin-Qout+Wtotal-Wfan))/(Wtotal-Wfan)
print "Percentage of power going to refrigerant: ", percentPowereff
print "Energy rate balance: ", (Qin-Qout+percentPowereff*(Wtotal-Wfan))

# calculation for COP for the refrigeration cycle
COPbeta = Qin/(percentPowereff*(Wtotal-Wfan))
print "beta: ", COPbeta

# calculation for COP for the heat pump
COPgamma = Qout/(percentPowereff*(Wtotal-Wfan))
print "gamma: ", COPgamma

# plot phase envelopes

Ps = [130000, 1300000, 1300000, 130000, 130000]
Hs = [380000, 430000, 230000, 230000, 380000]

states = {}

# states
p1 = 130000. #Pa
h1 = 390000. #J/kg
states[1] = stater('P',p1,'H',h1,'R12')

p2 = 1300000. #Pa
h2 = 430000. #J/kg
states[2] = stater('P',p2,'H',h2,'R12')

p3 = 1300000. #Pa
h3 = 230000. #J/kg
states[3] = stater('P',p3,'H',h3,'R12')

p4 = 130000. #Pa
h4 = 230000. #J/kg
states[4] = stater('P',p4,'H',h4,'R12')

print state_table(states)

annotate(str(1),xy=(Hs[0],Ps[0]-50000))
annotate(str(2),xy=(Hs[1]+5000,Ps[1]+250000))
annotate(str(3),xy=(Hs[2]-6000,Ps[2]+250000))
annotate(str(4),xy=(Hs[3]-6000,Ps[3]-50000))

#BONUS
#temp
p_space = logspace(4, 8, 70)
T_space = linspace(100, 600, 40)
for Ti in T_space:
    h_space = stater("T", Ti, "P", p_space, "R12")['H']
    semilogy(h_space, p_space, color = "blue")
semilogy(h_space, p_space, color = "blue", label="Constant Temperature Lines")
    
#entropy
p_space = logspace(4, 8, 70)
s_space = linspace(700, 1900, 40)
for si in s_space:
    h_space = stater("S", si, "P", p_space, "R12")['H']
    semilogy(h_space, p_space, color = "green")
semilogy(h_space, p_space, color = "green", label="Constant Entropy Lines")
    
#quality
p_space = logspace(4, 8, 70)
q_space = linspace(0, 1, 40)
for qi in q_space:
    h_space = stater("Q", qi, "P", p_space, "R12")['H']
    semilogy(h_space, p_space, color = "magenta")
semilogy(h_space, p_space, color = "magenta", label="Constant Quality Lines")

title("Pressure-Enthalpy Diagram for R12 (Freon) in Cycle")
phcycle = plot(Hs,Ps,'k')
setp(phcycle, color='r', linewidth=2.5)
ph_phase_envelope('R12', fill=True)
semilogy()
xlabel("Enthalpy (J/kg)")
ylabel("Absolute Presure (Pa)")
xlim(140000,450000)
ylim(70000,40000000)
legend(loc="best")
grid(True)
showme()
clf()

Ts = [T1.iloc[-1]+273, T2.iloc[-1]+273, T3.iloc[-1]+273+20, T3.iloc[-1]+273+20, T3.iloc[-1]+273, T4.iloc[-1]+273,T4.iloc[-1]+273, T1.iloc[-1]+273]
Ss = [1650, 1650, 1550, 1130, 1065, 1080, 1575, 1650]

annotate(str(1),xy=(Ss[0]+18,Ts[0]-2))
annotate(str(2),xy=(Ss[1]+3,Ts[1]+3))
annotate(str(3),xy=(Ss[4]-24,Ts[4]+2))
annotate(str(4),xy=(Ss[5]-20,Ts[5]-8))

#BONUS
#quality
T_space = linspace(100, 500, 70)
q_space = linspace(0., 1., 40)
for qi in q_space:
    s_space = stater("T", T_space, "Q", qi, "R12")['S']
    plot(s_space, T_space, color = "magenta")
plot(s_space, T_space, color = "magenta", label="Constant Quality Lines")

#pressure
T_space = linspace(100, 500, 70)
p_space = logspace(4, 7, 40)
for pi in p_space:
    s_space = stater("T", T_space, "P", pi, "R12")['S']
    plot(s_space, T_space, color = "green")
plot(s_space, T_space, color = "green", label="Constant Pressure Lines")

#enthalpy
s_space = linspace(700, 1900, 70)
h_space = linspace(150000, 450000, 40)
for hi in h_space:
    T_space = stater("S", s_space, "H", hi, "R12")['T']
    plot(s_space, T_space, color = "red")
plot(s_space, T_space, color = "red", label="Constant Enthalpy Lines")

title("Temperature-Entropy Diagram for R12 (Freon) in Cycle")
tscycle = plot(Ss, Ts, 'k')
setp(tscycle, color='b', linewidth=2.5)
ts_phase_envelope('R12', fill=True)
xlabel("Entropy (J/(kg*K))")
ylabel("Temperature (K)")
xlim(750,1800)
ylim(200,420)
legend(loc="best")
grid(True)
showme()
clf()
