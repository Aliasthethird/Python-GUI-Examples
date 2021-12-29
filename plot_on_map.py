import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'ro')

def init():
    im = show(rasterio.open('stennis_QW.tif'), ax=ax)
    return ln,

def ani(i):
    xdata.append(-89.6327 + random.random()*0.005)
    ydata.append(30.351 + random.random()*0.005)
    ln.set_data(xdata, ydata)
    return ln,

anim = FuncAnimation(fig, ani, frames=100,
                    init_func=init, repeat=False, blit=True)
plt.show()


