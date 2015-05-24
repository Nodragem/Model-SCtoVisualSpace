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

for pos_ciblex in (60, 75):
    for size_barre in (4, 8, 20, 40):
        VisualMap = np.ones((ret_height*10, ret_width*10))
        pos_barrex = pos_ciblex - 30 
        VisualMap[600-size_barre/2:600+size_barre/2, pos_barrex:pos_barrex+1] = 0
        
        SCMap = transfCartToCol2(VisualMap, ret_linx, ret_liny, col_linx, col_liny)
        SCMap_zoom=SCMap[190:410, 40:260]*250
        buffer = Image.new("L",(SCMap_zoom.shape[1],SCMap_zoom.shape[0]))
        buffer.putdata(list(SCMap_zoom.flat))
        name = "img/tandonnet/cond" + str(pos_ciblex) +"-" + str(size_barre) +".png"
        buffer.save(name, format="png") 
        
        buffer = buffer.resize((60,60), Image.ANTIALIAS)
        SCMap_zoom_resized = np.reshape(np.array(buffer.getdata()),(60,60))
        filtre = 180
        SCMap_zoom_resized[SCMap_zoom_resized<filtre] = 0
        SCMap_zoom_resized[SCMap_zoom_resized>=filtre] = 250 
        buffer = Image.new("L",(SCMap_zoom_resized.shape[1],SCMap_zoom_resized.shape[0]))
        buffer.putdata(list(SCMap_zoom_resized.flat))
        name = "img/tandonnet/resizecond" + str(pos_ciblex) +"-" + str(size_barre) + ".png"
        buffer.save(name, format = "png")
#map3 = SCMap

plt.figure(figsize= (16,12), dpi=80)

plt.subplot(221)
imgaxes = plt.imshow(VisualMap[ 600-30:600+30, 0:100], cmap= cm.gray, interpolation = "nearest", extent=[0,10,-3,3])#vmin=np.min(Th), vmax = np.max(Th))
axes = imgaxes.get_axes()
axes.grid(True)

plt.subplot(222)
cmap = cm.gray
cmap.set_bad('k',1.)
imgaxes = plt.imshow(SCMap.transpose(),cmap=cmap, interpolation = "nearest", extent=[-3,3,5,0])
axes = imgaxes.get_axes()
axes.grid(True)

plt.subplot(223)
imgaxes = plt.imshow(SCMap_zoom, cmap= cm.gray, interpolation = "nearest", extent=[0.4,2.6,-1.1,1.1])#, extent=[0,60,-60,60])#vmin=np.min(Th), vmax = np.max(Th))
axes = imgaxes.get_axes()
axes.grid(True) 

plt.subplot(224)
imgaxes = plt.imshow(SCMap_zoom_resized, cmap= cm.gray, interpolation = "nearest")#, extent=[0,60,-60,60])#vmin=np.min(Th), vmax = np.max(Th))
axes = imgaxes.get_axes()
axes.grid(True)

plt.show()



