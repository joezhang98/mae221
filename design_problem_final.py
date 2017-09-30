## Author: Joe Zhang
## Date:   01/16/17

## Notes: MAE design problem due on Dean's Date.  This pithy code contains the p-v, p-h, and T-s diagrams of my Rankine cycle as well as the state table and all calculations.  It also contains a plot of net present value (NPV) of my power plant over 30 years assuming a discount rate of 6 percent.

# Background Information:
# The working fluid in the cycle is water
# Maintain at least 90% quality at turbine exit
# Turbine and pump stages are adiabatic processes with an isentropic efficiency of 85%
# All heaters are adiabatic processes
# The power plant must comply with cooling water intakes regulations published by the EPA and state regulations (the state chosen in my problem is California)
from pithy import*

# Givens/Restraints
eff_t = 0.85   # 85% turbine efficiency
eff_p = 0.85   # 85% pump efficiency
e_cost = 0.08  # cost of electricty in $/kWhr
e_cost *= 24 * 365.25 / 1000 # units of $/Wyear
f_cost = 0.025 # cost of fuel in $/kWhr
f_cost *= 24 * 365.25 / 1000 # units of $/Wyear
m1_dot = 100.  # max flow rate in kg/s

##############################################################
# The following section of code defines the state table      #
##############################################################
states = {}

# Defines State 1
# Description: steam enters the turbine at 700 Celsius
p1 = 1.6e7         # Pa
T1 = 700. + 273.15 # K
states[1] = stater('P',p1,'T',T1,'water')
h1 = states[1]['H']

# Defines State 2 Ideal
# Description: steam diverted between the first and second stages to the first closed feedwater heater
p2 = 8.0e6           # Pa
s2s = states[1]['S'] # J/kgK 
states2s = stater('P',p2,'S',s2s,'water')
h2s = states2s['H']

# Defines State 2 Actual
h2 = h1 - eff_t * (h1 - h2s)
states[2] = stater('P',p2,'H',h2,'water')

# Defines State 3 Ideal
# Description: steam diverted between the second and third stages to a second closed feedwater heater
p3 = 4.0e6           # Pa
s3s = states[2]['S'] # J/kgK
states3s = stater('P',p3,'S',s3s,'water')
h3s = states3s['H']

# Defines State 3 Actual
h3 = h2 - eff_t * (h2 - h3s)
states[3] = stater('P',p3,'H',h3,'water')

# Defines State 4 Ideal
# Description: steam expands in three stages to a reheat pressure of 2000 kPa
p4 = 2.0e6           # Pa
s4s = states[3]['S'] # J/kgK
states4s = stater('P',p4,'S',s4s,'water')
h4s = states4s['H']

# Defines State 4 Actual
h4 = h3 - eff_t * (h3 - h4s)
states[4] = stater('P',p4,'H',h4,'water')

# Defines State 5
# Description: steam reheated to 500 Celsius
p5 = p4            # Pa
T5 = 500. + 273.15 # K
states[5] = stater('P',p5,'T',T5,'water')
h5 = states[5]['H']

# Defines State 6 Ideal
# Description: steam diverted between the fourth and fifth stages to an open feedwater heater
p6 = 8.0e5           # Pa
s6s = states[5]['S'] # J/kgK
states6s = stater('P',p6,'S',s6s,'water')
h6s = states6s['H']

# Defines State 6 Actual
h6 = h5 - eff_t * (h5 - h6s)
states[6] = stater('P',p6,'H',h6,'water')

# Defines State 7 Ideal
# Description: steam diverted between the fifth and sixth stages to a third closed feedwater heater
p7 = 2.0e5           # Pa
s7s = states[6]['S'] # J/kgK
states7s = stater('P',p7,'S',s7s,'water')
h7s = states7s['H']

# Defines State 7 Actual
h7 = h6 - eff_t * (h6 - h7s)
states[7] = stater('P',p7,'H',h7,'water')

# Defines State 8 Ideal
# Description: steam expands in three more stages to a condenser pressure of 10 kPa
p8 = 1.0e4           # Pa
s8s = states[7]['S'] # J/kgK
states8s = stater('P',p8,'S',s8s,'water')
h8s = states8s['H']

