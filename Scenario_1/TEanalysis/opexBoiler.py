# Perfomance from the simulations are needed
import importlib
MOUT  = importlib.import_module('readModelOutput')
IC_Boiler  = importlib.import_module('capexBoiler')

# remember revenue from el

OPEXBoilerFixed = 0.03 * IC_Boiler.CAPEX_Boiler # kr
OPEXBoilerVariable = 1.57 * MOUT.result_Qhob_tot # 0.15€/MWhth --> 1.57 kr/MWhth Apparently this is the output. The primary energy is used for the emissions


# Plant and Network
OPEXtot = OPEXBoilerFixed + OPEXBoilerVariable;


