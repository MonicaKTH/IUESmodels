# Sizing parameters
import importlib 

M_OUT  = importlib.import_module('readModelOutput')

CAPEX_Boiler = 1570000 * M_OUT.CAPth_Boiler # 0.15 M€/MW --> 1.57 Msek/MW From paper The role of DH  1570000

CAPEXtot = CAPEX_Boiler
