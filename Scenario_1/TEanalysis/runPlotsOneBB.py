import importlib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

M_OUT  = importlib.import_module('readModelOutput_OneBB')

results = "Results"

#_WEEK 1__________________________________________________________________________________________________
start = 24 * 32 # h/d * d # 1
stop = 24 * 39 # h/d * d  # 24 * 79
tmr = M_OUT.series_time[start:stop]
tmr_x = range(0,len(tmr))
for ii in tmr_x:
    tmr.iloc[ii] = tmr.iloc[ii][5:16] 

fig, ax = plt.subplots()

## One building block
#fig.set_figheight(8)
#fig.set_figwidth(18)
## Demand
#ax.plot(tmr,M_OUT.series_HSUB_Qdem[start:stop], "o-", alpha=1,label='Demand')
## Heat pump
#ax.plot(tmr,M_OUT.series_HP_Qth[start:stop], "--", alpha=1,label='Heat pump')
#
## Thermal energy storage
#ax.plot(tmr,M_OUT.series_TES_Qflow[start:stop], "--", alpha=1,label='Themal storage')
#
## Electrical backup
#plt.plot(tmr,M_OUT.series_EB_Pel[start:stop]*0.9, "--", alpha=1,label='Electrical backup')

## District heating
#ax.plot(tmr,M_OUT.series_DH_Qth[start:stop], "--", alpha=1,label='District heating')

#ax.set_title('(a)',fontweight="bold", size=18,loc="left") # Title
#ax.tick_params(labelsize=14)
#plt.legend(bbox_to_anchor=(0,1.02,1,0.2),ncol=5,loc="lower center",prop={'size': 13})
#plt.xlabel(xlabel='Time (h)',fontsize=18)
#plt.xticks(np.arange(min(tmr_x), max(tmr_x)+1, 25))
#plt.ylabel(ylabel='Heat power (kW)',fontsize=18)
#plt.savefig(results+"\WE1_ThermalP.png")

y = [M_OUT.series_HP_Qth[start:stop],-M_OUT.series_TES_Qflow[start:stop],M_OUT.series_EB_Pel[start:stop]*0.9,M_OUT.series_DH_Qth[start:stop]] 
# Basic stacked area chart.
plt.stackplot(tmr,y, edgecolor='white',labels=[ 'HP','TES','EB', 'DH'])

ax.plot(tmr, M_OUT.series_HSUB_Qdem[start:stop], "k--", alpha=1,label='Heat load', linewidth = 3)
#ax.plot(time, EStsS['EStsS_WHR_DHlosses'], "r--", alpha=1,label='Heat losses', linewidth = 3)
plt.ylim(top=180)
plt.legend(loc='upper left')
ax.tick_params(labelsize=10)
plt.xticks(np.arange(min(tmr_x), max(tmr_x)+1, 41)) # 25
plt.legend(bbox_to_anchor=(0,1.02,1,0.2),ncol=5,loc="lower center",prop={'size': 10},columnspacing=0.5)
plt.xlabel(xlabel='Time (h)',fontsize=16)
plt.ylabel(ylabel='Heat power (kW)',fontsize=16)
plt.savefig(results+"\WE1_ThermalP.png")


# Other
fig1, ax1 = plt.subplots()
color = 'tab:red'
ax1.set_xlabel('Time (h)',fontsize=18)
ax1.set_ylabel('Thermostat setpoint',color=color,fontsize=18)
ax1.plot(tmr, M_OUT.series_CTRL_Tth[start:stop],color=color)
color = 'tab:blue'
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
ax2.set_ylabel('TES state of charge',color=color,fontsize=18)  # we already handled the x-label with ax1
ax2.plot(tmr, M_OUT.series_TES_SoC[start:stop],color=color)
fig1.set_figheight(6)
fig1.set_figwidth(16)
fig1.tight_layout()  # otherwise the right y-label is slightly clipped
ax1.tick_params(labelsize=14)
plt.xticks(np.arange(min(tmr_x), max(tmr_x)+1, 25))
plt.savefig(results+"\WE1_SetPoints.png")

# Weather
fig2, ax2 = plt.subplots()
Toutdoor = pd.read_csv('..\InputData\Weather_Stockholm2016.csv')
fig2.set_figheight(6)
fig2.set_figwidth(16)
ax2.plot(tmr,Toutdoor[start:stop], "o-", alpha=1)
ax2.set_xlabel(xlabel='Time (h)',fontsize=18)
plt.xticks(np.arange(min(tmr_x), max(tmr_x)+1, 25))
ax2.set_ylabel(ylabel='Outdoor Temperature [°C]',fontsize=18)
ax2.tick_params(labelsize=14)
plt.savefig(results+"\WE1_Toutdoor.png")
