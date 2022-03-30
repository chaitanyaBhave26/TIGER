##EXAMPLE FOR LINE PLOT ON EXODUS FILES

import matplotlib.pyplot as plt
from MultiExodusReader import MultiExodusReader
import numpy as np

#CLOSE EXISTING PLOTS
plt.close('all')

#SET PLOT PARAMS
fig = plt.figure(figsize=(3.0,1.85),dpi=500)
plt.rcParams.update({'font.family':'Arial'})
plt.rc('font', family='sans-serif',weight='bold')

ax = fig.add_subplot(111)

#NAME OF EXODUS FILE TO PLOT
filenames = '1D/Ni20Cr_hart.e'

#OPEN MULTI EXODUS READER
MF = MultiExodusReader(filenames)

#ALL TIME STEPS IN EXODUS FILES
times = MF.global_times

#READ c_Cr DATA at FIRST TIMESTEP
x,y,z,c = MF.get_data_at_time('c_Cr',times[1])

# For 1D, EXODUS STORES X ELEMENTS TWICE, SO WE SELECT FIRST SET USING x[:,0]
ax.plot(x[:,0],c[:],'r-',linewidth=1.5)

#READ c_Cr DATA at LAST TIMESTEP
x,y,z,c = MF.get_data_at_time('c_Cr',times[-1])

ax.plot(x[:,0],c[:],'b--',linewidth=1.5)

#FORMATTING PLOT
xmin = 40.0
xmax = 160.0
ymin = 0
ymax = 0.25


ax.set_xlim(xmin,xmax)
ax.set_ylim(ymin,ymax)

xticks=[ int(tick) for tick in np.linspace(xmin,xmax, 7)]
ax.set_xticks(xticks)  # arbitrary chosen
ax.set_xticklabels(xticks,fontsize=6)


yticks= np.around(np.linspace(ymin,ymax, 6),1)
ax.set_yticks(yticks)  # arbitrary chosen
ax.set_yticklabels(yticks,fontsize=6)


ax.tick_params(axis='x',direction='in',length=5)
ax.tick_params(axis='y',direction='in',which='major',length=5)

#ADD BORDER LINES FOR AXES
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(1.0)

ax.margins(x=0, y=0)
ax.set_ylabel('Cr atomic fraction',fontsize=7,fontweight='bold')
ax.set_xlabel('X ($\mu$m)',fontsize=7,fontweight='bold')

legend_properties = {'weight':'bold','size':6}
lgd = ax.legend(["time = 0 hrs","time = 1000 hrs"],  bbox_to_anchor = (0.5,-0.2),loc= 'upper center',prop=legend_properties,ncol=2,framealpha=0)

fig.tight_layout(pad=0.3)

#SAVEFIG ALLOWS YOU TO SAVE FIGURE IN DESIRED DPI AND TRANSPARENCY
plt.savefig('1D/1d_exodus_line_plot.png',dpi=500,transparent=True)

#PLT.SHOW FOR LOOKING AT PLOT IN INTERACTIVE VIEW
plt.show()