# Defines State 8 Actual
h8 = h7 - eff_t * (h7 - h8s)
states[8] = stater('P',p8,'H',h8,'water')

# Defines State 9
# Description: saturated liquid exits the condenser at 10 kPa
p9 = p8 # Pa
q9 = 0  # quality
states[9] = stater('P',p9,'Q',q9,'water')
h9 = states[9]['H']
v9 = states[9]['V']

# Defines State 10 Ideal
# Description: saturated liquid enters the condensate pump and receives work
p10 = 8.0e5                 # Pa
h10s = h9 + v9 * (p10 - p9) # J/kg
states10s = stater('P',p10,'H',h10s,'water')

# Defines State 10 Actual
h10 = h9 + ((h10s - h9) / eff_p)
states[10] = stater('P',p10,'H',h10,'water')

# Defines State 11
# Description: condensate leaves the third closed feedwater heater at 160 Celsius
p11 = p10           # Pa
T11 = 160. + 273.15 # K
states[11] = stater('P',p11,'T',T11,'water')
h11 = states[11]['H']

# Defines State 12
# Description: condensate exits the open feedwater heater as saturated liquid
p12 = p11 # Pa
q12 = 0   # quality
states[12] = stater('P',p12,'Q',q12,'water')
h12 = states[12]['H']
v12 = states[12]['V']

# Defines State 13 Ideal
# Description: saturated liquid enters the main boiler feed pump and receives work
p13 = p1 # Pa
h13s = h12 + v12 * (p13 - p12)
states13s = stater('P',p13,'H',h13s,'water')

# Defines State 13 Actual
h13 = h12 + ((h13s - h12) / eff_p)
states[13] = stater('P',p13,'H',h13,'water')

# Defines State 14
# Description: condensate leaves the second closed feedwater heater at 280 Celsius
p14 = p13           # Pa
T14 = 280. + 273.15 # K
states[14] = stater('P',p14,'T',T14,'water')
h14 = states[14]['H']

# Defines State 15
# Description: steam diverted between the first and second stages exits the first closed feedwater heater as saturated liquid
p15 = p2 # Pa
q15 = 0  # quality
states[15] = stater('P',p15,'Q',q15,'water')
h15 = states[15]['H']

# Defines State 16
# Description: saturated liquid undergoes an adiabatic throttling process to 4000 kPa
p16 = p3  # Pa
h16 = h15 # J/kg
states[16] = stater('P',p16,'H',h16,'water')

# Defines State 17
# Description: steam diverted between the second and third stages exits the second closed feedwater heater as saturated liquid
p17 = p3 # Pa
q17 = 0  # quality
states[17] = stater('P',p17,'Q',q17,'water')
h17 = states[17]['H']

# Defines State 18
# Description: saturated liquid undergoes an aidabatic throttling process to 800 kPa
p18 = p6  # Pa
h18 = h17 # J/kg
states[18] = stater('P',p18,'H',h18,'water')

# Defines State 19
# Description: steam diverted between the fifth and sixth stages exits the third closed feedwater heater as saturated liquid
p19 = p7 # Pa
q19 = 0  # quality
states[19] = stater('P',p19,'Q',q19,'water')
h19 = states[19]['H']

# Defines State 20
# Description: saturated liquid undergoes an adiabatic throttling process to 10 kPa
p20 = p8  # Pa
h20 = h19 # J/kg
states[20] = stater('P',p20,'H',h20,'water')

# Defines State 21
# Description: condensate leaves the first closed feedwater heater at 320 Celsius
p21 = p1            # Pa
T21 = 320. + 273.15 # K
states[21] = stater('P',p21,'T',T21,'water')
h21 = states[21]['H']

# Prints the state table of the cycle
print state_table(states)

##############################################################
# The following section of code determines performance of    # # the power plant, and includes calculations for thermal     # # efficiency, net work output, heat in to the boiler, and    # # heat out through the condenser
##############################################################

# Diverted mass flow rate calculations
y1 = (h21-h14)/(h2-h15)
y2 = (h14-y1*h16-(1-y1)*h13)/(h3-h17)
y3 = ((1-y1)*h12-y2*h18-(1-y1-y2)*h11)/(h6-h11)
y4 = ((1-y1-y2-y3)*(h11-h10))/(h7-h19)

