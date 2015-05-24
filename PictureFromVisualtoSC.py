'''
Created on 2 fevr. 2012

@author: Geoffrey Megardon
'''
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from util.SCTransformation import *
from util.util import *

## see an example of how to integrate a grid in MatrixFromVisualtoSC.py
goToFileDir(__file__)
cmap = cm.gray
cmap.set_bad('k',1.) # choose the color and alpha of the background: (k, w, b, g, r)

# retina/visual space in degrees:
ret_width = 60
ret_height = 120
ret_linx = np.around(np.arange(0, ret_width, 0.1), decimals = 1)
ret_liny = np.around(np.arange(-ret_height/2, ret_height/2, 0.1), decimals=1)

# Superior Colliculus space in mm:
col_width = 5
col_height = 6
col_linx =  np.around(np.arange(0, col_width, 0.01), decimals=2)
col_liny = np.around(np.arange(-col_height/2, col_height/2, 0.01), decimals=2)

# Open an image file to be transformed and transform it:
VisualMap = openImg("./receptivefield2.1.png") # you can also create your own matrix
SCMap = transfCartToCol2(VisualMap, ret_linx, ret_liny, col_linx, col_liny)

# Do the figure:
fig = plt.figure(figsize= (16,12), dpi=80)
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

ax1.imshow(VisualMap, cmap= cmap, interpolation = "nearest", extent=[0,60,-60,60])#vmin=np.min(Th), vmax = np.max(Th))
axes = ax1.get_axes()
ax1.set_xlim(0,60)
ax1.set_ylim(-60,60)
#axes.grid(True)

ax2.imshow(SCMap,cmap=cmap, interpolation = "nearest", extent=[0,5,-3,3])
axes = ax2.get_axes()
#axes.grid(True)

# plot the SC grid
toTrace = ( np.array([2, 5, 10, 30, 60]), np.arange(-90,100, 30) )
gridSC = constructSCGrid(*toTrace)
gridRet = constructRetinalGrid(*toTrace)
plotGrid(gridRet, ax1)
plotGrid(gridSC, ax2)

## change the size of the axis font
plt.axis('scaled')
ax2.axis((0.,5.0,-3.,3.))
for tick in ax1.xaxis.get_major_ticks() + ax1.yaxis.get_major_ticks():
    tick.label.set_fontsize(16)
for tick in ax2.xaxis.get_major_ticks() + ax2.yaxis.get_major_ticks():
    tick.label.set_fontsize(16)
plt.savefig("img/toSC-FromPicture.png")
plt.show()

