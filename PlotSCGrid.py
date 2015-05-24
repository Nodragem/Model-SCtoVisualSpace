'''
Created on 2 fevr. 2012

@author: Geoffrey Megardon
'''
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from util.SCTransformation import *
from util.util import *

goToFileDir(__file__)

print "Plot a SC grid"
toTrace = ( np.arange(0,91,5), np.arange(-90,100, 15) )
gridSC = constructSCGrid(*toTrace)
gridRet = constructRetinalGrid(*toTrace)
fig = plt.figure(dpi = 200)
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
plotGrid(gridRet, ax1)
plotGrid(gridSC, ax2)

## change the size of the axis font
plt.axis('scaled')
ax2.axis((0.,5.0,-3.,3.))
for tick in ax1.xaxis.get_major_ticks() + ax1.yaxis.get_major_ticks():
    tick.label.set_fontsize(16)
for tick in ax2.xaxis.get_major_ticks() + ax2.yaxis.get_major_ticks():
    tick.label.set_fontsize(16)
plt.savefig("img/SC-grid.png")
plt.show()

