#SHOWS HOW TO PLOT AN EXODUS FILE AND A POSTPROCESSOR CSV FILE AT THE SAME TIME

#IMPORT MultiExodusReader CLASS TO READ EXODUS FILES
from MultiExodusReader import MultiExodusReader

#MATPLOTLIB
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PolyCollection
import matplotlib

#NUMPY FOR ARRAY HANDLING
import numpy as np

import os
#FOR PLOTTING POSTPROCESSOR OR VECTOR POSTPROCESSOR
import csv

#PLOT FORMAT SETTINGS
plt.rcParams.update({'font.family':'Arial'})
plt.rc('font', family='serif',weight='bold')

#FUNCTION FOR READING CSV FILES AND EXTRACTING LABELS AND RAW DATA FROM THEM --> USES PYTHON CSV MODULE
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

#READ CSV FILE
csv_file = '2D/grain_growth_2D_graintracker_out.csv'
labels,data = getRawData(csv_file,',')

#EXTRACT VARIABLES FOR PLOTTING
time_post_proc = data[labels.index('time') ]
GT_post_proc = data[labels.index('grain_tracker') ]

#EXODUS FILE FOR RENDERING
#ANY CHARACTER(S) CAN BE PLACED IN PLACE OF THE *, EG. 2D/grain_growth_2D_graintracker_out.e.1921.0000 or 2D/grain_growth_2D_graintracker_out.e-s001 
filenames = '2D/grain_growth_2D_graintracker_out.e*'


#READ EXODUS FILE SERIES WITH MultiExodusReader
MF = MultiExodusReader(filenames)

#GET A LIST OF SIMULATION TIME POINTS
times = MF.global_times

#GETTING CLOSEST TIME STEP TO DESIRED SIMULATION TIME FOR RENDER --> TYPICALLY 200 FRAMES WITH 20 FPS GIVES A GOOD 10 S LONG VIDEO
n_frames = 100
t_max = times[-1]
t_frames =  np.linspace(0,t_max,n_frames)
idx_frames = [ np.where(times-t_frames[i] == min(times-t_frames[i],key=abs) )[0][0] for i in range(n_frames) ]

#LOOP OVER EACH TIME STEP IN idx_frames
for (i,time_step) in enumerate(idx_frames):
    print( "Rendering frame no. ",i+1)
    #GENERATE FIGURE WINDOW
    fig, (ax1,ax2) = plt.subplots(1,2,figsize=(7,3),dpi = 500)

    #EXODUS RENDER

    #GET X,Y,Z AND C (UNIQUE GRAINS VALUES) AT CURRENT TIME STEP
    x,y,z,c = MF.get_data_at_time('unique_grains',times[time_step])                     #Read coordinates and variable value

    #GENERATE COORDINATES ARRAY THAT STORES X AND Y POINTS TOGETHER
    coords = np.asarray([ np.asarray([x_val,y_val]).T for (x_val,y_val) in zip(x,y) ])

    #USE POLYCOLLECTION TO DRAW ALL POLYGONS DEFINED BY THE COORDINATES
    p = PolyCollection(coords, cmap=matplotlib.cm.coolwarm, alpha=1)#,edgecolor='k')    #Edge color can be set if you want to show mesh

    #COLOR THE POLYGONS WITH OUR VARIABLE
    p.set_array(np.array(c) )

    #ADD THE POLYGON COLLECTION TO AXIS --> THIS IS WHAT ACTUALLY PLOTS THE POLYGONS ON OUR WINDOW
    ax1.add_collection(p)

    #FIGURE FORMATTING
    ax1.set_xlim([0,1000])                                                              #You can use x and y arrays for setting this, but usually it is easier to manually set
    ax1.set_ylim([0,1000])
    ax1.set_aspect('equal')                                                             #Ensures mesh image has same aspect ratio as physical dimensions

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

    #WE WANT TO PLOT POSTPROCESSOR ONLY UPTO THE TIME WHERE WE HAVE RENDERED THE SIMULATION
    #COMPUTE INDEX OF ARRAY IN POSTP FOR TIME THAT CORRESPONDS TO EXODUS RENDER TIME
    post_proc_idx = time_post_proc.index(times[time_step])

    #PLOT POSTPROC UPTO THAT INDEX
    ax2.plot(time_post_proc[:post_proc_idx],GT_post_proc[:post_proc_idx],'k-',linewidth=1.5)

    #DRAW A STAR AT END POINT OF PLOT TO MAKE IT LOOK NICE
    ax2.plot(time_post_proc[post_proc_idx],GT_post_proc[post_proc_idx],'k*',markersize=5)

    #FIGURE FORMATTING
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

    #TIGHT LAYOUT ADJUSTS BORDERS AND PADDING TO GET THE BEST LOOKING IMAGE
    fig.tight_layout()

    #SAVE FIGURE WITH NAME ENDING IN INDEX OF RENDERED FRAME, DPI =500 AND TRANSPARENT BACKGROUND
    fig.savefig('2D/2d_fancy_'+str(i)+'.png',dpi=500,transparent=True)             #Remember to create the folder pyrender to store images in!!

    #IMPORTANT TO CLOSE FIGURE AFTER YOU ARE DONE WITH IT. OTHERWISE EACH GENERATED FIGURE WILL BE HELD IN MEMORY TILL SCRIPT FINISHES EXECUTION
    plt.close(fig)
