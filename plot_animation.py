import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

frame_i = [1, 2, 3, 4]

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'ro')

def init_ani():
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    return ln,

def ani(i):
    xdata.append(i)
    ydata.append(i)
    ln.set_data(xdata, ydata)
    return ln,

ani = FuncAnimation(fig, ani, frames=frame_i,
                    init_func=init_ani, blit=True)
plt.show()