import importlib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

M_OUT  = importlib.import_module('readModelOutput')

results = "Results"

# Set the first plot over the whole year. When you have access to the results you can check the lines by selecting groups of them
# Later you will want to idetify relevant weeks

#_AFTER__________________________________________________________________________________________________
start = 3 + 24 * 64# h/d * d  # 24 * 64
stop = 24 * 78 # h/d * d # 24 * 78
jump = 2
tmr = M_OUT.gf.iloc[start:stop:jump, 0]# range(0,(stop-start),2)
tmr_x = range(0,len(tmr))

for ii in tmr_x:
    tmr.iloc[ii] = tmr.iloc[ii][5:16] 

limit = 100*np.ones(len(tmr))

print(M_OUT.gf.iloc[start:stop:jump, 0])

elements = list(M_OUT.gf.columns)
trafo = elements[1]

cables = elements[2::] # cables = elements[2::]


cables_critical = []
cables_relevant = []

for cable in cables:
    flag_critical = 0
    flag_relevant = 0
	
    for ii in M_OUT.gf.loc[start-1:stop-1:jump,cable]:
        if ii >= 100:
            flag_critical = 1
        if ii > 1:
            flag_relevant = 1   

    if flag_critical > 0:
        cables_critical = cables_critical + [cable]
    if flag_relevant > 0:
        cables_relevant = cables_relevant + [cable]         

cables_interesting = ['Llugnw24','Luddnw3','LU 1',]
			
fig, ax = plt.subplots()
[ax.plot(tmr,M_OUT.gf.loc[start:stop:jump,cable], "o-", alpha=1) for cable in cables_interesting]
ax.plot(tmr,limit, "o-", alpha=1,color='k')

ax.legend(["Cable 1","Cable 2","Cable 3","Limit"],loc="upper right",fontsize=18)
fig.set_figheight(8)
fig.set_figwidth(18)

ax.set_title('(b)',fontweight="bold", size=18) # Title
plt.xlabel(xlabel='Time (h)',fontsize=18)
plt.xticks(np.arange(min(tmr_x), max(tmr_x)+1, 25))
plt.ylabel(ylabel='Cables loading (%)',fontsize=18)
plt.ylim(top=155)
ax.tick_params(labelsize=14)

plt.savefig(results+"\LinesLoading_IT2.png")

#_BEFORE__________________________________________________________________________________________________
fig2, ax2 = plt.subplots()

#[ax.plot(tmr,M_OUT.gf[cable][start:stop:jump], "o-", alpha=1,label=cable) for cable in cables]
[ax2.plot(tmr,M_OUT.gf.loc[start-1:stop-1:jump,cable], "o-", alpha=1) for cable in cables_interesting]
ax2.plot(tmr,limit, "o-", alpha=1,color='k')

ax2.legend(["Cable 1","Cable 2","Cable 3","Limit"],loc="upper right",fontsize=18)
fig2.set_figheight(8)
fig2.set_figwidth(18)

ax2.set_title('(a)',fontweight="bold", size=18) # Title
plt.xlabel(xlabel='time (h)',fontsize=18)
plt.xticks(np.arange(min(tmr_x), max(tmr_x)+1, 25))
plt.ylabel(ylabel='Cables loading (%)',fontsize=18)
plt.ylim(top=155)
plt.ylim(bottom=40)
ax2.tick_params(labelsize=14)

plt.savefig(results+"\LinesLoading_IT1.png")

#_TRANSORMER__________________________________________________________________________________________________
fig3, ax3 = plt.subplots()

ax3.plot(tmr,M_OUT.gf.loc[start-1:stop-1:jump,trafo], "o-", alpha=1,label='Iteration 1')
ax3.plot(tmr,M_OUT.gf.loc[start:stop:jump,trafo], "o-", alpha=1,label='Iteration 2')
ax3.plot(tmr,limit, "o-", alpha=1,label='Limit',color='k')

ax3.legend(fontsize=18)
fig3.set_figheight(8)
fig3.set_figwidth(18)

plt.xlabel(xlabel='Time (h)',fontsize=18)
plt.xticks(np.arange(min(tmr_x), max(tmr_x)+1, 25))
plt.ylabel(ylabel='Transformer loading (%)',fontsize=18)
plt.ylim(top=110)
ax3.tick_params(labelsize=14)

plt.savefig(results+"\TransformerLoading.png")
######################################################################################