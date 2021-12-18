"""
Demonstrates how to pass class methods to generate new artists.

Unfortunately, this is getting slower and slower as more artists are 
added -> do NOT use! See pass_artis_by_object_2 instead
"""

__author__ = 'Gero Nootz'
__version__ = '1.0.0'
__email__ = 'gero.noozt@usm.edu'
__status__ = 'Prototype'
# https://www.python.org/dev/peps/pep-0008/#module-level-dunder-names
    
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime


fig, ax = plt.subplots()

class Aclass1(object):
    def __init__(self, i):
        self.i = i
 
    def plot(self, ax):
        ax.set_ylim(0, 10)
        ax.set_xlim(0, 10)
        sc = plt.scatter(self.i, self.i, marker='o', c='g')
        return sc

class Aclass2(object):
    def __init__(self, i):
        self.i = i
 
    def plot(self, ax):
        ax.set_ylim(0, 10)
        ax.set_xlim(0, 10)
        pl = plt.plot(self.i, self.i, marker='x', c='r')
        return pl

def objects():
    n = 100
    for cnt in range(n):
        if cnt % 2 == 0:
            o1 = Aclass1(cnt*10/n)
            yield o1
        else:
            o2 = Aclass2(cnt*10/n)
            yield o2

def update(o, ax):
    temp_t = datetime.datetime.now()
    print('UPDATE',o.i)
    print(datetime.datetime.now() - temp_t)
    return o.plot(ax),
    
    
ani = FuncAnimation(fig, update, frames=objects, fargs=(ax,), interval=10, blit=False, repeat=False)
plt.show()