# Work and heat calculations
W_turbine1 = m1_dot*((h1-h2)+(1-y1)*(h2-h3)+(1-y1-y2)*(h3-h4))
W_turbine2 = m1_dot*((1-y1-y2)*(h5-h6)+(1-y1-y2-y3)*(h6-h7)+(1-y1-y2-y3-y4)*(h7-h8))
W_pump1 = m1_dot*((1-y1-y2-y3)*(h10-h9))
W_pump2 = m1_dot*((1-y1)*(h13-h12))
W_turbine_net = W_turbine1 + W_turbine2
W_pump_net = W_pump1 + W_pump2
Q_in = m1_dot*((h1-h21)+(1-y1-y2)*(h5-h4))
Q_out = m1_dot*((1-y1-y2-y3-y4)*h8+y4*h20-(1-y1-y2-y3)*h9)

# Calculates thermal efficiency, backwork ratio, heat rejection, and heat input in proper units
W_net = W_turbine_net - W_pump_net
thermal_eff = W_net / Q_in
bwr = W_pump_net / W_turbine_net
percent_eff = 100. * thermal_eff
MW_W_net = W_net / 1.0e6
MW_Q_out = Q_out / 1.0e6
MW_Q_in = Q_in / 1.0e6

# Prints out thermal efficiency, backwork ratio, heat rejection, and heat input
print "Power Plant Performance Characteristics"
print ""
print "Net power output   = %.2f MW" % MW_W_net
print "Thermal efficiency = %.1f%%" % percent_eff
print "Backwork ratio       = %.3f" % bwr
print "Heat rejection        = %.2f MW" % MW_Q_out
print "Heat input              = %.2f MW" % MW_Q_in

##############################################################
# The following section of code ensures that cooling water   #
# intakes of the power plant comply with US environmental    #
# regulations
##############################################################

# Reference: http://www.waterboards.ca.gov/laws_regulations/
# maximum allowed temperature increase for discharged water in the state of California is 10 Celsius

specific_heat = 4186. # specific heat of water (J/(kg K))
temp_change = 10.     # C or K
conversion_L_to_gal = 0.264172
m_water_dot = Q_out / (specific_heat * temp_change)
m_water_gallons = m_water_dot*24*60*60*conversion_L_to_gal

# Prints the cooling water intake of the power plant and the maximum allowed cooling water intake under U.S. law
print ""
print "Power Plant Cooling Water Intake Compliance"
print ""
print "Flow rate of intake water        =  %.1f million gallons/day" % (m_water_gallons/1.0e6)
print "Maxmimum flow rate allowed = 125.0 million gallons/day"
print ""

##############################################################
# The following section of code plots the p-v diagram        #
##############################################################

# Process through the boiler
T21to1 = linspace(states[21]['T'],states[1]['T'],100)
process21to1 = stater('T',T21to1,'P',p1,'water')

# Process through the boiler to reheat steam
T4to5 = linspace(states[4]['T'],states[5]['T'],100)
process4to5 = stater('T',T4to5,'P',p5,'water')

# Processes through the turbines
p1to2 = linspace(states[1]['P'],states[2]['P'],100)
s1to2 = linspace(states[1]['S'],states[2]['S'],100)
process1to2 = stater('P',p1to2,'S',s1to2,'water')
p2to3 = linspace(states[2]['P'],states[3]['P'],100)
s2to3 = linspace(states[2]['S'],states[3]['S'],100)
process2to3 = stater('P',p2to3,'S',s2to3,'water')
p3to4 = linspace(states[3]['P'],states[4]['P'],100)
s3to4 = linspace(states[3]['S'],states[4]['S'],100)
process3to4 = stater('P',p3to4,'S',s3to4,'water')
p5to6 = linspace(states[5]['P'],states[6]['P'],100)
s5to6 = linspace(states[5]['S'],states[6]['S'],100)
process5to6 = stater('P',p5to6,'S',s5to6,'water')
p6to7 = linspace(states[6]['P'],states[7]['P'],100)
s6to7 = linspace(states[6]['S'],states[7]['S'],100)
process6to7 = stater('P',p6to7,'S',s6to7,'water')
p7to8 = linspace(states[7]['P'],states[8]['P'],100)
s7to8 = linspace(states[7]['S'],states[8]['S'],100)
process7to8 = stater('P',p7to8,'S',s7to8,'water')

