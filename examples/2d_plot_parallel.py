from MultiExodusReader import MultiExodusReader
import multiprocessing as mp
import glob

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PolyCollection
import matplotlib
import numpy as np
from time import time
import os

#WE READ THE EXODUS FILE ONCE FOR EACH PROCESS --> MAKE SURE SYSTEM HAS SUFFICIENT RAM FOR THIS
filenames = '2D/grain_growth_2D_graintracker_out.e*'                             #STAR REPRESENTS ALL FILES FOLLOWING THIS TEMPLATE
files_list = glob.glob(filenames)
MF = MultiExodusReader(filenames)
times = MF.global_times

#Function that plots a single frame
def plot_this_frame(i,frame_time):
    fig, ax = plt.subplots()

    x,y,z,c = MF.get_data_at_time('unique_grains',frame_time)               #Read coordinates and variable value --> Will be parallelized in future
    coords = np.asarray([ np.asarray([x_val,y_val]).T for (x_val,y_val) in zip(x,y) ])
    p = PolyCollection(coords, cmap=matplotlib.cm.coolwarm, alpha=1,edgecolor='k')      #Edge color can be set if you want to show mesh

    ## Map plot variable range to color range
    c_min = np.amin(c)
    c_max = np.amax(c)
    colors = 255*(c - c_min)/(c_max-c_min)
    prev_coords = np.copy(coords)

    p.set_array(np.array(colors) )
    ax.add_collection(p)
    ax.set_xlim([0,1000])                                                                   #You can use x and y arrays for setting this, but usually it is easier to manually set
    ax.set_ylim([0,1000])
    ax.set_aspect('equal')                                                                  #Ensures mesh image has same aspect ratio as physical dimensions
    fig.colorbar(p,label="Unique grains")
    fig.savefig('2D/2d_render_'+str(i)+'.png',dpi=500,transparent=True )             #Remember to create the folder pyrender to store images in!!
    plt.close(fig)
    return (True)


#IF IN MAIN PROCESS
if __name__ == "__main__":
    #HOW MANY PROCESSES IN PARALLEL
    n_procs = 10
    #GENERATE TIME STEPS FOR FRAMES TO BE RENDERED
    n_frames = 200
    t_max = times[-1]
    t_frames =  np.linspace(0,t_max,n_frames)
    idx_frames = [ np.where(times-t_frames[i] == min(times-t_frames[i],key=abs) )[0][0] for i in range(n_frames) ]
    frame_times = np.asarray(times)[idx_frames]
    en_frame_times = list(enumerate(frame_times))

    #CREATE A PROCESS POOL
    pool = mp.Pool(n_procs)

    #DISTRIBUTE FRAME WRITING TASK TO ALL PROCESSES --> ALWAYS USE SYNC DISTRIBUTION, ASYNC CAUSES ISSUES WITH FILE READING
    ex_files = [pool.apply(plot_this_frame,args=(en_frame_time)) for en_frame_time in en_frame_times  ]

    #CLOSE PROCESS POOL AND COMPILE RESULTS
    pool.close()
    pool.join()
