"""
Demonstrate how to update a matplotlib graph via a queue from a thread in tkinter
"""
# https://www.tutorialspoint.com/embedding-a-matplotlib-animation-into-a-tkinter-frame
import tkinter
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib import pyplot as plt, animation
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

# plt.axes()
fig = plt.Figure(dpi=200)
ax = fig.add_subplot(xlim=(0, 2), ylim=(-1.1, 1.1))

line, = ax.plot([], [], lw=2)
plt.getp(line)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

button = tkinter.Button(master=root, text="Quit", command=root.quit)
button.pack(side=tkinter.BOTTOM)

toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
toolbar.update()
toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)

def init():
    line.set_data([], [])
    ax.set_xlabel('x-data')
    ax.set_ylabel('y-data')
    return line,

def animate(line):
    return line

q = queue.Queue()

def provide(line):
    i = 0
    while True:
        q.put(line)
        i += 1      
        x = np.linspace(0, 2, 100)
        y = np.sin(2 * np.pi * (x - 0.01 * i))
        line.set_data(x, y)
        time.sleep(0.05)
      

def collect_from_queue():
    while True:
        if q.qsize() > 100:
            logging.warning('Queue size is %i', q.qsize())
        yield q.get(),

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    threading.Thread(target = provide,args=(line,), daemon = True).start()        

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=collect_from_queue(), interval=30, blit=True)
    print("Number of threads: ", threading.active_count())
    tkinter.mainloop()