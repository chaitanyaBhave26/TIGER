from MultiExodusReader import MultiExodusReader

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib
import numpy as np
from time import time
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from mpl_toolkits.mplot3d import Axes3D

filenames = '3D/grain_growth_3D_out.e*'                             #Star represents all files following this template

##Open multi exodus reader
MF = MultiExodusReader(filenames)

##List of all times for which exodus is read
times = MF.global_times

fig = plt.figure()
ax = fig.add_subplot('111',projection='3d')


x,y,z,c = MF.get_data_at_time('unique_grains',MF.global_times[-1])               #Read coordinates and variable value --> Will be parallelized in future

c_min = np.amin(c)
c_max = np.amax(c)

cw = matplotlib.cm.ScalarMappable(cmap=matplotlib.cm.hsv)
cw.set_array([c_min,c_max])

C = cw.to_rgba(c)

surfaces = []
colors = []

coords = np.asarray([ np.asarray([x_val,y_val,z_val]).T for (x_val,y_val,z_val) in zip(x,y,z) ])
for (i,side) in enumerate(coords):
    sides = [ [side[0],side[1],side[2],side[3]],
                     [side[4],side[5],side[6],side[7]],
                     [side[0],side[1],side[5],side[4]],
                     [side[3],side[2],side[6],side[7]],
                     [side[1],side[2],side[6],side[5]],
                     [side[4],side[7],side[3],side[0]] ]
    c_temp = [C[i] for j in range(6)]
    surfaces+=sides
    colors+=c_temp

P = Poly3DCollection(surfaces, facecolors=colors,   alpha=1.0)
collection = ax.add_collection3d(P)

ax.set_xlim([0,1000])                                                                   #You can use x and y arrays for setting this, but usually it is easier to manually set
ax.set_ylim([0,1000])
ax.set_zlim([0,1000])


fig.colorbar(cw,label="Unique Grains")
fig.tight_layout()
fig.savefig('3D/3d_render.png',dpi=500,transparent=True )             #Remember to create the folder pyrender to store images in!!

plt.show()
