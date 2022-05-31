from MultiExodusReader import MultiExodusReader

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib
import numpy as np
from time import time
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from mpl_toolkits.mplot3d import Axes3D

#EXODUS FILE FOR RENDERING
#ANY CHARACTER(S) CAN BE PLACED IN PLACE OF THE *, EG. 2D/grain_growth_2D_graintracker_out.e.1921.0000 or 2D/grain_growth_2D_graintracker_out.e-s001
filenames = '3D/grain_growth_3D_out.e*'                             #Star represents all files following this template

#READ EXODUS FILE SERIES WITH MultiExodusReader
MF = MultiExodusReader(filenames)

#GET A LIST OF SIMULATION TIME POINTS
times = MF.global_times

#GENERATE FIGURE WINDOW AND SUBPLOT AXIS
fig = plt.figure()
ax = fig.add_subplot('111',projection='3d')

#GET X,Y,Z AND C (UNIQUE GRAINS VALUES) AT CURRENT TIME STEP
x,y,z,c = MF.get_data_at_time('unique_grains',MF.global_times[-1])               #Read coordinates and variable value --> Will be parallelized in future

#CREATE A COLORMAP OBJECT (cw) THAT CONVERTS VARIABLE VALUE c INTO A RGBA VALUE
c_min = np.amin(c)
c_max = np.amax(c)
#USING COLORMAP HSV. MATPLOTLIB HAS A LIST OF COLORMAPS YOU CAN USE, OR YOU CAN EVEN GENERATE YOUR OWN CUSTOM MAP
cw = matplotlib.cm.ScalarMappable(cmap=matplotlib.cm.hsv)
cw.set_array([c_min,c_max])

#CONVERT VARIABLE VALUES TO RGBA VALUES
C = cw.to_rgba(c)

#GENERATE CORNER POINT COORDINATES FOR THE QUAD8 MESH POLYGONS
coords = np.dstack([x,z,y])

#REPEAT THE COLORING ARRAY 3 TIMES, ONCE FOR EACH SURFACE
colors = np.repeat(C,3,axis=0)
#GENERATE THE 3 SIDES FOR EACH POLYGON, AND ASSIGN THE CELL VALUE OF THE POLYGON TO THE sides --> WE ONLY RENDER 3 SIDES OF EACH CUBE IN THE POLYGON
surfaces = np.ndarray((coords.shape[0]*3,4,3))
surfaces[0::3]=coords[:,[0,1,2,3],:]
surfaces[1::3]=coords[:,[3,2,6,7],:]
surfaces[2::3]=coords[:,[4,7,3,0],:]

#CREATE A Poly3DCollection FROM OUR SURFACES
P = Poly3DCollection(surfaces, facecolors=colors,   alpha=1.0)

#PLOT THE POLY3DCOLLECTION ON OUR AXIS
collection = ax.add_collection3d(P)

#FIGURE FORMATTING SETTINGS
ax.set_xlim([0,1000])                                                                   #You can use x and y arrays for setting this, but usually it is easier to manually set
ax.set_ylim([0,1000])
ax.set_zlim([0,1000])

#CREATE COLORBAR FROM OUR COLORBAR OBJECT CW
fig.colorbar(cw,label="Unique Grains")

#TIGHT LAYOUT TO AUTOMATICALLY ADJUST BORDERS AND PADDING FOR BEST LOOKING IMAGE
fig.tight_layout()

#SAVE FIGURE IN DESIRED DPI AND TRANSPARENCY
fig.savefig('3D/3d_render.png',dpi=500,transparent=True )             #Remember to create the folder pyrender to store images in!!

#USE PLT.SHOW FOR AN INTERACTIVE 3D DISPLAY OF IMAGE. THIS CAN BE A BIT SLOW TO MANIPULATE DEPENDING ON EXODUS FILE SIZE
plt.show()
