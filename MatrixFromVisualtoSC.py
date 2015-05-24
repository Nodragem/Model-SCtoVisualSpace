'''
Created on 2 fevr. 2012

@author: Geoffrey Megardon
'''
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from util.SCTransformation import *
from util.util import *

## we add a grid and a background color compared to PictureFromVisualtoSC.py. 
goToFileDir(__file__)
cmap = cm.jet # matlab's style of colormap
cmap.set_bad('k',1.) # choose the color and alpha of the background: (k, w, b, g, r)
PLOT_GRID = True; color1 = "black"; color2="black" # choose if you want a grid or not, and the grid's color

# description of the retina/visual space in degrees:
ret_width = 60
ret_height = 120
ret_linx = np.around(np.arange(0, ret_width, 0.1), decimals = 1)
ret_liny = np.around(np.arange(-ret_height/2, ret_height/2, 0.1), decimals=1)

# description of the Superior Colliculus space in mm:
col_width = 5
col_height = 6
col_linx =  np.around(np.arange(0, col_width, 0.01), decimals=2)
col_liny = np.around(np.arange(-col_height/2, col_height/2, 0.01), decimals=2)

# create a matrix to be transformed and transform it (Visual to SC):
X,Y = np.meshgrid(ret_linx, ret_liny)
Xc, Yc = 7.5, 3.5
Sx = 10.0
Sy = 2.5
VisualMap = gaussianBump(X,Y,Xc,Yc, 1, Sx, Sy)
SCMap = transfCartToCol2(VisualMap, ret_linx, ret_liny, col_linx, col_liny)

# ------------------
# Do the figure:
# ------------------
fig = plt.figure(figsize= (16,12), dpi=80)
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

if PLOT_GRID: # plot the grid
    toTrace = ( np.arange(0,91,5), np.arange(-90,100, 15) )
    gridSC = constructSCGrid(*toTrace)
    gridRet = constructRetinalGrid(*toTrace)
    plotGrid(gridRet, ax1, color1, color2)
    plotGrid(gridSC, ax2,  color1, color2)

ax1.imshow(VisualMap, cmap= cmap, interpolation = "nearest", extent=[0,60,-60,60])#vmin=np.min(Th), vmax = np.max(Th))
axes = ax1.get_axes()
axes.grid(True)

ax2.imshow(SCMap,cmap= cmap, interpolation = "nearest", extent=[0,5,-3,3])
axes = ax2.get_axes()
axes.grid(True)

# change the size of the axis' text's font:
plt.axis('scaled')
ax2.axis((0.,5.0,-3.,3.))
for tick in ax1.xaxis.get_major_ticks() + ax1.yaxis.get_major_ticks():
    tick.label.set_fontsize(16)
for tick in ax2.xaxis.get_major_ticks() + ax2.yaxis.get_major_ticks():
    tick.label.set_fontsize(16)
plt.savefig("img/toSC-FromMatrix.png")
plt.show()

