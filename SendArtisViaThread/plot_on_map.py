"""
Demonstrate how to update a matplotlib graph from inside a thread
"""

import tkinter as tk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib import pyplot as plt, animation
import numpy as np
import queue
import threading
import time
import logging
import rasterio
from rasterio.plot import show
import random
# my libs
import threadartists as ta

__author__ = 'Gero Nootz'
__copyright__ = ''
__credits__ = ['', '']
__license__ = ''
__version__ = '1.0.0'
__date__ = '12/26/2021'
__maintainer__ = 'Gero Nootz'
__email__ = 'gero.noozt@usm.edu'
__status__ = 'Prototype'


def rand_coordints():
    scatter_artist = ta.ScatterArtist(q_art, s=50, label='scatter plot')
    while True:
        new_xy = (-89.63056 + (random.random()-0.5)*0.01, 30.35275 + (random.random()-0.5)*0.01)
        scatter_artist.add_data_to_artist(new_xy)
        time.sleep(0.1)

def rand_coordints_temp():
    scatter_artist = ta.ScatterArtist(q_art, s=50, label='scatter plot')
    for i in range(100):
        new_xy = (-89.63056 + (random.random()-0.5)*0.01, 30.35275 + (random.random()-0.5)*0.01)
        scatter_artist.add_data_to_artist(new_xy)
        time.sleep(0.1)
    print('done')

def init():
    im =show(rasterio.open('stennis_QW.tif'), ax=ax)
    return []

if __name__ == '__main__':

    logging.basicConfig(level=logging.WARNING) # print to console
    # logging.basicConfig(filename='main.log', encoding='utf-8', level=logging.DEBUG) # append to file
    # logging.basicConfig(filename='example.log', filemode='w', level=logging.INFO) # overide file each run

    q_art = queue.Queue(maxsize=0)  

    root = tk.Tk()
    root.wm_title("Update mpl in Tk via queue")

    fig = plt.Figure(figsize=(9.1, 6))
    ax = fig.add_subplot()
    # ax.get_xaxis().set_visible(False)
    # ax.get_yaxis().set_visible(False)
    # ax.axis('off')
    ax.axis('equal')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    button = tk.Button(master=root, text="Quit", command=root.quit)
    button.pack(side=tk.BOTTOM)

    toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
    toolbar.update()
    toolbar.pack(side=tk.BOTTOM, fill=tk.X)


    # threading.Thread(target=rand_coordints, daemon = True).start() 
    # threading.Thread(target=rand_coordints, daemon = True).start() 
    # threading.Thread(target=rand_coordints, daemon = True).start() 
    # threading.Thread(target=rand_coordints, daemon = True).start() 
    threading.Thread(target=rand_coordints_temp, daemon = True).start() 
    threading.Thread(target=rand_coordints_temp, daemon = True).start() 
    threading.Thread(target=rand_coordints_temp, daemon = True).start() 
    threading.Thread(target=rand_coordints_temp, daemon = True).start() 
    threading.Thread(target=rand_coordints_temp, daemon = True).start() 
    threading.Thread(target=rand_coordints_temp, daemon = True).start() 
    threading.Thread(target=rand_coordints_temp, daemon = True).start() 
    threading.Thread(target=rand_coordints_temp, daemon = True).start() 
    threading.Thread(target=rand_coordints_temp, daemon = True).start() 


    anim = animation.FuncAnimation(fig, ta.animate, frames=ta.artist_manager(ax, q_art),
             init_func=init, interval=50, blit=True, repeat=True)

    logging.debug('Number of threads: %i', threading.active_count())

    tk.mainloop()


















