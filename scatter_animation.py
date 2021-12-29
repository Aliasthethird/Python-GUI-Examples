# https://stackoverflow.com/questions/26892392/matplotlib-funcanimation-for-scatter-plot

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

# plt.close('all')

x = np.random.rand(40)
y = np.random.rand(40)


fig = plt.figure(2)
ax = plt.axes(xlim=(0, 1), ylim=(0, 1))
scat = ax.scatter([], [], s=60)

def init():
    scat.set_offsets([])
    return scat,

def animate(i):
    data = np.hstack((x[:i,np.newaxis], y[:i, np.newaxis]))
    scat.set_offsets(data)
    return scat,

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(x)+1, 
                               interval=200, blit=True, repeat=False)

plt.show()