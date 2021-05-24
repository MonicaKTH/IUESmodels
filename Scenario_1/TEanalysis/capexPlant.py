# Sizing parameters
import importlib 

M_OUT  = importlib.import_module('readModelOutput')

CAPEX_Plant = 108600000 * M_OUT.CAPelNet_Plant # [kr] Elforsk

CAPEX_Network = 10319 * M_OUT.CAP_Net  # 10319 SEK/m (for 45 MW and 300 mm pipe diameter)

CAPEX_TES = 1700 * M_OUT.CAPth_TES # 160-260 €/m3 1666.99-2708.85 kr/m3 Technology_Data

CAPEXtot = CAPEX_Plant + CAPEX_Network + CAPEX_TES

 