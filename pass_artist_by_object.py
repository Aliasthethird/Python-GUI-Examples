import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime

fig, ax = plt.subplots()

class aclass(object):
    def __init__(self, i):
        self.i = i
 
    def plot(self, ax):
        ax.set_ylim(0, 10)
        ax.set_xlim(0, 10)
        sc = plt.scatter(self.i, self.i, marker='o', c='#1f77b4')
        return sc

class aclass2(object):
    def __init__(self, i):
        self.i = i
 
    def plot(self, ax):
        ax.set_ylim(0, 10)
        ax.set_xlim(0, 10)
        pl = plt.plot(self.i, self.i, marker='x', c='#1f77b4')
        return pl

def objects():
    n = 100
    for cnt in range(n):
        if cnt % 2 == 0:
            o1 = aclass(1)
            yield o1
        else:
            o2 = aclass(cnt*10/n)
            yield o2

def update(o, ax):
    temp_t = datetime.datetime.now()
    print('UPDATE',o.i)
    print(datetime.datetime.now() - temp_t)
    return o.plot(ax),
    
    
ani = FuncAnimation(fig, update, frames=objects, fargs=(ax,), interval=10, blit=False, repeat=False)
plt.show()