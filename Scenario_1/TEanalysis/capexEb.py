# Sizing parameters
import importlib 
import pandas as pd

M_OUT  = importlib.import_module('readModelOutput')

CAPEX_Eb = pd.DataFrame()

numEB = 1360. # 1360 sek/kW Technology data for energy plants (2012)


for building in M_OUT.buildings:

    CAPEX_Eb['{}'.format(building)] = [float(M_OUT.df['{}'.format(building)][13]) * numEB]   
	
CAPEXtot = CAPEX_Eb
	