# Process through the condenser
s8to9 = linspace(states[8]['S'],states[9]['S'],100)
process8to9 = stater('S',s8to9,'P',p9,'water')
s20to9 = linspace(states[20]['S'],states[9]['S'],100)
process20to9 = stater('S',s20to9,'P',p9,'water')

# Processes through the pumps
p9to10 = linspace(states[9]['P'],states[10]['P'],100)
s9to10 = linspace(states[9]['S'],states[10]['S'],100)
process9to10 = stater('P',p9to10,'S',s9to10,'water')
p12to13 = linspace(states[12]['P'],states[13]['P'],100)
s12to13 = linspace(states[12]['S'],states[13]['S'],100)
process12to13 = stater('P',p12to13,'S',s12to13,'water')

# Processes through the closed heaters
T10to11 = linspace(states[10]['T'],states[11]['T'],100)
p10to11 = linspace(states[10]['P'],states[11]['P'],100)
process10to11 = stater('T',T10to11,'P',p10to11,'water')
T13to14 = linspace(states[13]['T'],states[14]['T'],100)
process13to14 = stater('T',T13to14,'P',p14,'water')
T14to21 = linspace(states[14]['T'],states[21]['T'],100)
process14to21 = stater('T',T14to21,'P',p21,'water')
T2to15 = linspace(states[2]['T'],states[15]['T'],100)
process2to15 = stater('T',T2to15,'P',p15,'water')
T3to17 = linspace(states[3]['T'],states[17]['T'],100)
process3to17 = stater('T',T3to17,'P',p17,'water')
h16to17 = linspace(states[16]['H'],states[17]['H'],100)
process16to17= stater('H',h16to17,'P',p17,'water')
s7to19 = linspace(states[7]['S'],states[19]['S'],100)
process7to19 = stater('S',s7to19,'P',p19,'water')

# Process through the deaerating open heater
s11to12 = linspace(states[11]['S'],states[12]['S'],100)
process11to12 = stater('S',s11to12,'P',p12,'water')
s6to12 = linspace(states[6]['S'],states[12]['S'],100)
process6to12 = stater('S',s6to12,'P',p12,'water')
s18to12 = linspace(states[18]['S'],states[12]['S'],100)
process18to12 = stater('S',s18to12,'P',p12,'water')

# Processes through the valves
p15to16 = linspace(states[15]['P'],states[16]['P'],100)
process15to16 = stater('H',h16,'P',p15to16,'water') 
p17to18 = linspace(states[17]['P'],states[18]['P'],100)
process17to18 = stater('H',h18,'P',p17to18,'water')
p19to20 = linspace(states[19]['P'],states[20]['P'],100)
process19to20 = stater('H',h20,'P',p19to20,'water')

# Draws the graph of pressure vs. specific volume
title("p-v Diagram with States Labeled")
pv_phase_envelope('water', fill = True)
loglog()
for i in range(1,22): 
    annotate('%i'%i, xy = (states[i]['V'],states[i]['P']))
xlabel("Specific Volume (m^3/kg)")
ylabel("Pressure (Pa)")
xlim(1.0e-4,1.0e2)
ylim(1e3,1e9)

# Draws the main cycle
plot(process1to2['V'],process1to2['P'],'r')
plot(process2to3['V'],process2to3['P'],'r')
plot(process3to4['V'],process3to4['P'],'r')
plot(process4to5['V'],process4to5['P'],'r')
plot(process5to6['V'],process5to6['P'],'r')
plot(process6to7['V'],process6to7['P'],'r')
plot(process7to8['V'],process7to8['P'],'r')
plot(process8to9['V'],process8to9['P'],'r')
plot(process9to10['V'],process9to10['P'],'r')
plot(process10to11['V'],process10to11['P'],'r')
plot(process11to12['V'],process11to12['P'],'r')
plot(process12to13['V'],process12to13['P'],'r')
plot(process13to14['V'],process13to14['P'],'r')
plot(process14to21['V'],process14to21['P'],'r')
plot(process21to1['V'],process21to1['P'],'r')

