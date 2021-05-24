# Perfomance from the simulations are needed
import importlib
MOUT  = importlib.import_module('readModelOutput')
IC_Plant  = importlib.import_module('capexPlant')

# remember revenue from el

# Network
OPEXfixed_Network = -0.064 * IC_Plant.CAPEX_Network # kr 
OPEXvariable_Network_OM = 0.01 * IC_Plant.CAPEX_Network # kr

# Plant
Fuel = -130 * MOUT.result_Qplant_PE # From ElForsk: sek/MWh_fuel/y
ElRevenues = MOUT.Pel_sell * MOUT.result_Qplant_El

# From ElForsk: 3140 (kr/kW/year) --> 3140000 (kr/MW/year)
OPEXfixed = 3140000 * MOUT.CAPelNet_Plant + OPEXfixed_Network # kr
#OPEXfixed = 140 * MOUT.result_Qplant_PE + OPEXfixed_Network # Nader
# From ElForsk: 40 (kr/MWh_fuel)
OPEXvariable = 40 * MOUT.result_Qplant_PE + OPEXvariable_Network_OM + Fuel - ElRevenues # kr
#OPEXvariable = 90 * MOUT.result_Qplant_PE + OPEXvariable_Network_OM + Fuel - ElRevenues # kr Nader

# Plant and Network
OPEXtot = OPEXfixed + OPEXvariable


