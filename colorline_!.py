# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 13:33:41 2016

@author: OldzieMa
Added more inforoatoi about the project 
evem more information
"""

#import matplotlib.pyplot as plt
#import numpy as np
#import matplotlib.collections as mcoll
#import matplotlib.path as mpath
#from time import sleep
#import numpy as np
#
#
#
#def colorline(
#    x, y, z=None, cmap=plt.get_cmap('copper'), norm=plt.Normalize(0.0, 1.0),
#        linewidth=3, alpha=1.0):
#    """
#    http://nbviewer.ipython.org/github/dpsanders/matplotlib-examples/blob/master/colorline.ipynb
#    http://matplotlib.org/examples/pylab_examples/multicolored_line.html
#    Plot a colored line with coordinates x and y
#    Optionally specify colors in the array z
#    Optionally specify a colormap, a norm function and a line width
#    """
#
#    # Default colors equally spaced on [0,1]:
#    if z is None:
#        z = np.linspace(0.0, 1.0, len(x))
#
#    # Special case if a single number:
#    if not hasattr(z, "__iter__"):  # to check for numerical input -- this is a hack
#        z = np.array([z])
#
#    z = np.asarray(z)
#
#    segments = make_segments(x, y)
#    lc = mcoll.LineCollection(segments, array=z, cmap=cmap, norm=norm,
#                              linewidth=linewidth, alpha=alpha)
#
#    ax = plt.gca()
#    ax.add_collection(lc)
#
#    return lc
#
#def make_segments(x, y):
#    """
#    Create list of line segments from x and y coordinates, in the correct format
#    for LineCollection: an array of the form numlines x (points per line) x 2 (x
#    and y) array
#    """
#
#    points = np.array([x, y]).T.reshape(-1, 1, 2)
#    segments = np.concatenate([points[:-1], points[1:]], axis=1)
#    return segments
#
##N = 10
##np.random.seed(101)
##x = np.random.rand(N)
##y = np.random.rand(N)
##fig, ax = plt.subplots()
## This is just comment
##path = mpath.Path(np.column_stack([x, y]))
##verts = path.interpolated(steps=3).vertices
##x, y = verts[:, 0], verts[:, 1]
##z = np.linspace(0, 1, len(x))
##colorline(x, y, z, cmap=plt.get_cmap('jet'), linewidth=2)
#
#
## Setup
#x = np.linspace(0,4*np.pi,1000)
#y = np.sin(x)
#MAP = 'cubehelix'
#NPOINTS = len(x)
#
#fig = plt.figure()
#ax1 = fig.add_subplot(111) # regular resolution color map
#for i in range(10):
#    colorline(x,y,cmap='cubehelix', linewidth=1)
#    
#    
import numpy as np
import matplotlib.pyplot as plt

x = np.arange(700)
y = np.sin(x/300.0)
#y = x
t = x
plt.scatter(x, y, s=5, c=t, marker="+")
plt.grid()
plt.show()