# Draws the reheat processes
plot(process2to15['V'],process2to15['P'],'r')
plot(process15to16['V'],process15to16['P'],'r')
plot(process3to17['V'],process3to17['P'],'r')
plot(process16to17['V'],process16to17['P'],'r')
plot(process17to18['V'],process17to18['P'],'r')
plot(process7to19['V'],process7to19['P'],'r')
plot(process20to9['V'],process20to9['P'],'r')
plot(process19to20['V'],process19to20['P'],'r')
plot(process6to12['V'],process6to12['P'],'r')
plot(process18to12['V'],process18to12['P'],'r')

# Completes the cycle diagram and shows it on the graph
plot([states[2]['V'],states[15]['V']],[states[2]['P'],states[15]['P']],'r')
plot([states[3]['V'],states[17]['V']],[states[3]['P'],states[17]['P']],'r')
plot([states[7]['V'],states[19]['V']],[states[7]['P'],states[19]['P']],'r')
showme()
clf()

##############################################################
# The following section of code plots the p-h diagram        #
##############################################################

# Draws the graph of pressure vs. specific enthalpy
title("p-h Diagram with States Labeled")
ph_phase_envelope('water',fill = True)
semilogy()
for i in range(1,22): 
    annotate('%i'%i, xy = (states[i]['H'],states[i]['P']))
xlabel("Specific Enthalpy (J/kg)")
ylabel("Pressure (Pa)")
xlim(1.0e4,4.0e6)
ylim(1e3,1e9)

# Draws the main cycle
plot(process1to2['H'],process1to2['P'],'r')
plot(process2to3['H'],process2to3['P'],'r')
plot(process3to4['H'],process3to4['P'],'r')
plot(process4to5['H'],process4to5['P'],'r')
plot(process5to6['H'],process5to6['P'],'r')
plot(process6to7['H'],process6to7['P'],'r')
plot(process7to8['H'],process7to8['P'],'r')
plot(process8to9['H'],process8to9['P'],'r')
plot(process9to10['H'],process9to10['P'],'r')
plot(process10to11['H'],process10to11['P'],'r')
plot(process11to12['H'],process11to12['P'],'r')
plot(process12to13['H'],process12to13['P'],'r')
plot(process13to14['H'],process13to14['P'],'r')
plot(process14to21['H'],process14to21['P'],'r')
plot(process21to1['H'],process21to1['P'],'r')

# Draws the reheat processes
plot(process2to15['H'],process2to15['P'],'r')
plot(process15to16['H'],process15to16['P'],'r')
plot(process3to17['H'],process3to17['P'],'r')
plot(process16to17['H'],process16to17['P'],'r')
plot(process17to18['H'],process17to18['P'],'r')
plot(process7to19['H'],process7to19['P'],'r')
plot(process20to9['H'],process20to9['P'],'r')
plot(process19to20['H'],process19to20['P'],'r')
plot(process6to12['H'],process6to12['P'],'r')
plot(process18to12['H'],process18to12['P'],'r')

# Completes the cycle diagram and shows it on the graph
plot([states[2]['H'],states[15]['H']],[states[2]['P'],states[15]['P']],'r')
plot([states[3]['H'],states[17]['H']],[states[3]['P'],states[17]['P']],'r')
plot([states[7]['H'],states[19]['H']],[states[7]['P'],states[19]['P']],'r')
showme()
clf()

##############################################################
# The following section of code plots the T-s diagram        #
##############################################################

# Draws the graph of temperature vs. specific entropy
title("T-s Diagram with States Labeled")
ts_phase_envelope('water',fill = True)
for i in range(1,22):
    annotate('%i'%i, xy = (states[i]['S'],states[i]['T']))
xlabel("Specific Entropy (J/kgK)")
ylabel("Temperature (K)")
xlim(0,1.0e4)
ylim(200,1200)

# Draws the main cycle
plot(process1to2['S'],process1to2['T'],'r')
plot(process2to3['S'],process2to3['T'],'r')
plot(process3to4['S'],process3to4['T'],'r')
plot(process4to5['S'],process4to5['T'],'r')
plot(process5to6['S'],process5to6['T'],'r')
plot(process6to7['S'],process6to7['T'],'r')
plot(process7to8['S'],process7to8['T'],'r')
plot(process8to9['S'],process8to9['T'],'r')
plot(process9to10['S'],process9to10['T'],'r')
plot(process10to11['S'],process10to11['T'],'r')
plot(process11to12['S'],process11to12['T'],'r')
plot(process12to13['S'],process12to13['T'],'r')
plot(process13to14['S'],process13to14['T'],'r')
plot(process14to21['S'],process14to21['T'],'r')
plot(process21to1['S'],process21to1['T'],'r')

