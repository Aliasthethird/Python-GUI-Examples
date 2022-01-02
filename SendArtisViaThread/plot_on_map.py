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
import rasterio.plot as rioplot
import random
import math

# my libs
import threadartists as ta

__author__ = 'Gero Nootz'
__copyright__ = ''
__credits__ = ['', '']
__license__ = ''
__version__ = '1.0.0'
__date__ = '12/26/2021'
__maintainer__ = 'Gero Nootz'
__email__ = 'gero.nootz@usm.edu'
__status__ = 'Prototype'


def rand_coordints():
    scatter_artist = ta.ScatterArtist(q_art, s=50, label='scatter plot')
    i = 1
    while True:
        new_xy = (-89.63056 + (random.random()-0.5)*0.01, 30.35275 + (random.random()-0.5)*0.01)
        scatter_artist.add_data_to_artist(new_xy)
        if i%100 == 0:
            scatter_artist.clear_data()
        i += 1
        time.sleep(0.1)

def rand_coordints_temp():
    scatter_artist = ta.ScatterArtist(q_art, s=50, label='temp scatter plot')
    for i in range(100):
        new_xy = (-89.63056 + (random.random()-0.5)*0.01, 30.35275 + (random.random()-0.5)*0.01)
        scatter_artist.add_data_to_artist(new_xy)
        time.sleep(0.1)

def plot_image(): 
        artist = ta.ImageArtist(q_art, label='image plot', alpha=1)
        artist.add_data_to_artist('yota.png', 0.05, (-89.63099633995162, 30.348934679652352))
        while True: 
            new_xy = (-89.63056 + (random.random()-0.5)*0.01, 30.35275 + (random.random()-0.5)*0.01)
            artist.set_position(new_xy, 0)
            time.sleep(1)

def animate_iver(): 
        iver_art = ta.ImageArtist(q_art, label='iver animation', alpha=0.6)
        trace_art = ta.LineArtist(q_art, label='iver trace', c='r')

        iver_art.add_data_to_artist('Iver.png', 0.05, (iver_art.ax.get_xlim()[0], 30.348934679652352))
        x_range = iver_art.ax.get_xlim()[1] - iver_art.ax.get_xlim()[0]
        y_range = iver_art.ax.get_ylim()[1] - iver_art.ax.get_ylim()[0]
        i = 0
        while True: 
            x_pos = iver_art.ax.get_xlim()[0] + i * x_range
            y_pos = (iver_art.ax.get_ylim()[0]+(y_range/2)) + 0.9*0.5*y_range*math.sin(
                2*(math.pi/x_range)*(x_pos-iver_art.ax.get_xlim()[0]))
            new_xy = (x_pos, y_pos)
            deg = 65 * math.cos(2*(math.pi/x_range)*(x_pos-iver_art.ax.get_xlim()[0]))
            iver_art.set_position(new_xy, deg)
            trace_art.add_data_to_artist(new_xy)
            i += 0.01
            if (x_pos-iver_art.ax.get_xlim()[0]) > x_range:
                trace_art.clear_data()
                i = 0
            time.sleep(0.3)



def plot_geotif(): 
        """Work in progress..."""
        artist = ta.GeoTifArtist(q_art, label='GeoTif plot')
        artist.add_data_to_artist('Stennis_QW.tif')
        artist.set_xlim(artist.geotif_xlim[0], artist.geotif_xlim[1])
        artist.set_ylim(artist.geotif_ylim[0], artist.geotif_ylim[1])
        while True: 
            time.sleep(2)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO) # print to console
    # logging.basicConfig(filename='main.log', encoding='utf-8', level=logging.DEBUG) # append to file
    # logging.basicConfig(filename='example.log', filemode='w', level=logging.INFO) # overide file each run

    q_art = queue.Queue(maxsize=0)  

    root = tk.Tk()
    root.wm_title("Update mpl in Tk via queue")
    fig = plt.Figure()
    ax = fig.add_subplot()

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    button = tk.Button(master=root, text="Quit", command=root.quit)
    button.pack(side=tk.BOTTOM)

    toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
    toolbar.update()
    toolbar.pack(side=tk.BOTTOM, fill=tk.X)
 
    # threading.Thread(target=rand_coordints, daemon = True).start() 
    # threading.Thread(target=rand_coordints_temp, daemon = True).start() 
    threading.Thread(target=plot_geotif, daemon = True).start() 
    # threading.Thread(target=plot_image, daemon = True).start() 
    threading.Thread(target=animate_iver, daemon = True).start() 
    
    anim = animation.FuncAnimation(fig, ta.animate, frames=ta.artist_manager(ax, fig, q_art),
             init_func=ta.init, interval=300, blit=True, repeat=True)

    tk.mainloop()