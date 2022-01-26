"""
Demonstrates how to use the artgallery library to plot two animaitons
"""

import tkinter as tk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np    
import threading
import time
import artgallery as ag

__author__ = 'Gero Nootz'
__copyright__ = ''
__credits__ = ['', '']
__license__ = ''
__version__ = '1.0.0'
__date__ = '01/25/2022'
__maintainer__ = 'Gero Nootz'
__email__ = 'gero.nootz@usm.edu'
__status__ = 'example'

class plot_image(): 
        def __init__(self, gal: ag.Gallerist):
            self.gal = gal
            self.artist = ag.ImageArtist(self.gal, label='image plot')
            self.artist.append_data_to_artist('yota.png', size=0.1, position=(1,0), deg=0)
        
        def update(self): 
            data = np.random.rand(2)    
            new_xy = (data[0]*2, data[1]*2 - 1) 
            self.artist.set_position(new_xy, np.random.rand()*360)
            root.after(500, self.update)            

class PlotRandLine(threading.Thread):
        def __init__(self, gal: ag.Gallerist):
            self.gal = gal
            threading.Thread.__init__(self, daemon=True)

        def run(self):   
            artist = ag.LineArtist(self.gal, label='line plot', zorder=10)
            i = 0
            while True:        
                data = np.random.rand(2)    
                new_xy = (data[0]*2, data[1]*2 - 1) 
                artist.append_data_to_artist(new_xy)
                if i%100 == 0:
                    artist.clear_data()
                i += 1
                time.sleep(0.1)

class PlotRandScetter(threading.Thread):
        def __init__(self, gal: ag.Gallerist):
            self.gal = gal
            threading.Thread.__init__(self, daemon=True)

        def run(self): 
            """ 
            Demonstrates how to plot a scatter artist from a thread using
            append_data_to_artist(new_xy)
            """       
            scatter_artist = ag.ScatterArtist(self.gal, s=60, marker='^', label='scatter plot')
            while True:        
                data = np.random.rand(10,2)
                data[:, 1] = (data[:, 1] * 2) - 1
                data[:, 0] = data[:, 0] * 2
                scatter_artist.add_data_to_artist(data, facecolors=np.random.rand(10,4))
                time.sleep(1)     

if __name__ == '__main__':

    root = tk.Tk()
    root.title("Two Galleries at the same time")

    # root.rowconfigure(0, weight=1)
    # root.columnconfigure(1, weight=3)

    frame1 = tk.Frame(root).grid(row=0, column=0)
    fig1 = plt.Figure()
    ax1 = fig1.add_subplot(xlim=(0, 2), ylim=(-1.1, 1.1))
    ax1.set_xlabel('x-data')
    ax1.set_ylabel('y-data')
    canvas1 = FigureCanvasTkAgg(fig1, master=frame1)
    canvas1.get_tk_widget().grid(row=0, column=0)

    frame2 = tk.Frame(root).grid(row=0, column=0)
    fig2 = plt.Figure()
    ax2 = fig2.add_subplot(xlim=(0, 2), ylim=(-1.1, 1.1))
    ax2.set_xlabel('x-data')
    ax2.set_ylabel('y-data')
    canvas2 = FigureCanvasTkAgg(fig2, master=frame2)
    canvas2.get_tk_widget().grid(row=1, column=1)

    gal1 = ag.Gallerist(ax1, fig1, interval=100)
    PlotRandLine(gal1).start()   # demonstrate class container 
    plot_image(gal1).update() # demonstrate using tk.after method to update  

    gal2 = ag.Gallerist(ax2, fig2, interval=100)
    plot_image(gal2).update() # demonstrate using tk.after method to update  
    PlotRandScetter(gal2).start() # demonstrate class container

    root.mainloop()