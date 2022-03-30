#SHOWS HOW TO DO A LINE PLOT ON A 2D MESH
from MultiExodusReader import MultiExodusReader

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PolyCollection
import matplotlib
import numpy as np
from time import time
import os
import math

#FIGURE PARAMS
fig, (ax1,ax2) = plt.subplots(1,2,figsize=(7,3),dpi = 500)

#FILE NAME STRING. '*' CAN BE REPLACED WITH ANY CHARACTER IN ACTUAL FILE NAME, EG. 2D/grain_growth_2D_graintracker_out.e.1921.0000 OR 2D/grain_growth_2D_graintracker_out.e-s001
filenames = '2D/grain_growth_2D_graintracker_out.e*'                #Star represents all files following this template

#CREATE MULTIEXODUSREADER OBJECT
MF = MultiExodusReader(filenames)

#GET A LIST OF ALL TIMES FROM SIMULATION
times = MF.global_times


x,y,z,c = MF.get_data_at_time('bnds',MF.global_times[-1])           #Read coordinates and variable value --> Will be parallelized in future

#GET CENTER VALUE FOR EACH CELL
X_mean = np.mean(x,1)
Y_mean = np.mean(y,1)

#PARAMETERS OF THE LINE WE WANT TO PLOT VALUES ALONG
P1 = [0,0]                                                          #END POINT
P2 = [1000,1000]                                                    #END POINT
n_points = 1000                                                     #NUM OF POINTS TO SAMPLE ALONG LINE

#GET DISTANCE BETWEEN END POINTS
D = math.sqrt(sum([ (P2[i] - P1[i])**2 for i in range(len(P1)) ]) )
#GET DISTANCES FOR EACH SAMPLE POINT FROM P1
d = np.linspace(0,D,n_points)

#GET X AND Y CO-ORDINATES FOR SAMPLE POINTS
P_x = P1[0] + d*(P2[0] -P1[0] )/D
P_y = P1[1] + d*(P2[1] -P1[1] )/D

#STORE X,Y COORDINATES IN AN ARRAY OF POINTS
P = np.asarray([P_x,P_y]).T

#FOR EACH SAMPLE POINT, FIND VARIABLE VALUE ON THE CLOSEST CELL
plot_val = []
for point in P:
    dst_sq = (X_mean-point[0])**2 + (Y_mean - point[1])**2
    nearest_idx = np.argmin(dst_sq)
    plot_val+=[c[nearest_idx] ]

#PLOT DISTANCE OF POINT FROM P1 (X-AXIS) VS VARIABLE VALUE (Y-AXIS)
ax2.plot(d,plot_val,'k')

#PLOT FORMATTING
xmin = 0
xmax = 1500
ymin = -0.1
ymax = 1.1


ax2.set_xlim([xmin,xmax])
ax2.set_ylim([ymin,ymax])

xticks=[ int(tick) for tick in np.linspace(0,xmax, 6)]
ax2.set_xticks( xticks )
ax2.set_xticklabels( xticks ,fontsize=6,fontweight='bold')
yticks = np.around(np.linspace(ymin,ymax, 7),1)
ax2.set_yticks( yticks)
ax2.set_yticklabels( yticks,fontsize=6,fontweight='bold')
ax2.tick_params(axis='x',direction='in',length=5)
ax2.tick_params(axis='y',direction='in',which='major',length=5)
ax2.margins(x=0, y=0)
ax2.set_ylabel('bnds',fontsize=7,fontweight='bold')
ax2.set_xlabel('Distance ($\mu$m)',fontsize=7,fontweight='bold')


##2D RENDER --> USES THE 2d_plot.py EXAMPLE CODE

#GET POLYGONS FOR EACH CELL IN MESH
coords = np.asarray([ np.asarray([x_val,y_val]).T for (x_val,y_val) in zip(x,y) ])
#USE POLYCOLLECTION TO DRAW ALL THE POLYGONS
p = PolyCollection(patches, cmap=matplotlib.cm.coolwarm, alpha=1)#,edgecolor='k')      #Edge color can be set if you want to show mesh
#USE COLORING VARIABLE 'c' TO COLOR POLYGONS
p.set_array(np.array(c) )
#ADD POLYGON COLLECTION TO AXIS --> THIS ACTUALLY PLOTS THE POLYGONS
ax1.add_collection(p)

#DRAW THE LINE PLOTTED THE VARIABLE ALONG
ax1.plot(P[:,0],P[:,1],'k-',linewidth=1.0)

#PLOT FORMATTING PARAMETERS
ax1.set_xlim([0,1000])                                                                   #You can use x and y arrays for setting this, but usually it is easier to manually set
ax1.set_ylim([0,1000])
ax1.set_aspect('equal')                                                                  #Ensures mesh image has same aspect ratio as physical dimensions
cbar = fig.colorbar(p,label="bnds",ax=ax1,fraction=0.046, pad=0.04)
cbar.ax.tick_params(labelsize=6)
cbar.ax.set_ylabel("bnds",fontsize=7,fontweight='bold')

xticks=[ int(tick) for tick in np.linspace(0,1000, 6)]
ax1.set_xticks( xticks )
ax1.set_xticklabels( xticks ,fontsize=6,fontweight='bold')
yticks = [ int(tick) for tick in np.linspace(0,1000, 6)]
ax1.set_yticks( yticks)
ax1.set_yticklabels( yticks,fontsize=6,fontweight='bold')
ax1.tick_params(axis='x',direction='in',length=5)
ax1.tick_params(axis='y',direction='in',which='major',length=5)
ax1.set_ylabel('Y ($\mu$m)',fontsize=7,fontweight='bold')
ax1.set_xlabel('X ($\mu$m)',fontsize=7,fontweight='bold')

#TIGHT LAYOUT ADJUSTS BORDERS AND PADDING TO GIVE BEST LOOKING IMAGE
plt.tight_layout()

#SAVE FIGURE WITH DPI=500 AND TRANSPARENT BACKGROUND
fig.savefig('2d_lineplot.png',dpi=500,transparent=True)             #Remember to create the folder pyrender to store images in!!
plt.close()
