import numpy as np
import importlib
import pandas as pd
import matplotlib.pyplot as plt

## GRID ################################################################
gf=pd.read_csv('..\TEsimulation\Results\Files\GridLoading.csv')

## DR ################################################################
df=pd.read_csv('..\TEsimulation\AddFiles\Blocks_data.csv',sep=';')
buildings = list(df)[2::]

results = pd.DataFrame()
results['Indicator']=['DHW','HP_Pel','HP_Qth','EB_Pel','TES_Qch','TES_Qdis','HP_Qth_net','EB_Qth','DH_Qth','Qth_dem','HP_Disconnections']
# Twiks
m2ref = 4889 # B5
dhw=pd.read_csv('SummerAddition\Dhw.csv',sep=';') #hourly DHW for one day in Wh for 48m2


for building in buildings:

    #paths to simulation output files#
    eflowsFileDR = "..\TEsimulation\Results\Files\{}\EnergyFlows.csv".format(building)

    #read data from output files
    eflowsDataDR = pd.read_csv(eflowsFileDR)
    endF = len(eflowsDataDR.index) # EVEN

    #extract field power values#
    series_HP_Pel = eflowsDataDR.loc[3:endF:2, 'HP_Pel_kW'] #eflowsDataDR['HP_Pel_kW'] 
    series_HP_Qth = eflowsDataDR.loc[3:endF:2, 'HP_Qth_kW']	
    series_EB_Pel = eflowsDataDR.loc[3:endF:2, 'EB_Pel_kW']	
    series_TES_SoC = eflowsDataDR.loc[3:endF:2, 'TES_SoC']
    series_TES_Qflow = eflowsDataDR.loc[3:endF:2, 'TES_Qflow_kWh']    
    series_TES_Qch =series_TES_Qflow[series_TES_Qflow > 0]
    series_TES_Qdis =series_TES_Qflow[series_TES_Qflow < 0]
	
    series_HSUB_Qdem = eflowsDataDR.loc[1:(endF-2):2, 'HSUB_Qdem_B_kW'] # Heating demand from the reference building block   


    #series_CTRL_Tth = eflowsDataDR.loc[3:endF:2, 'CTRL_Tth_Cdeg'] # Heating demand from the reference building block 
    #series_ROOM_Tindoor = eflowsDataDR.loc[1:(endF-2):2, 'ROOM_Tindoor_Cdeg'] # Heating demand from the reference building block 
    series_HP_QthSP = eflowsDataDR.loc[3:endF:2, 'CTRL_Qth_spilled_kW'] # Spilled heat
    series_DH_Qth = eflowsDataDR.loc[3:endF:2, 'CTRL_QDH_B_kW'] # DH 
	
    overloadings = 0.	

    for zz in series_HP_Pel:

        if zz == 0.:
	        overloadings = overloadings +1

    ## Calculations
    results['{}'.format(building)] = sum(dhw['DHW (W)']) / 48 * float(df["{}".format(building)][3]) /1000 * (365 - 80 * 2) #[kWh] Summer days = (Days in a year minus the days considered as winter season) 
    results['{}'.format(building)][1] = sum(series_HP_Pel)  * 2 + results['{}'.format(building)][0] / 3.2 #[kWh]
    results['{}'.format(building)][2] = sum(series_HP_Qth)  * 2 + results['{}'.format(building)][0] #[kWh]
    results['{}'.format(building)][3] = sum(series_EB_Pel)  * 2 #[kWh]
    results['{}'.format(building)][4] = sum(series_TES_Qch)  * 2 + sum(series_HP_QthSP)  * 2#[kWh]
    results['{}'.format(building)][5] = sum(series_TES_Qdis)  * 2 #[kWh] THIS IS NEGATIVE	   
    results['{}'.format(building)][6] = results['{}'.format(building)][2] - results['{}'.format(building)][5] - results['{}'.format(building)][4] # hp + tes to load	
    results['{}'.format(building)][7] = results['{}'.format(building)][3] * 0.9 # Heat from the eb
    results['{}'.format(building)][8] = sum(series_DH_Qth)  * 2 #[kWh] 
    results['{}'.format(building)][9] = sum(series_HSUB_Qdem)  * 2 #[kWh] 	
    results['{}'.format(building)][10] = overloadings  * 2 #[kWh]	

results.to_csv('Results\BBresults.csv')

result_Qhp_tot = results.sum(axis = 1)[6]
result_Qeb_tot = results.sum(axis = 1)[3] * 0.9
result_QtesD_tot = results.sum(axis = 1)[5]
result_QtesCandSP_tot = results.sum(axis = 1)[4]
result_PELhp_tot = results.sum(axis = 1)[1]
result_PELeb_tot = results.sum(axis = 1)[3]
result_Qsummer = results.sum(axis = 1)[0]
result_DH_Qth_temp = results.sum(axis = 1)[8]
result_HSUB_Qdem = results.sum(axis = 1)[9]

COPhp = 4.65 # Avg 4.65
Pel_sell = 0.375*1000 #sek/MWh
PrVar = 1
Pel_buy = 1 * PrVar #sek/kWh Nader

ir = [0.08,0.04]
life = [30,15]
startLife = 0

## CR ################################################################
eflowsFileCR = '..\TEsimulation\Results\Files\EnergyFlows.csv'
eflowsDataCR = pd.read_csv(eflowsFileCR)
series_DH_PE = eflowsDataCR.loc[3:endF:2, 'DH_PE_MW']
result_DH_Qth = sum(series_DH_PE) * 2  #[kWh] winter season for one building block (ref)

result_DH_Qth = result_DH_Qth_temp

result_Qplant_totN = result_DH_Qth  # [kWh] only the share going to the load
result_QfromTES_tot = 0. # included in the above
result_Qhob_tot = 0. # included in the above

# Pure demand
HSUB_Qdem_tot = result_HSUB_Qdem + result_Qsummer



# Not using this at the moment
CAPel_Plant = 6.6 # MW gross
etaEnet_Plant = 0.19
etaEgross_Plant = 0.22
CAPelNet_Plant = CAPel_Plant * etaEnet_Plant/etaEgross_Plant # MW net
etaH_Plant = 0.67 # Technology_Data

result_Qplant_PE = result_DH_Qth / etaH_Plant # [kWh]
result_Qplant_El = CAPelNet_Plant * 7125# Estimated net electricity generation

CAP_Net = 14800 # m

CAPth_TES = 0. # m3 Central TES

CAPth_Boiler = 0. # MW # Central boiler
etaH_Boiler = 0.8




