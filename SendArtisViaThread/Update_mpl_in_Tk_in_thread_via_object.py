
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
from matplotlib import pyplot as plt, animation
import numpy as np
import queue
import threading
import time
import logging
import threadartists as ta


plt.rcParams["figure.figsize"] = [7.00, 3.50]
# plt.rcParams["figure.autolayout"] = True
# plt.rcParams['lines.linestyle'] = '--'


def provide_image1(): 
    delay = np.random.rand()*10    
    sleep = np.random.rand()  
    image = plt.imread('iver.jpg')
    artist = ta.ImageArtist(q_art, label='image plot')
    logging.debug('createdg artist %i for provide_image1', id(artist))

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
 
    artist = ta.LineArtist(q_art, label='line plot')
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
 
    
    scatter_artist = ta.ScatterArtist(q_art, s=60, marker='x', label='scatter plot')
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

def provide_temp_scatter(): 
        '''
        demonstrate deleting objects and with it reoving artists
        after some time.

        !!!!!!!!!!!! This is currently not working reliable !!!!!!!!!!!!!
        '''

        delay = np.random.rand()*10
        sleep = np.random.rand() 

        scatter_artist = ta.ScatterArtist(q_art, s=60, marker='o', label='scatter plot')
        logging.debug('createdg artist %i for provide_scatter2', id(scatter_artist))

        time.sleep(delay)
        
        for i in range(10):          
            data = np.random.rand(2)    
            new_xy = (data[0]*2, data[1]*2-1) 
            scatter_artist.add_data_to_artist(new_xy)
            # print(i)
            time.sleep(sleep)

        logging.debug('deleting artist of object %i from provide_scatter2', id(scatter_artist))    
        # once the thread ends the scatter_artist object goes out of scope and the destructor requests that
        # the artist is deleted from the list managed by the artist_manager() function.
        # !!!!!!!!! this is currently unreliable !!!!!!!!!!!!
        
        q_art.join()

def provide_scatter3():    
    scatter_artist = ta.ScatterArtist(s=60, marker='o', label='scatter plot')
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

    threading.Thread(target = provide_temp_scatter, daemon = True).start() 

    threading.Thread(target = provide_scatter1, daemon = True).start()        
    threading.Thread(target = provide_scatter1, daemon = True).start()        
    threading.Thread(target = provide_scatter1, daemon = True).start()        
    threading.Thread(target = provide_scatter1, daemon = True).start()        
    threading.Thread(target = provide_scatter1, daemon = True).start()          
    threading.Thread(target = provide_scatter1, daemon = True).start()        
    threading.Thread(target = provide_scatter1, daemon = True).start()        
    threading.Thread(target = provide_scatter1, daemon = True).start()        
    threading.Thread(target = provide_scatter1, daemon = True).start()        
    threading.Thread(target = provide_scatter1, daemon = True).start()        
      

    anim = animation.FuncAnimation(fig, ta.animate, frames=ta.artist_manager(ax, q_art), init_func=lambda : ta.init(ax), 
                                                         interval=200, blit=True)
    logging.debug('Number of threads: %i', threading.active_count())

    tk.mainloop()

