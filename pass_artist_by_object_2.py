"""
Demonstrates how to pass class methods to generate new artists.

Only creates new artists if a new object is in the queue that has
not been send befor -> the plot does not slow down over time!
"""

__author__ = 'Gero Nootz'
__version__ = '1.0.0'
__email__ = 'gero.noozt@usm.edu'
__status__ = 'Prototype'
# https://www.python.org/dev/peps/pep-0008/#module-level-dunder-names

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import logging
import time
from abc import ABC, abstractmethod # will use later

logging.basicConfig(level=logging.INFO)
 
fig, ax = plt.subplots()

class class1(object):
    """Printing data as line plot"""
    def __init__(self):
        self.new_xy = ([],[])
        self.ax = None


    def init_artist(self):            
            xy_data = np.array([], dtype=float).reshape(0, 2) # prepare (N,2) array
            artist, = self.ax.plot([], [], marker='None', linestyle='-',
                                            label='line plot', c='r')
            return xy_data, artist

    def update_artist(self):
        self.xy_data = np.vstack([self.xy_data, [[self.new_xy[0], self.new_xy[1]]]])
        self.artist.set_data(self.xy_data[:,0], self.xy_data[:,1])
 
    def plot(self, ax):
        if self.ax is None:
            self.ax = ax
            self.xy_data, self.artist = self.init_artist()
            new_artist = True
        else:
            new_artist = False

        self.update_artist()
        return {'artist': self.artist, 'newArtist': new_artist}

class class2(object):
    """Printing data as scatter plot"""
    def __init__(self):
        self.new_xy = ([],[])
        self.ax = None

    def init_artist(self):            
            xy_data = np.array([], dtype=float).reshape(0, 2) # prepare (N,2) array
            artist = self.ax.scatter([], [], s=60, label='scatter plot')
            return xy_data, artist

    def update_artist(self):
        self.xy_data = np.vstack([self.xy_data, [[self.new_xy[0], self.new_xy[1]]]]) 
        self.artist.set_offsets(self.xy_data)
    

 
    def plot(self, ax):
        if self.ax is None: # get axis and generate artist the first time the plot method is called
            self.ax = ax
            self.xy_data, self.artist = self.init_artist()
            new_artist = True
        else:
            new_artist = False

        self.update_artist()
        return {'artist': self.artist, 'newArtist': new_artist}

o1 = class1()
o2 = class2()

def supply_objects(n , delay_s=0):
    for cnt in range(n):
        time.sleep(delay_s)
        if cnt % 2 == 0:
            o1.new_xy = (cnt*10/n,cnt*10/n)
            yield o1
        else:
            o2.new_xy = (cnt*10/n,cnt*10/n)
            yield o2
       

def init_plot():
    ax.set_ylim(0, 10)
    ax.set_xlim(0, 10)
    return artists

artists = []
def update_plot(plot_object, ax):
    artist = plot_object.plot(ax)
    if artist["newArtist"]: # add new artist when a not seen before object is received
        artists.append(artist["artist"])
        logging.info('New object detected "%s", numbere of artists: %i',
                                    artist['artist'].get_label(), len(artists))
    return artists
    

ani = FuncAnimation(fig, update_plot, frames=supply_objects(10, delay_s=0.0), fargs=(ax,),
                interval=0, init_func=init_plot, blit=True, repeat=False)
plt.show()