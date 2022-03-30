from MultiExodusReader import MultiExodusReader

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PolyCollection
import matplotlib
import numpy as np
from time import time
import os

#EXODUS FILE FOR RENDERING
#ANY CHARACTER(S) CAN BE PLACED IN PLACE OF THE *, EG. 2D/grain_growth_2D_graintracker_out.e.1921.0000 or 2D/grain_growth_2D_graintracker_out.e-s001
filenames = '2D/grain_growth_2D_graintracker_out.e*'

#READ EXODUS FILE SERIES WITH MultiExodusReader
MF = MultiExodusReader(filenames)

#GET A LIST OF SIMULATION TIME POINTS
times = MF.global_times

#GETTING CLOSEST TIME STEP TO DESIRED SIMULATION TIME FOR RENDER --> TYPICALLY 200 FRAMES WITH 20 FPS GIVES A GOOD 10 S LONG VIDEO
n_frames = 200
t_max = times[-1]
t_frames =  np.linspace(0,t_max,n_frames)
idx_frames = [ np.where(times-t_frames[i] == min(times-t_frames[i],key=abs) )[0][0] for i in range(n_frames) ]

#LOOP OVER EACH TIME STEP IN idx_frames
for (i,time_step) in enumerate(idx_frames):
    print( "Rendering frame no. ",i+1)
    #GENERATE FIGURE WINDOW
    fig, ax = plt.subplots()

    #GET X,Y,Z AND C (UNIQUE GRAINS VALUES) AT CURRENT TIME STEP
    x,y,z,c = MF.get_data_at_time('unique_grains',MF.global_times[time_step])               #Read coordinates and variable value --> Will be parallelized in future

    #GENERATE COORDINATES ARRAY THAT STORES X AND Y POINTS TOGETHER
    coords = np.asarray([ np.asarray([x_val,y_val]).T for (x_val,y_val) in zip(x,y) ])

    #USE POLYCOLLECTION TO DRAW ALL POLYGONS DEFINED BY THE COORDINATES
    p = PolyCollection(coords, cmap=matplotlib.cm.coolwarm, alpha=1,edgecolor='k')      #Edge color can be set if you want to show mesh

    #COLOR THE POLYGONS WITH OUR VARIABLE
    p.set_array(np.array(colors) )

    #ADD THE POLYGON COLLECTION TO AXIS --> THIS IS WHAT ACTUALLY PLOTS THE POLYGONS ON OUR WINDOW
    ax.add_collection(p)

    #FIGURE FORMATTING

    #SET X AND Y LIMITS FOR FIGURE --> CAN USE x,y ARRAYS BUT MANUALLY SETTING IS EASIER
    ax.set_xlim([0,1000])
    ax.set_ylim([0,1000])
    #SET ASPECT RATIO TO EQUAL TO ENSURE IMAGE HAS SAME ASPECT RATIO AS ACTUAL MESH
    ax.set_aspect('equal')

    #ADD A COLORBAR, VALUE SET USING OUR COLORED POLYGON COLLECTION
    fig.colorbar(p,label="Unique grains")

    #STORE FIGURE IN 2D FOLDER, AND THE NAME ENDS WITH THE INDEX OF THE RENDERED FRAME. DPI = 500 AND TRANSPARENT BACKGROUND
    fig.savefig('2D/2d_render_'+str(i)+'.png',dpi=500,transparent=True )

    #CLOSE FIGURE AFTER YOU ARE DONE WITH IT. OTHERWISE ALL GENERATED FIGURES WILL BE HELD IN MEMORY TILL SCRIPT FINISHES RUNNING
    plt.close(fig)
