"""
Demonstrate how to update a matplotlib graph from inside a thread
"""

import tkinter as tk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib import (pyplot as plt, animation)
from matplotlib.backend_bases import key_press_handler
import queue
import threading
import time
import logging
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
        time.sleep(5)
        iver_art = ta.ImageArtist(q_art, label='iver animation', alpha=1, zorder=4)
        trace_art = ta.LineArtist(q_art, label='iver trace', c='r', alpha=0.6, zorder=3)
        icon_size = 0.015
        iver_art.add_data_to_artist('Iver_icon_small.png', icon_size, (0, 0), 0)
        x_range = iver_art.ax.get_xlim()[1] - iver_art.ax.get_xlim()[0]
        y_range = iver_art.ax.get_ylim()[1] - iver_art.ax.get_ylim()[0]
        i = 0
        while True: 
            x_pos = iver_art.ax.get_xlim()[0] + i * x_range
            y_pos = (iver_art.ax.get_ylim()[0]+(y_range/2)) + 0.9*0.5*y_range*math.sin(
                2*(math.pi/x_range)*(x_pos-iver_art.ax.get_xlim()[0]))
            new_xy = (x_pos, y_pos)
            deg = 65 * (math.cos(2*(math.pi/x_range)*(x_pos-iver_art.ax.get_xlim()[0]))-90)
            iver_art.set_position(new_xy, deg)
            trace_art.add_data_to_artist(new_xy)
            i += 0.01
            if (x_pos-iver_art.ax.get_xlim()[0]) > x_range:
                trace_art.clear_data()
                i = 0
            time.sleep(1)

def animate_wamv(): 
        time.sleep(3)
        iver_art = ta.ImageArtist(q_art, label='wam-v animation', alpha=1, zorder=4)
        trace_art = ta.LineArtist(q_art, label='vam-v trace', c='g', alpha=0.6, zorder=3)
        icon_size = 0.02
        iver_art.add_data_to_artist('WAM-V_icon_small.png', icon_size, (0, 0), 0)
        x_range = iver_art.ax.get_xlim()[1] - iver_art.ax.get_xlim()[0]
        y_range = iver_art.ax.get_ylim()[1] - iver_art.ax.get_ylim()[0]
        i = 0
        while True: 
            x_pos = iver_art.ax.get_xlim()[0] + i * x_range
            y_pos = (iver_art.ax.get_ylim()[0]+(y_range/2)) + 0.9*0.5*y_range*math.sin(
                2*(math.pi/x_range)*(x_pos-iver_art.ax.get_xlim()[0]))
            new_xy = (x_pos, y_pos)
            deg = 65 * (math.cos(2*(math.pi/x_range)*(x_pos-iver_art.ax.get_xlim()[0]))-90)
            iver_art.set_position(new_xy, deg)
            trace_art.add_data_to_artist(new_xy)
            i += 0.01
            if (x_pos-iver_art.ax.get_xlim()[0]) > x_range:
                trace_art.clear_data()
                i = 0
            time.sleep(1)

def plot_geotif(): 
        """Work in progress..."""
        noaachart = ta.GeoTifArtist(q_art, label='Cat Island ENC', alpha=0.6, zorder=1)
        noaachart.add_data_to_artist('Cat_Island_ENC.tif')
        noaachart.set_xlim(noaachart.geotif_xlim[0], noaachart.geotif_xlim[1])
        noaachart.set_ylim(noaachart.geotif_ylim[0], noaachart.geotif_ylim[1])

        goolemap = ta.GeoTifArtist(q_art, label='GeoTif plot', zorder=-1, alpha=1)
        goolemap.add_data_to_artist('Cat_Island_Low_2.tif')
        goolemap.set_xlim(goolemap.geotif_xlim[0], goolemap.geotif_xlim[1])
        goolemap.set_ylim(goolemap.geotif_ylim[0], goolemap.geotif_ylim[1])
        while True: 
            time.sleep(2)

def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                        # Fatal Python Error: PyEval_RestoreThread: NULL tstate

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO) # print to console
    # logging.basicConfig(filename='main.log', encoding='utf-8', level=logging.DEBUG) # append to file
    # logging.basicConfig(filename='example.log', filemode='w', level=logging.INFO) # overide file each run

    q_art = queue.Queue(maxsize=0)  

    root = tk.Tk()
    root.wm_title("Update mpl in Tk via queue")
    fig = plt.Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)

    # ax.set_aspect('equal')
    # ax.margins(2,2) 
    # plt.axis('scaled')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    button = tk.Button(master=root, text="Quit", command=_quit)
    button.pack(side=tk.BOTTOM)

   
    # threading.Thread(target=rand_coordints, daemon = True).start() 
    # threading.Thread(target=rand_coordints_temp, daemon = True).start() 
    threading.Thread(target=plot_geotif, daemon = True).start() 
    # threading.Thread(target=plot_image, daemon = True).start() 
    threading.Thread(target=animate_iver, daemon = True).start() 
    threading.Thread(target=animate_wamv, daemon = True).start() 
    
    anim = animation.FuncAnimation(fig, ta.animate, frames=ta.gallerist(ax, fig, q_art),
             interval=1000 , blit=True, repeat=False)

    tk.mainloop()