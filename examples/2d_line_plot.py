#SHOWS HOW TO DO A LINE PLOT ON MESH
from MultiExodusReader import MultiExodusReader

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib
import numpy as np
from time import time
import os
import math

fig, (ax1,ax2) = plt.subplots(1,2,figsize=(7,3),dpi = 500)
filenames = '2D/grain_growth_2D_graintracker_out.e*'                             #Star represents all files following this template

##Open multi exodus reader
MF = MultiExodusReader(filenames)

##List of all times for which exodus is read
times = MF.global_times


x,y,z,c = MF.get_data_at_time('bnds',MF.global_times[-1])               #Read coordinates and variable value --> Will be parallelized in future

#Get center of each cell
X_mean = np.mean(x,1)
Y_mean = np.mean(y,1)

P1 = [0,0]
P2 = [1000,1000]
n_points = 1000

D = math.sqrt(sum([ (P2[i] - P1[i])**2 for i in range(len(P1)) ]) )

d = np.linspace(0,D,n_points)


P_x = P1[0] + d*(P2[0] -P1[0] )/D
P_y = P1[1] + d*(P2[1] -P1[1] )/D

P = np.asarray([P_x,P_y]).T

plot_val = []
for point in P:
    dst_sq = (X_mean-point[0])**2 + (Y_mean - point[1])**2
    nearest_idx = np.argmin(dst_sq)
    plot_val+=[c[nearest_idx] ]

ax2.plot(d,plot_val,'k')

xmin = 0
xmax = 1500
ymin = -0.1
ymax = 1.1

ax2.set_xlim([0,xmax])                                                                   #You can use x and y arrays for setting this, but usually it is easier to manually set
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


##2D render
coords = np.asarray([ np.asarray([x_val,y_val]).T for (x_val,y_val) in zip(x,y) ])
patches = [Polygon(points) for points in coords]                                        #Patch collection sets all the polygons we drew using the mesh
p = PatchCollection(patches, cmap=matplotlib.cm.coolwarm, alpha=1)#,edgecolor='k')      #Edge color can be set if you want to show mesh

## Map plot variable range to color range
c_min = 0 #np.amin(c)
c_max = 1 #np.amax(c)
colors = 255*(c - c_min)/(c_max-c_min)

p.set_array(np.array(colors) )
ax1.add_collection(p)

##Drawing the line we are plotting
ax1.plot(P[:,0],P[:,1],'k-',linewidth=1.0)

ax1.set_xlim([0,1000])                                                                   #You can use x and y arrays for setting this, but usually it is easier to manually set
ax1.set_ylim([0,1000])
ax1.set_aspect('equal')                                                                  #Ensures mesh image has same aspect ratio as physical dimensions
cbar = fig.colorbar(p,label="bnds",ax=ax1,fraction=0.046, pad=0.04)
cbar.ax.tick_params(labelsize=6)
cbar.ax.set_ylabel("bnds",fontsize=7,fontweight='bold')
####
                                                             #Ensures mesh image has same aspect ratio as physical dimensions

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

plt.tight_layout()

fig.savefig('2d_lineplot.png',dpi=500,transparent=True)             #Remember to create the folder pyrender to store images in!!
plt.close()
