"""
Demonstrates how to use the artgallery library to plot on a map using init_func.
This is faster than adding the background image as an animation artist
but has some unexplained bugs. Resizing the figure will resume the animation
"""

import tkinter as tk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib import (pyplot as plt, animation)
from matplotlib.backend_bases import key_press_handler
import threading
import time
import logging
import math

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

class AnimateIver(threading.Thread):
    def __init__(self):
       threading.Thread.__init__(self, daemon=True)

    def run(self): 
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
                i += 0.001
                if (x_pos-iver_art.ax.get_xlim()[0]) > x_range:
                    trace_art.clear_data()
                    i = 0
                time.sleep(0.1)

class AnimateWamV(threading.Thread):
    def __init__(self):
       threading.Thread.__init__(self, daemon=True)

    def run(self): 
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

class PlotGeotif(threading.Thread):
    def __init__(self):
       threading.Thread.__init__(self, daemon=True)

    def run(self): 
            """Work in progress..."""
            satimage = ag.GeoTifArtist(gal, label='Sat plot', zorder=5, alpha=1, add_artist_to_init_func=True)
            satimage.add_data_to_artist('Cat_Island_Low_2.tif')

            noaachart = ag.GeoTifArtist(gal, label='Cat Island ENC', zorder=6, alpha=0.6, add_artist_to_init_func=True)
            noaachart.add_data_to_artist('Cat_Island_ENC.tif')

            satimage.set_xlim(satimage.geotif_xlim[0], satimage.geotif_xlim[1])
            satimage.set_ylim(satimage.geotif_ylim[0], satimage.geotif_ylim[1])

            while True: 
                time.sleep(10)

def _quit():
    root.quit()     
    root.destroy()  


def holdani(anim):
    while True:
        time.sleep(10)    
        print('animation holted')
        anim.pause()
        # anim.event_source.stop()
        time.sleep(10) 
        print('animation resumed')
        anim.resume() 
        # anim._init_func() # use to call init_func with flush_events()
        # anim.frame_seq = anim.new_frame_seq() 
        # canvas.flush_events() # calls init_func of FuncAnimation() but does not update the background. Why?
        # https://github.com/matplotlib/matplotlib/blob/710fce3df95e22701bd68bf6af2c8adbc9d67a79/lib/matplotlib/backends/_backend_tk.py#L161
                     

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO) # print to console
    # logging.basicConfig(filename='main.log', encoding='utf-8', level=logging.DEBUG) # append to file
    # logging.basicConfig(filename='example.log', filemode='w', level=logging.INFO) # overide file each run
 
    root = tk.Tk()
    root.wm_title("plot on map")
    fig = plt.Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)

  
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    button = tk.Button(master=root, text="Quit", command=_quit)
    button.pack(side=tk.BOTTOM)

    gal = ag.Gallerist(ax, fig)

    PlotGeotif().start()
    AnimateIver().start()
    AnimateWamV().start()

    # Using init function is much faster in terms of updating but slower to rescale. It also is not stable!!!
    anim = animation.FuncAnimation(gal.fig,
                                    gal.animate,
                                    init_func=gal.init_func,
                                    interval=100,
                                    blit=True)

    # demonstrat holting animation
    # threading.Thread(target=holdani, args=(anim,), daemon = True).start()   

    tk.mainloop()