# Draws the reheat processes
plot(process2to15['S'],process2to15['T'],'r')
plot(process15to16['S'],process15to16['T'],'r')
plot(process3to17['S'],process3to17['T'],'r')
plot(process16to17['S'],process16to17['T'],'r')
plot(process17to18['S'],process17to18['T'],'r')
plot(process7to19['S'],process7to19['T'],'r')
plot(process20to9['S'],process20to9['T'],'r')
plot(process19to20['S'],process19to20['T'],'r')
plot(process6to12['S'],process6to12['T'],'r')
plot(process18to12['S'],process18to12['T'],'r')

# Completes the cycle diagram and draws it on the graph
process2to15line = stater('T',states[15]['T'],'Q',1,'water')
process3to17line = stater('T',states[17]['T'],'Q',1,'water')
process7to19line = stater('T',states[19]['T'],'Q',1,'water')
plot([process2to15line['S'],states[15]['S']],[process2to15line['T'],states[15]['T']],'r')
plot([process3to17line['S'],states[17]['S']],[process3to17line['T'],states[17]['T']],'r')
plot([process7to19line['S'],states[19]['S']],[process7to19line['T'],states[19]['T']],'r')
showme()
clf()

##############################################################
# The following section of code calculates the capital cost  # # of the power plant and plots the NPV over 30 years         #
# assuming a discount rate of 6 percent
##############################################################

# Reference: http://link.springer.com/article/10.1007/s40092-015-0116-8
boiler = 76000000.     # cost of a boiler in $
turbines = 6.*3500000. # cost of six steam turbines
pump1 = 35000.         # cost of a main boiler feed pump
pump2 = 9000.          # cost of a condensate pump
condenser = 17000000.  # cost of a condenser
civil = 58000000.      # cost of civil construction
electrical = 60000000. # cost of electrical construction

# Reference: http://web.ornl.gov/info/reports/1952/3445603531612.pdf
closed_heaters = 3.*30000. # cost of three closed heaters
open_heater = 40000.       # cost of a deaerating open heater

#Reference: http://hisunvalve.m.sell.ecer.com/pz6b8605b-api-electric-gate-valve-z941h-150lb-of-power-plant-valve.html
valves = 3.*500. # cost of three power plant valves

# Total capital cost, fuel cost, and revenues
initial_cost = boiler+turbines+pump1+pump2+condenser+civil+electrical+closed_heaters+open_heater+valves
input_cost = Q_in * f_cost
output_revenue = W_net * e_cost
total_revenue = output_revenue - input_cost
discount_rate = .06

# Defines a function that calculates the return on investment year after year
def tnpv(rate):
    a = [-initial_cost]
    npvs = []
    for i in range(30): a.append(total_revenue)
    for i in range(len(a)):
        npvs.append(npv(rate, a[0:i+1]))
    ts = range(1, len(npvs)+1)
    return ts, npvs

# Calculates the revenue curve
ttp = []
rates = [discount_rate]
for rate in rates:
    a = tnpv(discount_rate)
    for i in a[1]:
        if i > 0:
            ttp.append(a[1].index(i))
            break
    plot(a[0], a[1], label = "discount rate = %s%%"% (str(rate * 100)))

# Plot of NPV vs. Time for the power plant
axhline(0, color = 'k', linestyle = "--")
annotate("time to profit", xy = (0.3,10))
title("NPV vs. Time")
xlabel("Time (years)")
ylabel("NPV ($)")
legend(loc="best")
showme()
clf()

# Prints the initial investment and yearly profit/revenue
print "Initial Investment    = $%.1f million" % (initial_cost/1.0e6)
print "Fuel cost                 = $%.1f million/year" % (input_cost/1.0e6)
print "Electricity revenue  = $%.1f million/year" % (output_revenue/1.0e6)
print "Net revenue            = $%.1f million/year" % (total_revenue/1.0e6)