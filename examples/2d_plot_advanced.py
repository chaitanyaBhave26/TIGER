##Shows how to plot csv and exodus at the same time

from MultiExodusReader import MultiExodusReader

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib
import numpy as np
from time import time
import os
import csv

plt.rcParams.update({'font.family':'Arial'})
plt.rc('font', family='serif',weight='bold')

def getRawData(fileName, delim): # extract raw data from csv file
    rawData = []
    with open(fileName, 'r') as f:
        CSVReader = csv.reader(f, delimiter = delim, skipinitialspace = True)
        labels = next(CSVReader)
        array_size = len(labels)
        rawData = [ [] for i in range(array_size)]
        for row in CSVReader:
            for (i,val) in enumerate(row):
                rawData[i].append(float(val) )
    return (labels,rawData)

csv_file = '2D/grain_growth_2D_graintracker_out.csv'
labels,data = getRawData(csv_file,',')

time_post_proc = data[labels.index('time') ]
GT_post_proc = data[labels.index('grain_tracker') ]


filenames = '2D/grain_growth_2D_graintracker_out.e*'                             #Star represents all files following this template


##Open multi exodus reader
MF = MultiExodusReader(filenames)

##List of all times for which exodus is read
times = MF.global_times

##Getting closest time step to desired simulation time for render --> Typically 200 frames with 20 fps gives a good 10 s long video
n_frames = 100
t_max = times[-1]
t_frames =  np.linspace(0,t_max,n_frames)
idx_frames = [ np.where(times-t_frames[i] == min(times-t_frames[i],key=abs) )[0][0] for i in range(n_frames) ]

##This section onward for each simulation time to render. MF.global_times[index] --> index is time step number
for (i,time_step) in enumerate(idx_frames):
    print( "Rendering frame no. ",i+1)
    fig, (ax1,ax2) = plt.subplots(1,2,figsize=(7,3),dpi = 500)

    # fig, (ax1,ax2) = plt.subplots(1,2,figsize=(7,3),dpi = 500)

    #EXODUS RENDER
    x,y,z,c = MF.get_data_at_time('unique_grains',times[time_step])               #Read coordinates and variable value --> Will be parallelized in future
    coords = np.asarray([ np.asarray([x_val,y_val]).T for (x_val,y_val) in zip(x,y) ])
    patches = [Polygon(points) for points in coords]                                        #Patch collection sets all the polygons we drew using the mesh
    p = PatchCollection(patches, cmap=matplotlib.cm.coolwarm, alpha=1)#,edgecolor='k')      #Edge color can be set if you want to show mesh

    ## Map plot variable range to color range
    c_min = 0 #np.amin(c)
    c_max = 1 #np.amax(c)
    colors = 255*(c - c_min)/(c_max-c_min)
    prev_coords = np.copy(coords)


    p.set_array(np.array(colors) )
    ax1.add_collection(p)
    ax1.set_xlim([0,1000])                                                                   #You can use x and y arrays for setting this, but usually it is easier to manually set
    ax1.set_ylim([0,1000])
    ax1.set_aspect('equal')                                                                  #Ensures mesh image has same aspect ratio as physical dimensions

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

    cbar = fig.colorbar(p,ax=ax1,fraction=0.046, pad=0.04)
    cbar.ax.tick_params(labelsize=6)
    cbar.ax.set_ylabel("Unique grains",fontsize=7,fontweight='bold')

    #POSTPROCESSOR RENDER
    post_proc_idx = time_post_proc.index(times[time_step])
    ax2.plot(time_post_proc[:post_proc_idx],GT_post_proc[:post_proc_idx],'k-',linewidth=1.5)
    ax2.plot(time_post_proc[post_proc_idx],GT_post_proc[post_proc_idx],'k*',markersize=5)
    xmax = 2000
    ymax = 100
    ymin = 40
    ax2.set_xlim([0,xmax])                                                                   #You can use x and y arrays for setting this, but usually it is easier to manually set
    ax2.set_ylim([ymin,ymax])

    xticks=[ int(tick) for tick in np.linspace(0,xmax, 6)]
    ax2.set_xticks( xticks )
    ax2.set_xticklabels( xticks ,fontsize=6,fontweight='bold')
    yticks = [ int(tick) for tick in np.linspace(ymin,ymax, 4)]
    ax2.set_yticks( yticks)
    ax2.set_yticklabels( yticks,fontsize=6,fontweight='bold')
    ax2.tick_params(axis='x',direction='in',length=5)
    ax2.tick_params(axis='y',direction='in',which='major',length=5)
    ax2.margins(x=0, y=0)
    ax2.set_ylabel('Grain tracker',fontsize=7,fontweight='bold')
    ax2.set_xlabel('Time (s)',fontsize=7,fontweight='bold')

    fig.tight_layout()
    fig.savefig('2D/2d_fancy_'+str(i)+'.png',dpi=500,transparent=True)             #Remember to create the folder pyrender to store images in!!
    plt.close()
