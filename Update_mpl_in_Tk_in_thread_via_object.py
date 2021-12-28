"""
Demonstrate how to update a matplotlib graph from inside a thread
"""

__author__ = 'Gero Nootz'
__copyright__ = ''
__credits__ = ['', '']
__license__ = ''
__version__ = '1.0.0'
__date__ = '12/26/2021'
__maintainer__ = 'Gero Nootz'
__email__ = 'gero.noozt@usm.edu'
__status__ = 'Prototype'


import tkinter as tk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib import pyplot as plt, animation
import numpy as np
import queue
import threading
import time
import logging
from enum import Enum, auto
from abc import ABC, abstractmethod

plt.rcParams["figure.figsize"] = [7.00, 3.50]
# plt.rcParams["figure.autolayout"] = True
# plt.rcParams['lines.linestyle'] = '--'


class Add_del_art(Enum):
    add = auto()
    delete = auto()


class Artist(ABC):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

        logging.debug('__init__ created objecyt with ID: %i', id(self)) 
        self.add_or_del_artist = Add_del_art.add
        self.artist_exsits = False
        self.art_data = np.array([], dtype=float).reshape(0, 2) # prepare (N,2) array

        q_art.put(self)
        while self.artist_exsits == False:
            logging.debug('no artist created yet for object %i', id(self))
            time.sleep(1)
        logging.info('artist for object %i created', id(self))

    def __del__(self):  
        logging.warning('deleting of artists via class Artists is unreliable')      
        self.add_or_del_artist = Add_del_art.delete
        logging.debug('!!!!!!!!!!!!!!!Placing object %i in queue to be deleted!!!!!!!!!!', id(self))
        q_art.put(self)
        while self.artist_exsits == True:
            logging.debug('artist of object %i not deleted yet', id(self))
            time.sleep(1)
        logging.info('artist of object %i deleted', id(self))
 
    @abstractmethod
    def create_artist(self, ax: plt.axes):
        pass

    @abstractmethod
    def add_data_to_artist(self,new_data):
        pass

    @abstractmethod
    def clear_data(self):
        pass

    def set_artist_exsits(self, artist_exsits):
        self.artist_exsits = artist_exsits

class ImageArtist(Artist):
    def create_artist(self, ax: plt.axes):
        logging.debug('Object %i recived ax with ID: %i', id(self), id(ax))
        self.artist = ax.scatter([], [], animated=True, **self.kwargs)
        return self.artist

    def add_data_to_artist(self,new_data):
        # logging.debug('adding dat to artist %i', id(self.artist))
        self.art_data = np.vstack([self.art_data, [[new_data[0], new_data[1]]]])
        self.artist.set_offsets(self.art_data)

    def clear_data(self):
        self.art_data = np.array([], dtype=float).reshape(0, 2) # prepare (N,2) array 
        self.artist.set_offsets(self.art_data)

class ScatterArtist(Artist):
    def create_artist(self, ax: plt.axes):
        logging.debug('Object %i recived ax with ID: %i', id(self), id(ax))
        self.artist = ax.scatter([], [], animated=True, **self.kwargs)
        return self.artist

    def add_data_to_artist(self,new_data):
        # logging.debug('adding dat to artist %i', id(self.artist))
        self.art_data = np.vstack([self.art_data, [[new_data[0], new_data[1]]]])
        self.artist.set_offsets(self.art_data)

    def clear_data(self):
        self.art_data = np.array([], dtype=float).reshape(0, 2) # prepare (N,2) array 
        self.artist.set_offsets(self.art_data)

class LineArtist(Artist):
    def create_artist(self, ax: plt.axes):
        logging.debug('Object %i recived ax with ID: %i', id(self), id(ax))
        self.artist, = ax.plot([], [], animated=True, **self.kwargs)
        return self.artist

    def add_data_to_artist(self,new_data):
        # logging.debug('adding dat to artist %i', id(self.artist))
        self.art_data = np.vstack([self.art_data, [[new_data[0], new_data[1]]]])
        self.artist.set_data(self.art_data[:,0], self.art_data[:,1])

    def clear_data(self):
        self.art_data = np.array([], dtype=float).reshape(0, 2) # prepare (N,2) array 
        self.artist.set_data(self.art_data[:,0], self.art_data[:,1])



def provide_image1(): 
    delay = np.random.rand()*10    
    sleep = np.random.rand() 
 
    
    artist = LineArtist(label='line plot')
    logging.debug('createdg artist %i for provide_line1', id(artist))

    time.sleep(delay)   

    i = 0
    while True:        
        data = np.random.rand(2)    
        new_xy = (data[0]*2, data[1]*2-1) 
        artist.add_data_to_artist(new_xy)
        if i%10 == 0:
            artist.clear_data()
        i += 1
        time.sleep(sleep)

def provide_line1(): 
    delay = np.random.rand()*10    
    sleep = np.random.rand() 
 
    
    artist = LineArtist(label='line plot')
    logging.debug('createdg artist %i for provide_line1', id(artist))

    time.sleep(delay)   

    i = 0
    while True:        
        data = np.random.rand(2)    
        new_xy = (data[0]*2, data[1]*2-1) 
        artist.add_data_to_artist(new_xy)
        if i%10 == 0:
            artist.clear_data()
        i += 1
        time.sleep(sleep)

def provide_scatter1(): 
    delay = np.random.rand()*10    
    sleep = np.random.rand() 
 
    
    scatter_artist = ScatterArtist(s=60, marker='x', label='scatter plot')
    logging.debug('createdg artist %i for provide_scatter1', id(scatter_artist))

    time.sleep(delay)   

    i = 0
    while True:        
        data = np.random.rand(2)    
        new_xy = (data[0]*2, data[1]*2-1) 
        scatter_artist.add_data_to_artist(new_xy)
        if i%10 == 0:
            scatter_artist.clear_data()
        i += 1
        time.sleep(sleep)

