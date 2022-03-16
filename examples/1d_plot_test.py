import matplotlib.pyplot as plt
from MultiExodusReader import MultiExodusReader
import numpy as np

# close existing plots
plt.close('all')
#set plot dimensions
fig = plt.figure(figsize=(3.0,1.85),dpi=500)
plt.rcParams.update({'font.family':'Arial'})
plt.rc('font', family='sans-serif',weight='bold')
##LINE PLOT
ax = fig.add_subplot(111)

# Name of exodus file to plot
filenames = '1D/Ni20Cr_hart.e'

##Open multi exodus reader
MF = MultiExodusReader(filenames)

#All time steps in exodus files
times = MF.global_times

#Read c_Cr data at timestep 1
x,y,z,c = MF.get_data_at_time('c_Cr',MF.global_times[1])
ax.plot(x[:,0],c[:],'r-',linewidth=1.5)

#Read c_Cr data at last timestep
x,y,z,c = MF.get_data_at_time('c_Cr',MF.global_times[-1])
ax.plot(x[:,0],c[:],'b--',linewidth=1.5)


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

#Set axis spine widths
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(1.0)

ax.margins(x=0, y=0)
ax.set_ylabel('Cr atomic fraction',fontsize=7,fontweight='bold')
ax.set_xlabel('X ($\mu$m)',fontsize=7,fontweight='bold')

legend_properties = {'weight':'bold','size':6}
lgd = ax.legend(["time = 0 hrs","time = 1000 hrs"],  bbox_to_anchor = (0.5,-0.2),loc= 'upper center',prop=legend_properties,ncol=2,framealpha=0)

fig.tight_layout(pad=0.3)
plt.savefig('1D/1d_exodus_line_plot.png',dpi=500,transparent=True)
plt.show()
