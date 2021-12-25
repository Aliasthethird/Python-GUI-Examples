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
    def init_artist(self):     
        pass

    @abstractmethod
    def update_artist(self):
        pass
 
    def plot(self, ax):
        if self.ax is None:
            self.ax = ax            
            self.init_artist()
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

    def init_artist(self): 
        self.artist, = self.ax.plot([], [], label='line plot', animated=True, **self.kwargs)
       

    def update_artist(self):        
        self.artist.set_data(self.xy_data[:,0], self.xy_data[:,1]) 



def supply_objects(n_iter , delay_s=0):
    for cnt in range(n_iter):
        time.sleep(delay_s)
        if cnt % 2 == 0:
            line_artist.new_xy = (cnt*10/n_iter,cnt*10/n_iter)
            yield line_artist

       

def init_plot():
    """initialize plt, set axis limits"""
    artists = []
    ax.set_ylim(0, 10)
    ax.set_xlim(0, 10)
    return artists


def update_plot(artist):
    if artist is not None:
        artists.append(artist)
        logging.info('New object detected "%s", numbere of artists: %i',
                                    artist.get_label(), len(artists))
    return artists


def supply_artists(n_iter, delay_s, ax):
    artist1, = ax.plot([], [], marker='o', animated=True, linestyle='None', label='artist1')
    print(type(artist1))
    yield artist1
    artist2, = ax.plot([], [], marker='x', animated=True, linestyle='None', label='artist2')
    yield artist2
    xs = np.array([], dtype=float)
    ys = np.array([], dtype=float)
    for i in range(n_iter):
        time.sleep(delay_s)
        x, y = 10*i/n_iter, 10*i/n_iter
        xs = np.append(xs, x)
        ys = np.append(ys, x)
        artist1.set_data([xs], [ys])
        artist2.set_data([xs], [ys+1])
        yield None



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    artists = []
     
    fig, ax = plt.subplots()
    artist, = ax.plot([], [], label='line plot', animated=True)
    ani = FuncAnimation(fig, update_plot, frames=supply_artists(n_iter=10, delay_s=0, ax=ax),
                    interval=0, init_func=init_plot, blit=True, repeat=False)
    plt.show()