def provide_scatter2(): 

    delay = np.random.rand()*10
    sleep = np.random.rand() 

    scatter_artist = ScatterArtist(s=60, marker='o', label='scatter plot')
    logging.debug('createdg artist %i for provide_scatter2', id(scatter_artist))

    time.sleep(delay)
    
    for i in range(10):          
        data = np.random.rand(2)    
        new_xy = (data[0]*2, data[1]*2-1) 
        scatter_artist.add_data_to_artist(new_xy)
        # print(i)
        time.sleep(sleep)

    logging.debug('deleting artist of object %i from provide_scatter2', id(scatter_artist))    
    # del scatter_artist
    # if not 'scatter_artist' in locals():
    #     logging.debug('deleted artist from provide_scatter2')
    # else:
    #     logging.error('artist from provide_scatter2 was NOT deleted, why?')
       
    q_art.join()

def provide_scatter3():    
    scatter_artist = ScatterArtist(s=60, marker='o', label='scatter plot')
    logging.debug('createdg artist %i for provide_scatter2', id(scatter_artist))
    i = 1
    while True:        
        if i < 10:
            data = np.random.rand(2)    
            new_xy = (data[0]*2, data[1]*2-1) 
            scatter_artist.add_data_to_artist(new_xy)
            i += 1
        if i == 10:
            logging.debug('deleting artist of object %i from provide_scatter3', id(scatter_artist))
            del scatter_artist
            i += 1
        time.sleep(1)
     
def artist_manager(ax: plt.axes) -> list:
    """
    Collects new artists from a queue into a list of artists
    to be animated in matplotlib.animation.FuncAnimation
    -> returns a list of artists
    """
    artists = []
    artist_ids: int = []
    i: int = 0

    while True:
        try:
            object = q_art.get(False)
        except queue.Empty:
            pass
        else:            
            logging.debug('artist_manager recived object ID: %i', id(object)) 

            if object.add_or_del_artist == Add_del_art.add:
                logging.debug('adding artist')
                artist = object.create_artist(ax)

                artist_ids.append(id(object))
                artists.append(artist)
                logging.debug('Number of artists: %i', len(artists)) 

                logging.debug(artist_ids)
                logging.debug(artists)

                object.set_artist_exsits(True)

            elif object.add_or_del_artist == Add_del_art.delete:
                logging.debug('deleting artist of object ID: %i', id(object)) 

                index =  artist_ids.index(id(object))
                logging.debug('deleting artist form index %i', index)

                del artist_ids[index]
                del artists[index]

                logging.debug(artist_ids)
                logging.debug(artists)

                object.set_artist_exsits(False)
                logging.debug('Number of artists: %i', len(artists)) 
        
            else:
                logging.error('not of enum type Add_del_art')

            q_art.task_done()
        i += 1
        if i%100 == 0:
            logging.info('artist_manager is running i=%i', i)
            logging.info('Number of threads: %i', threading.active_count())

        yield artists

def init():
    ax.set_xlabel('x-data')
    ax.set_ylabel('y-data')
    return []

def animate(artists) -> list:
    """
    Receives a list of artists to be animated in matplotlib.animation.FuncAnimation
    -> returns a list of artists
    """
    return artists


if __name__ == '__main__':

    logging.basicConfig(level=logging.WARNING) # print to console
    # logging.basicConfig(filename='main.log', encoding='utf-8', level=logging.DEBUG) # append to file
    # logging.basicConfig(filename='example.log', filemode='w', level=logging.INFO) # overide file each run

    q_art = queue.Queue(maxsize=0)  

    root = tk.Tk()
    root.wm_title("Update mpl in Tk via queue")

    fig = plt.Figure(dpi=200)
    ax = fig.add_subplot(xlim=(0, 2), ylim=(-1.1, 1.1))
    logging.debug('Created ax with ID: %i', id(ax)) 

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    button = tk.Button(master=root, text="Quit", command=root.quit)
    button.pack(side=tk.BOTTOM)

    toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
    toolbar.update()
    toolbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    threading.Thread(target = provide_line1, daemon = True).start()        
    threading.Thread(target = provide_line1, daemon = True).start()        
    threading.Thread(target = provide_line1, daemon = True).start()        
    threading.Thread(target = provide_line1, daemon = True).start()        
    threading.Thread(target = provide_line1, daemon = True).start()        
    threading.Thread(target = provide_scatter1, daemon = True).start()        
    threading.Thread(target = provide_scatter1, daemon = True).start()        
    threading.Thread(target = provide_scatter1, daemon = True).start()        
    threading.Thread(target = provide_scatter1, daemon = True).start()        
    threading.Thread(target = provide_scatter1, daemon = True).start()        
    threading.Thread(target = provide_scatter2, daemon = True).start()        
    threading.Thread(target = provide_scatter1, daemon = True).start()        
    threading.Thread(target = provide_scatter1, daemon = True).start()        
    threading.Thread(target = provide_scatter1, daemon = True).start()        
    threading.Thread(target = provide_scatter1, daemon = True).start()        
    threading.Thread(target = provide_scatter1, daemon = True).start()        
      

    anim = animation.FuncAnimation(fig, animate, frames=artist_manager(ax), init_func=init, 
                                                         interval=20, blit=True)
    logging.debug('Number of threads: %i', threading.active_count())

    tk.mainloop()