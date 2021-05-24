# Sizing parameters
import importlib 
import pandas as pd

M_OUT  = importlib.import_module('readModelOutput')

CAPEX_Hp = pd.DataFrame()

numHP = 14560. # 14560 kr/kW from experience
numTES = 2700. # 2700 sek/m3 Technology data for energy plants (2012)

for building in M_OUT.buildings:

    CAPEX_Hp['{}'.format(building)] = [float(M_OUT.df['{}'.format(building)][11]) * numHP + float(M_OUT.df['{}'.format(building)][12]) * numTES]   
	
CAPEXtot = CAPEX_Hp   
	


