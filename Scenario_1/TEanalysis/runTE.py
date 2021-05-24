# LCOH is the sum of the LCOHs
import importlib
import numpy as np
import pandas as pd
import math

## DH Plant
import calculateLCOE as lcoe
M_OUT  = importlib.import_module('readModelOutput')
IC_Plant  = importlib.import_module('capexPlant')
OMC_Plant = importlib.import_module('opexPlant')
IC_Hp  = importlib.import_module('capexHp')
OMC_Hp = importlib.import_module('opexHp')
IC_Eb  = importlib.import_module('capexEb')
OMC_Eb = importlib.import_module('opexEb')
IC_Boiler  = importlib.import_module('capexBoiler')
OMC_Boiler = importlib.import_module('opexBoiler')

## Within this study, I use the LCOH from Paper II when it comes to the central plant --> cogeneration plant, central tes and boiler
#LH_Plant = lcoe.LCOH(M_OUT.ir[0],M_OUT.life[0],M_OUT.startLife) # interest rate, life, start
#out_Plant = LH_Plant.step(IC_Plant.CAPEXtot,OMC_Plant.OPEXtot,M_OUT.result_DH_Qth+M_OUT.result_QfromTES_tot) # capex (including network and TES), opex (including to TES and revenue from el), energy (including fgc and from TES, excluding to TES)
out_Plant = [278.93] # sek/MWh

## The central boiler is included in the above figure
#LH_Boiler = lcoe.LCOH(M_OUT.ir[0],M_OUT.life[0],M_OUT.startLife) # interest rate, life, start
#out_Boiler = LH_Boiler.step(IC_Boiler.CAPEXtot,OMC_Boiler.OPEXtot,M_OUT.result_Qhob_tot)
out_Boiler = [0.]

## For the distribute HPs I actually do the calculations, because it is per each
LH_Hp = lcoe.LCOH(M_OUT.ir[1],M_OUT.life[1],M_OUT.startLife) # interest rate, life, start
LH_Eb = lcoe.LCOH(M_OUT.ir[1],M_OUT.life[1],M_OUT.startLife) # interest rate, life, start

tot = M_OUT.result_Qplant_totN + M_OUT.result_QfromTES_tot + M_OUT.result_Qhob_tot + M_OUT.result_Qhp_tot + M_OUT.result_Qeb_tot #Total heat generation

weightedLCOH_hp = 0.
weightedLCOH_eb = 0.
weightedLCOH_hp_capex = 0.
weightedLCOH_eb_capex = 0.
weightedLCOH_hp_opex = 0.
weightedLCOH_eb_opex = 0.
#w_hp = 0.
for building in M_OUT.buildings:
    out_Hp = LH_Hp.step(IC_Hp.CAPEXtot[building][0],OMC_Hp.OPEXtot[building][0],M_OUT.results[building][6]) # the Qhp is part of a dataframe
    w_hp = M_OUT.results[building][6]/tot	
    weightedLCOH_hp = weightedLCOH_hp + out_Hp[0]* 1000 * w_hp # *1000 to switch to sek/MWh 	
    weightedLCOH_hp_capex = weightedLCOH_hp_capex + out_Hp[1]* 1000 * w_hp# *1000 to switch to sek/MWh
    weightedLCOH_hp_opex = weightedLCOH_hp_opex + out_Hp[2]* 1000 * w_hp# *1000 to switch to sek/MWh
		
    out_Eb = LH_Eb.step(IC_Eb.CAPEXtot[building][0],OMC_Eb.OPEXtot[building][0],M_OUT.results[building][7]) # the Qhp is part of a dataframe
    w_eb = M_OUT.results[building][7]/tot		
    weightedLCOH_eb = weightedLCOH_eb + out_Eb[0]* 1000 * w_eb# *1000 to switch to sek/MWh
    weightedLCOH_eb_capex = weightedLCOH_eb_capex + out_Eb[1]* 1000 * w_eb# *1000 to switch to sek/MWh
    weightedLCOH_eb_opex = weightedLCOH_eb_opex + out_Eb[2]* 1000 * w_eb# *1000 to switch to sek/MWh
   
