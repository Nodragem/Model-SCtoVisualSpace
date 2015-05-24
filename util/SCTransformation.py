'''
Created on 2 fevr. 2012

@author: Geoffrey Megardon
'''
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
import time

def openImg(path): # picture to matrix
    Img = Image.open(str(path))
    Img1 = ImageOps.grayscale(Img)
    largeur,hauteur = Img1.size
    imdata=Img1.getdata()
    tab=np.array(imdata)
    matrix = np.reshape(tab,(hauteur,largeur))
    return matrix

def gaussianBump(X,Y,Xc,Yc, A, se1, se2): ## return a matrix featuring a 2d Gaussian curve 
    A = 1
    M = A*np.exp(-(  ((X-Xc)**2)/(2*se1**2) + ((Y-Yc)**2)/(2*se2**2) ) )
    return(M)    
    
def r(x,y):
    return (np.sqrt(x**2+y**2))

def phi(x,y):
    return ( 2*np.arctan2(y,(x + np.sqrt(x**2+y**2))) )

def x(r, phi):
    return (r*np.cos(phi))

def y(r, phi):
    return (r*np.sin(phi))

def uColi(r, phi):
    return( 1.4* np.log(np.sqrt(r**2+2*3.0*r*np.cos(phi) + 3.0**2)/3.0) )

def vColi(r,phi):
    return( 1.8*np.arctan2((r*np.sin(phi)),(r*np.cos(phi)+3.0))  )

def rColi(u,v):
    return( 3.0*np.sqrt( np.exp(2*u/1.4) - 2*np.exp(u/1.4)*np.cos(v/1.8) + 1 ) )

def phiColi(u,v):
    return( np.arctan2( (np.exp(u/1.4)*np.sin(v/1.8)), ( np.exp(u/1.4)*np.cos(v/1.8)-1) ) )
    #return( np.arctan( (np.exp(u/1.4)*np.sin(v/1.8)) / ( np.exp(u/1.4)*np.cos(v/1.8)-1) ) )

def toColi(x,y):
    re, phie = r(x,y), phi(x,y)
    if(type(x) != np.ndarray):
        return(  ( uColi(re,phie), vColi(re,phie) )  )
    else:
        if len(x.shape)>1 or len(y.shape)>1:

            result = np.zeros((np.shape(x)[0], np.shape(x)[1],2))
            result[:,:,0] = uColi(re,phie)
            result[:,:,1] = vColi(re,phie)
        else:
            result = np.zeros((np.shape(x)[0], 1,2))
            #print result.shape, result[:,:,0].shape, np.matrix(uColi(re,phie)).shape
            result[:,:,0] = uColi(re,phie).reshape(np.shape(x)[0],1)
            result[:,:,1] = vColi(re,phie).reshape(np.shape(x)[0],1)
        return(result)


def fromColi(u,v):
    r, phi = rColi(u,v), phiColi(u,v)
    #print np.shape(r), np.shape(phi), np.max(r), np.max(phi)
    #print type(u)
    if (type(u) != float and type(u) != int):
        result = np.zeros((np.shape(u)[0], np.shape(u)[1],2))
        result[:,:,0] = x(r,phi)
        result[:,:,1] = y(r,phi)
        return(result)
    else:
        return (x(r, phi), y(r, phi))

def transfColToCart(m, linx, liny, linu, linv): 
    """ The function return the projection of the picture/matrix m to the Visual Space.
    The way to do can seem tricky:
    The idea is to NOT project pixels of the SC space to the Visual space,
    but to look where project the pixels of the Visual space in the SC space and then pick up the pixel value.
    Look the function transfColToCart for more comments..."""
    print "Transformation in progress..."
    start = time.time()
    lx, ly = len(linx), len(liny)
 
    minu, maxu = linu[0], linu[-1]
    minv, maxv = linv[0], linv[-1]
    du = 1/abs(linu[1]-linu[0])
    
    X, Y = np.meshgrid(linx, liny)
    coord = np.zeros((ly, lx, 2))
    coord[:,:,:] = toColi(X,Y)
    coord[:,:,0] = (np.ceil(du*coord[:,:,0])-1)/du 
    coord[:,:,1] = (np.trunc(du*coord[:,:,1]))/du
    coord[np.isnan(coord)] = 0
    mt = np.zeros((ly, lx))

    for x in xrange(0, lx):
        for y in xrange(0, ly):
            u, v = coord[y,x,0], coord[y, x, 1]

            if ((u > (maxu)) | (u < (minu)) | (v > (maxv)) | (v < (minv)) ):
                mt[y,x] = 0.0
            else:
                ind_u = np.nonzero(linu==u)[0][0]
                ind_v = np.nonzero(linv==v)[0][0]
                mt[y, x] = m[ind_v,ind_u]

    conn_time = time.time()-start
    a = time.gmtime(conn_time)
    print time.strftime("\ntask time for map transformation: %H:%M:%S",a )
    return(mt)

