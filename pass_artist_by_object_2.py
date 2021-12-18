'''Demonstrates how to pass class methods to generate new artists''' 

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime
import itertools

fig, ax = plt.subplots()
# sc, = plt.scatter([], [], 'ro')

class class1(object):
    def __init__(self, i):
        self.i = i
        self.xdata, self.ydata = [], []
        self.ax = None
 
    def plot(self, ax):
        if self.ax is None:
            self.ax = ax
            self.pl, = self.ax.plot([1, 2], [1, 2], marker='None', linestyle='--', c='#1f77b4')

        self.xdata.append(self.i)
        self.ydata.append(self.i)
        self.pl.set_data(self.xdata, self.ydata)
        return self.pl

class class2(object):
    def __init__(self, i):
        self.i = i
        self.xdata, self.ydata = [], []
        self.ax = None
 
    def plot(self, ax):
        if self.ax is None:
            self.ax = ax
            self.pl, = self.ax.plot([1, 2], [1, 2], marker='x', linestyle='None', c='#1f77b4')

        self.xdata.append(self.i)
        self.ydata.append(self.i+1)
        self.pl.set_data(self.xdata, self.ydata)
        return self.pl

o1 = class1(0)
o2 = class2(0)

def objects():
    n = 100
    for cnt in range(n):
        if cnt % 2 == 0:
            o1.i = cnt*10/n
            yield o1
        else:
            o2.i = cnt*10/n
            yield o2
       

def init_plot():
    ax.set_ylim(0, 10)
    ax.set_xlim(0, 10)

def update_plot(plot_object, ax):
    # temp_t = datetime.datetime.now()
    # print('UPDATE',o.i)
    # print(datetime.datetime.now() - temp_t)
    plot_object.plot(ax)
    print(id(plot_object))
    # artists.append(o.plot(ax))
    # return artists
    

ani = FuncAnimation(fig, update_plot, frames=objects, fargs=(ax,), interval=0, init_func=init_plot, blit=False, repeat=False)
plt.show()