'''
Created on 3 Sep 2013

@author: c1248317
'''
'''
Created on 2 fevr. 2012

@author: Geoffrey
'''
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.cm as cm
from util.SCTransformation import *
from util.util import *
  
goToFileDir(__file__)  

print "Boch et al. 1986"
toTrace = ( np.arange(0,91,5), np.arange(-90,100, 30) )
gridSC = constructSCGrid(*toTrace)
gridRet = constructRetinalGrid(*toTrace)
fig = plt.figure(dpi = 200)
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
#ax = plt.gca()
plotGrid(gridRet, ax1)
plotGrid(gridSC, ax2)
g= constructSCLineFromCartesian
list_Cu, list_Cv = [],[]
list_Cx, list_Cy = [], []
## Boch et al. sizes:
list_size = (0.258, 0.599, 0.847, 1.388)
## control condition:
list_size = (1.388, 1.388, 1.388, 1.388)
list_ecc = (1.0, 2.0, 4.0, 8.0)
list_col = []
for ecc, size in zip(list_ecc, list_size):
    #Cx, Cy = createCircle(ecc, 0, size)
    Cx, Cy = createRectangle(ecc-size/2., 0-size/2., ecc+size/2., 0+size/2)
    col = np.repeat(ecc, len(Cx))
    Cu, Cv = g(Cx,Cy)
    list_Cu.append(Cu); list_Cv.append(Cv)
    list_Cx.append(Cx); list_Cy.append(Cy)
    list_col.append(col)
    

list_Cv = np.concatenate(list_Cv, axis=0)
list_Cu = np.concatenate(list_Cu, axis=0)
list_Cx = np.concatenate(list_Cx, axis=0)
list_Cy = np.concatenate(list_Cy, axis=0)
list_col = np.concatenate(list_col, axis=0)
list_col = list_col/np.amax(list_col)

ax1.scatter( list_Cx, list_Cy, marker='o', 
s=20, linewidths=0, c=list_col.tolist(), cmap=plt.cm.coolwarm)
ax1.axis((0.,10.,-10.,10.))
ax2.scatter( list_Cu, list_Cv, marker='o', 
s=20, linewidths=0, c=list_col.tolist(), cmap=plt.cm.coolwarm)

# model_area = plt.Rectangle((0.14613, -1.83333), 100*11/300., 100*11/300., fc='cyan')
# ax.add_patch(model_area)
plt.axis('scaled')
ax2.axis((0.,2.5,-3.,3.))
for tick in ax1.xaxis.get_major_ticks() + ax1.yaxis.get_major_ticks():
    tick.label.set_fontsize(16) 
for tick in ax2.xaxis.get_major_ticks() + ax2.yaxis.get_major_ticks():
    tick.label.set_fontsize(16) 
plt.savefig("img/Boch-control.png")
plt.show()

