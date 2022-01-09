"""
Demonstrates how to use artgallery to plot on a map
"""

from re import T
import tkinter as tk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib import (pyplot as plt, animation)
from matplotlib.backend_bases import key_press_handler
import threading
import time
import logging
import math
import rasterio
import numpy as np

# my libs
import artgallery as ag

__author__ = 'Gero Nootz'
__copyright__ = ''
__credits__ = ['', '']
__license__ = ''
__version__ = '1.0.0'
__date__ = '12/26/2021'
__maintainer__ = 'Gero Nootz'
__email__ = 'gero.nootz@usm.edu'
__status__ = 'example'


def animate_iver(): 
        time.sleep(6)
        iver_art = ag.ImageArtist(gal, label='iver animation', alpha=1, zorder=4)
        trace_art = ag.LineArtist(gal, label='iver trace', c='r', alpha=0.6, zorder=3)
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
            time.sleep(0.1)

def animate_wamv(): 
        time.sleep(2)
        iver_art = ag.ImageArtist(gal, label='wam-v animation', alpha=1, zorder=4)
        trace_art = ag.LineArtist(gal, label='vam-v trace', c='g', alpha=0.6, zorder=3)
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
            time.sleep(0.1)

def plot_geotif(): 
        """Work in progress..."""
        noaachart = ag.GeoTifArtist(gal, label='Cat Island ENC', zorder=1, alpha=0.6)
        noaachart.add_data_to_artist('Cat_Island_ENC.tif')
        # noaachart.set_xlim(noaachart.geotif_xlim[0], noaachart.geotif_xlim[1])
        # noaachart.set_ylim(noaachart.geotif_ylim[0], noaachart.geotif_ylim[1])

        sat = ag.GeoTifArtist(gal, label='Sat plot', zorder=-1, alpha=1)
        sat.add_data_to_artist('Cat_Island_Low_2.tif')
        sat.set_xlim(sat.geotif_xlim[0], sat.geotif_xlim[1])
        sat.set_ylim(sat.geotif_ylim[0], sat.geotif_ylim[1])
        while True: 
            time.sleep(20)

def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                        # Fatal Python Error: PyEval_RestoreThread: NULL tstate


def holdani(anim):
    while True:
        time.sleep(10)    
        print('animation holted')
        anim.pause()
        time.sleep(10) 
        print('animation holted')
        anim.resume()     


def init():
    geo = ax.imshow([[]], extent=(
            0, 1, 0, 1), animated=True, origin='upper', zorder=100)

    fname = 'Cat_Island_Low_2.tif'
    with rasterio.open(fname, driver='GTiff') as geotif: 
        if geotif.crs != 'EPSG:4326':
            raise Warning('the file origon of the geotif is not EPSG:4326')  
        geotif_xlim=(geotif.bounds.left, geotif.bounds.right)
        geotif_ylim=(geotif.bounds.bottom, geotif.bounds.top)
        ax.set_xlim(geotif_xlim[0], geotif_xlim[1])
        ax.set_ylim(geotif_ylim[0], geotif_ylim[1])
        rgb = np.dstack((geotif.read(1), geotif.read(2), geotif.read(3)))    
    plt.setp(geo, extent=(
        geotif.bounds.left, geotif.bounds.right, geotif.bounds.bottom, geotif.bounds.top))
    geo.set_array(rgb)   

    ENC = ax.imshow([[]], extent=(
            0, 1, 0, 1), animated=True, origin='upper', zorder=100, alpha=0.6 )
    fname = 'Cat_Island_ENC.tif'
    with rasterio.open(fname, driver='GTiff') as geotif: 
        if geotif.crs != 'EPSG:4326':
            raise Warning('the file origon of the geotif is not EPSG:4326')  
        geotif_xlim=(geotif.bounds.left, geotif.bounds.right)
        geotif_ylim=(geotif.bounds.bottom, geotif.bounds.top)

        rgb = np.dstack((geotif.read(1), geotif.read(2), geotif.read(3)))    
    plt.setp(ENC, extent=(
        geotif.bounds.left, geotif.bounds.right, geotif.bounds.bottom, geotif.bounds.top))
    ENC.set_array(rgb)   

    return [geo, ENC]                               

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO) # print to console
    # logging.basicConfig(filename='main.log', encoding='utf-8', level=logging.DEBUG) # append to file
    # logging.basicConfig(filename='example.log', filemode='w', level=logging.INFO) # overide file each run


    root = tk.Tk()
    root.wm_title("plot on map")
    fig = plt.Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)

    gal = ag.gallerist(ax, fig)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    button = tk.Button(master=root, text="Quit", command=_quit)
    button.pack(side=tk.BOTTOM)

    
    threading.Thread(target=animate_iver, daemon = True).start() 
    threading.Thread(target=animate_wamv, daemon = True).start() 

    # Using init function is much faster in terms of updating but slower to rescale. It also is not stable!!!
    anim = animation.FuncAnimation(gal.fig, gal.animate, init_func=init, interval=100, blit=True, save_count=0, cache_frame_data=False)

    # # adding the maps as normal artists allows for faster resizing of the map but is slow to animate
    # threading.Thread(target=plot_geotif, daemon = True).start() 
    # anim = animation.FuncAnimation(gal.fig, gal.animate, interval=100, blit=True, save_count=0, cache_frame_data=False)


    

    # threading.Thread(target=holdani, args=(anim,), daemon = True).start()   


    tk.mainloop()