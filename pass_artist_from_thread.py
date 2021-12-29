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
from abc import ABC, abstractmethod


class plot_request(ABC):
    """Base class for plot request via Artist queue"""
    
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.new_xy = ([],[])
        self.xy_data = np.array([], dtype=float).reshape(0, 2) # prepare (N,2) array
        self.ax = None
    
    @abstractmethod
    def create_artist(self):   
        # needs to generate self.artist  
        pass

    @abstractmethod
    def update_artist(self):
        # update data of self.artist
        pass
 
    def plot(self, ax):
        if self.ax is None:
            self.ax = ax            
            self.create_artist()
            new_artist = True
        else:
            new_artist = False
            
        self.xy_data = np.vstack([self.xy_data, [[self.new_xy[0], self.new_xy[1]]]])
        self.update_artist()
        return {'artist': self.artist, 'newArtist': new_artist}

class LineArtist(plot_request):
    """Printing data as line plot"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_artist(self): 
        self.artist, = self.ax.plot([], [], label='line plot', animated=True, **self.kwargs)
       

    def update_artist(self):        
        self.artist.set_data(self.xy_data[:,0], self.xy_data[:,1]) 


class ScatterArtist(plot_request):
    """Printing data as scatter plot"""
    def create_artist(self):            
        self.artist = self.ax.scatter([], [], s=60, label='scatter plot', animated=True)
        

    def update_artist(self):
        self.artist.set_offsets(self.xy_data)
    

def supply_objects(n_iter , delay_s=0):
    for cnt in range(n_iter):
        time.sleep(delay_s)
        if cnt % 2 == 0:
            line_artist.new_xy = (cnt*10/n_iter,cnt*10/n_iter)
            yield line_artist
        else:
            scatter_artist.new_xy = (cnt*10/n_iter,cnt*10/n_iter)
            yield scatter_artist
       

def init_plot():
    """initialize plt, set axis limits"""
    artists = []
    ax.set_ylim(0, 10)
    ax.set_xlim(0, 10)
    return artists


def update_plot(plot_object, ax, artists):
    artist = plot_object.plot(ax)
    if artist["newArtist"]: # add new artist when a not seen before object is received
        artists.append(artist["artist"])
        logging.info('New object detected "%s", numbere of artists: %i',
                                    artist['artist'].get_label(), len(artists))
    return artists
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    artists = []
    line_artist = LineArtist(c='r', marker='o', linestyle='None', linewidth=3, markersize=50, markerfacecolor='None')
    scatter_artist = ScatterArtist()
    line_artist2 = LineArtist(c='r', marker='o', linestyle='None', linewidth=3, markersize=2, markerfacecolor='None')

    fig, ax = plt.subplots()
    ani = FuncAnimation(fig, update_plot, frames=supply_objects(n_iter=10, delay_s=0.0), fargs=(ax, artists),
                    interval=0, init_func=init_plot, blit=True, repeat=False)
    plt.show()