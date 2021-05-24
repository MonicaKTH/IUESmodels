# Perfomance from the simulations are needed
import importlib
import pandas as pd

M_OUT  = importlib.import_module('readModelOutput')

OPEXtot = pd.DataFrame()
for building in M_OUT.buildings:

    OPEXHpVariable = M_OUT.Pel_buy * (M_OUT.results[building][3])# kr

    # Plant and Network
    OPEXtot['{}'.format(building)] = [OPEXHpVariable]

