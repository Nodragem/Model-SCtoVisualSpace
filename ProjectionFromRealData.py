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

print "Projection of the double stimuli experiment"
toTrace = ( np.arange(0,91,5), np.arange(-90,100, 30) )
gridSC = constructSCGrid(*toTrace)
gridRet = constructRetinalGrid(*toTrace)
fig = plt.figure(dpi = 150)
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
#ax = plt.gca()
plotGrid(gridRet, ax1)
plotGrid(gridSC, ax2)
g= constructSCLineFromCartesian
cm1 = plt.get_cmap("prism")

list_col = []
subject = "BD"
d = np.load("LandingPositions_"+subject+".npy")
print d.shape
target_dir = np.linspace(5.625, 45, 8)
for i, t_dir in enumerate(target_dir):
    Cx, Cy = d[2,i][:,0], d[2,i][:,1]
    Cu, Cv = g(Cx,Cy)
    print i
    ax1.scatter( Cx, Cy, s=20, linewidths=0, c=cm1(i/8.), alpha=0.8)    
    ax2.scatter( Cu, Cv, s=20, linewidths=0, c=cm1(i/8.), alpha=0.8)

# for i, t_dir in enumerate(target_dir):
    # x,y = xy(13.5, np.radians(t_dir))
    # print x, y
    # ax1.scatter( x,y, c="black", s=100, marker="x")
    # u, v = toColi(x,y)
    # ax2.scatter( u,v, c="black", s=100, marker="x")

    
plt.axis('scaled')
ax2.axis((1.,3.5,-3.,3.))
ax1.axis((0.,15.,-15.,15.))
for tick in ax1.xaxis.get_major_ticks() + ax1.yaxis.get_major_ticks():
    tick.label.set_fontsize(16) 
for tick in ax2.xaxis.get_major_ticks() + ax2.yaxis.get_major_ticks():
    tick.label.set_fontsize(16) 
plt.savefig("img/"+subject+"-SC-F80-Tdifferent.png")
plt.show()

