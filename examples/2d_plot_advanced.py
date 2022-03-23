from MultiExodusReader import MultiExodusReader

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib
import numpy as np
from time import time
import os

filenames = '2D/grain_growth_2D_graintracker_out.e*'                             #Star represents all files following this template

##Open multi exodus reader
MF = MultiExodusReader(filenames)

##List of all times for which exodus is read
times = MF.global_times

##Getting closest time step to desired simulation time for render
n_frames = 1
t_max = times[-1]
t_frames =  np.linspace(0,t_max,n_frames)
idx_frames = [ np.where(times-t_frames[i] == min(times-t_frames[i],key=abs) )[0][0] for i in range(n_frames) ]

##This section onward for each simulation time to render. MF.global_times[index] --> index is time step number
for (i,time_step) in enumerate(idx_frames):
    print( "Rendering frame no. ",i+1)
    fig, ax = plt.subplots()

    x,y,z,c = MF.get_data_at_time('unique_grains',MF.global_times[time_step])               #Read coordinates and variable value --> Will be parallelized in future
    coords = np.asarray([ np.asarray([x_val,y_val]).T for (x_val,y_val) in zip(x,y) ])
    patches = [Polygon(points) for points in coords]                                        #Patch collection sets all the polygons we drew using the mesh
    p = PatchCollection(patches, cmap=matplotlib.cm.coolwarm, alpha=1)#,edgecolor='k')      #Edge color can be set if you want to show mesh

    ## Map plot variable range to color range
    c_min = 0 #np.amin(c)
    c_max = 1 #np.amax(c)
    colors = 255*(c - c_min)/(c_max-c_min)
    prev_coords = np.copy(coords)


    p.set_array(np.array(colors) )
    ax.add_collection(p)
    ax.set_xlim([0,1000])                                                                   #You can use x and y arrays for setting this, but usually it is easier to manually set
    ax.set_ylim([0,1000])
    ax.set_aspect('equal')                                                                  #Ensures mesh image has same aspect ratio as physical dimensions
    fig.colorbar(p,label="Cr mole fraction")
    fig.savefig('2D/2d_fancy_'+str(i)+'.png',dpi=500,transparent=True )             #Remember to create the folder pyrender to store images in!!
    plt.close()
