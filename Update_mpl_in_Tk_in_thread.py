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


import tkinter
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib import pyplot as plt, animation
import matplotlib.patches as patches
import matplotlib.cbook as cbook
import numpy as np
import queue
import threading
import time
import logging

plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True
plt.rcParams['lines.linestyle'] = '--'

root = tkinter.Tk()
root.wm_title("Update mpl in Tk via queue")

fig = plt.Figure(dpi=200)
ax = fig.add_subplot(xlim=(0, 2), ylim=(-1.1, 1.1))

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

button = tkinter.Button(master=root, text="Quit", command=root.quit)
button.pack(side=tkinter.BOTTOM)

toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
toolbar.update()
toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)


def provide_sin_1(ax):
    time.sleep(5)
    i = 0
    line, = ax.plot([], [], '--', lw=2, animated=True)
    # plt.getp(line)
    q.put(line)
    while True:        
        i += 1      
        x = np.linspace(0, 2, 100)
        y = np.sin(2 * np.pi * (x - 0.01 * i))
        line.set_data(x, y)
        time.sleep(0.05)

def provide_sin_2(ax):
    time.sleep(10)
    i = 0
    line, = ax.plot([], [], '.', lw=2, animated=True)
    # plt.getp(line)
    q.put(line)
    while True:        
        i += 1      
        x = np.linspace(0, 2, 100)
        y = np.cos(2 * np.pi * (x - 0.01 * i))
        line.set_data(x, y)
        time.sleep(0.1)

def provide_sin_3(ax):
    time.sleep(1)
    i = 0
    line, = ax.plot([], [], '-', lw=2, animated=True)
    # plt.getp(line)
    q.put(line)
    while True:        
        i += 1      
        x = np.linspace(0, 2, 100)
        y = np.cos(2 * np.pi * (x - 0.01 * i))
        line.set_data(x, y)
        time.sleep(0.5)

def provide_line(ax):
    time.sleep(0)
    i = 0
    line, = ax.plot([], [], '-', lw=2, animated=True)
    new_xy = ([],[])
    xy_data = np.array([], dtype=float).reshape(0, 2) # prepare (N,2) array
    # plt.getp(line)
    q.put(line)
    while True:        
        i += 1/100     
        new_xy = (i, i-1) 
        xy_data = np.vstack([xy_data, [[new_xy[0], new_xy[1]]]])
        line.set_data(xy_data[:,0], xy_data[:,1])
        time.sleep(0.1)

def provide_scatter(ax):
    time.sleep(0)
    scat = ax.scatter([], [], s=60, edgecolors='r',
                  facecolors='none', marker='o', label='scatter plot', animated=True)
    new_xy = ([],[])
    xy_data = np.array([], dtype=float).reshape(0, 2) # prepare (N,2) array
    # plt.getp(line)
    q.put(scat)
    while True:        
        data = np.random.rand(2)    
        new_xy = (data[0]*2, data[1]*2-1) 
        xy_data = np.vstack([xy_data, [[new_xy[0], new_xy[1]]]])
        scat.set_offsets(xy_data)
        time.sleep(1)

def provide_image(ax):
    # https://matplotlib.org/stable/gallery/images_contours_and_fields/image_clip_path.html#sphx-glr-gallery-images-contours-and-fields-image-clip-path-py
    time.sleep(0.1)
    with cbook.get_sample_data('grace_hopper.jpg') as image_file:
        image = plt.imread(image_file)
    sc = 10
    im_art = ax.imshow(image, extent=(0.05*sc, 0.15*sc, -0.06*sc, 0.06*sc), zorder=10, animated=True)  
    # patch = patches.Circle((0.0260, 0.0200), radius=0.01, transform=ax.transData)
    # im.set_clip_path(patch)      
    # plt.getp(im)
    q.put(im_art)
    i = 0
    while True:  
        i += 1/100
        im_art.set_extent((0.05*i, 0.15*i, -0.06*i, 0.06*i))     
        time.sleep(0.01)
      

def artist_manager(ax) -> list:
    """
    Collects new artists from a queue into a list of artists
    to be animated in matplotlib.animation.FuncAnimation
    -> returns a list of artists
    """
    artists = []
    while True:
        if not q.empty():
            if q.qsize() > 100:
                logging.warning('Queue size is %i', q.qsize())
            artist = q.get()
            artists.append(artist)
            logging.info('Number of artists: %i', len(artists))    
        else:
            pass
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

    logging.basicConfig(level=logging.INFO)
    q = queue.SimpleQueue()

    threading.Thread(target = provide_sin_1,args=(ax,), daemon = True).start()        
    threading.Thread(target = provide_sin_2,args=(ax,), daemon = True).start()        
    threading.Thread(target = provide_sin_3,args=(ax,), daemon = True).start()        
    threading.Thread(target = provide_line,args=(ax,), daemon = True).start()        
    threading.Thread(target = provide_scatter,args=(ax,), daemon = True).start()        
    threading.Thread(target = provide_image,args=(ax,), daemon = True).start()        

    anim = animation.FuncAnimation(fig, animate, frames=artist_manager(ax), init_func=init, 
                                                         interval=100, blit=True)
    logging.info('Number of threads: %i', threading.active_count())

    tkinter.mainloop()