# The result from the loop is the summation of the weighted LCOH (numerator) for all the HPs

w_dh = (M_OUT.result_Qplant_totN+M_OUT.result_QfromTES_tot)/tot
weightedLCOH_dh = out_Plant[0] * w_dh # Weighted LCOH (numerator) for the DH system

## Final LCOH
if math.isnan(weightedLCOH_hp):
    weightedLCOH_hp = 0
    weightedLCOH_hp_capex = 0
    weightedLCOH_hp_opex = 0
if math.isnan(weightedLCOH_eb):
    weightedLCOH_eb = 0
    weightedLCOH_eb_capex = 0
    weightedLCOH_eb_opex = 0
if math.isnan(weightedLCOH_dh):
    weightedLCOH_dh = 0
		
LCOH_life = (weightedLCOH_hp + weightedLCOH_eb + weightedLCOH_dh)
LCOH_DH = weightedLCOH_dh/LCOH_life*100
LCOH_HPs = weightedLCOH_hp/LCOH_life*100
LCOH_EBs = weightedLCOH_eb/LCOH_life*100
LCOH_HPs_capex = weightedLCOH_hp_capex/weightedLCOH_hp * 100
LCOH_HPs_opex = weightedLCOH_hp_opex/weightedLCOH_hp * 100
LCOH_EBs_capex = weightedLCOH_eb_capex/max(0.0000001,weightedLCOH_eb) * 100
LCOH_EBs_opex = weightedLCOH_eb_opex/max(0.0000001,weightedLCOH_eb) * 100

print('LCOH TOT',LCOH_life)
print('LCOH DH share',LCOH_DH)
print('LCOH HPs share',LCOH_HPs)
print('LCOH EBs share',LCOH_EBs)
print('LCOH HPs capex share',LCOH_HPs_capex)
print('LCOH HPs opex share',LCOH_HPs_opex)
print('LCOH EBs capex share',LCOH_EBs_capex)
print('LCOH EBs opex share',LCOH_EBs_opex)

# Emissions
CO2spec_el = 125./1000. # kg/MWh --> kg/kWh
CO2spec_dh = 69. /1000.# 69 gr/kWh -->kg/kWh

CO2_el = CO2spec_el * (M_OUT.result_PELhp_tot + M_OUT.result_PELeb_tot)/1000 #t
CO2_dh = CO2spec_dh * (M_OUT.result_Qplant_totN+M_OUT.result_QfromTES_tot)/1000 #t

CO2_tot = (CO2_el + CO2_dh) # t
CO2_DH_share = CO2_dh/CO2_tot *100
CO2_EL_share = CO2_el/CO2_tot *100

print('CO2 [t]',CO2_tot)
print('CO2 DH share[t]',CO2_DH_share)
print('CO2 EL share[t]',CO2_EL_share)

print('overloadings',M_OUT.overloadings)
print('Pure demand',M_OUT.HSUB_Qdem_tot)
print('charge - waste',M_OUT.result_QtesCandSP_tot - M_OUT.result_QtesD_tot)

TESres = pd.DataFrame({
'LCOH [sek/kWh]':LCOH_life,
'LCOH HPs [sek/kWh]':LCOH_HPs,
'LCOH EBs [sek/kWh]':LCOH_EBs,
'LCOH DH [sek/kWh]':LCOH_DH,
'LCOH HPs capex [sek/kWh]':LCOH_HPs_capex,
'LCOH HPs opex [sek/kWh]':LCOH_HPs_opex,
'LCOH EBs capex [sek/kWh]':LCOH_EBs_capex,
'LCOH EBs opex [sek/kWh]':LCOH_EBs_opex,
'CO2 [t]': CO2_tot,
'CO2 dh [t]': CO2_DH_share,
'CO2 el [t]': CO2_EL_share,
'overloadings': M_OUT.overloadings,
'Qdh [kWh]': M_OUT.result_Qplant_totN,
'Qtes [kWh]': M_OUT.result_QtesD_tot,
'Qhp [kWh]': M_OUT.result_Qhp_tot,
'Qeb [kWh]': M_OUT.result_Qeb_tot},
index=list('0'))

# Save to csv
TESres.to_csv('Results\TEresults.csv')