def transfCartToCol2(m, linx, liny, linu, linv):
    """ The function return the projection of the picture/matrix m to the SC:
    The way to do can seem tricky:
    The idea is to NOT project pixels of the Visual space to the SC space,
    but to look where project the pixels of the SC space in the Visual space and then pick up the pixel value"""
    # the matrix m represents the Visual map, it is a discrete Visual map .
    
    start = time.time()
    print "Transformation in progress..."
    lu, lv = len(linu), len(linv)
    print "lu, lv:", lu, lv
    minx, maxx = linx[0], linx[-1]
    miny, maxy = liny[0], liny[-1]
    dx = 1/abs(linx[1]-linx[0])
    #print minx, miny, maxx, maxy
    
    # this the matrix which represents the SC map: It is a discrete SC map.
    SC_map = np.zeros((lv, lu))
    # we create a matrix which give us the coordinates (u,v) of the pixels (i,j) of SC_map:
    # (u,v) are the axis of the SC space. 
    # (i,j) are the lines and columns of the matrix SC_map.
    U, V = np.meshgrid(linu, linv)  # each pixel has a u and a v. Then U and V have the same dimension than SC_map.
    # we create a matrix which will give coordinates (x,y) in the visual space to each pixels of SC_map
    coord = np.zeros((lv, lu, 2))
    coord[:,:,:] = fromColi(U,V) # Each point of the SC grid get coordinates in the Visual space.
    # coord[:,:,0] is the coordinates on x-axis.
    # coord[:,:,1] is the coordinates on y-axis.
    # for now coord is full of float numbers.
    # These coordinates MUST be integer because our Visual Space is define by the matrix m.
    coord[:,:,0] = (np.ceil(dx*coord[:,:,0])-1)/dx # the multiplication by dx is to be able to ceil at the level we want.
    # np.ceil would change -0.8 to -1, or 0.8 to 0: which is useful to keep negative numbers negative 
    coord[:,:,1] = (np.trunc(dx*coord[:,:,1]))/dx
    # transform: -0.8 en 0, et 0.8 en 0: useful to not be upper than maxy
 
    
    # we go in each pixel of the SC map:
    for i in xrange(0, lu):
        for j in xrange(0, lv):
            # we look where project this SC's pixel in the Visual Space:
            x, y = coord[j,i,0], coord[j, i, 1]

            if ((x > (maxx)) | (x < (minx)) | (y > (maxy)) | (y < (miny)) ):
                # if it project outside the Visual Space, it is Not a Number
                SC_map[j,i] = np.nan 
            else:
                # if it projects inside the Visual Space, we pick up the pixel value of its projection
                ind_x = np.nonzero(linx==x)[0][0] 
                ind_y = np.nonzero(liny==y)[0][0]
                SC_map[j, i] = m[ind_y,ind_x]


    conn_time = time.time()-start
    a = time.gmtime(conn_time)
    print time.strftime("\ntask time for map transformation: %H:%M:%S",a )
    return(SC_map)

def constructSCLine(r, phi): # if r is vector -> ligne, if phi is a vector -> cercle
    x1, y1 = x(r,phi), y(r,phi)
    #print toColi(x1,y1)[:,:,0]
    return(toColi(x1,y1)[:,:,0], toColi(x1,y1)[:,:,1])
    
def xy(r, phi):
    return x(r,phi), y(r,phi)
    
def constructRetinalGrid(r_list, phi_list):
    lines_r = []
    for r in r_list:
        lines_r.append(xy(r, np.radians(np.arange(-90,90,0.1))))
    lines_phi = []
    for phi in phi_list:
        lines_phi.append(xy(np.arange(0,90,0.1), np.radians(phi)))
    return(lines_r, lines_phi)
    
def constructSCLineFromCartesian(x, y):
    return(toColi(x,y)[:,:,0], toColi(x,y)[:,:,1])

def createCircle(xc, yc, r):
    x = np.arange(xc-r,xc+r,0.01)
    root = np.sqrt(r**2 - (x-xc)**2)
    y1 = root + yc
    y2 = - root + yc
    return np.tile(x,2), np.concatenate((y1,y2), axis=0)

def createRectangle(left, down, right, up):
    edge1 = np.arange(down, up, 0.1)
    y1 = np.tile(edge1,2) 
    x1 = np.concatenate( (np.repeat(left, len(edge1)), np.repeat(right, len(edge1)) ) ) 
    edge2 = np.arange(left, right, 0.1)
    x2 = np.tile(edge2,2)
    y2 =  np.concatenate( (np.repeat(up, len(edge2)), np.repeat(down, len(edge2)) ), axis=0 ) 
    #print x1, x2, y1, y2
    #print np.concatenate((x1,x2), axis =0), np.concatenate((y1,y2), axis =0)
    #return x2, y2
    return np.concatenate((x1,x2), axis =0), np.concatenate((y1,y2), axis =0)
    
def constructSCGrid(r_list, phi_list):
    lines_r = []
    for r in r_list:
        lines_r.append(constructSCLine(r, np.radians(np.arange(-90,90,0.1))))

    lines_phi = []
    for phi in phi_list:
        lines_phi.append(constructSCLine(np.arange(0,90,0.1), np.radians(phi)))

    return(lines_r, lines_phi)

def plotGrid(grid, ax, color1 = "black", color2 = "gray"):
    lines_r = grid[0]
    lines_phi = grid[1]
    for i in np.arange(0, np.shape(lines_r)[0]):
        ax.plot(lines_r[i][0], lines_r[i][1], color = color2)
    for i in np.arange(0, np.shape(lines_phi)[0]):
        ax.plot(lines_phi[i][0], lines_phi[i][1], color = color1)

