import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime

fig, ax = plt.subplots()

class aclass(object):
    def __init__(self, i):
        self.i = i
 
    def plot(self, ax):
        ax.set_ylim(-1.1, 1.1)
        ax.set_xlim(0, 10)
        sc = plt.scatter(self.i, self.i, marker='o', c='#1f77b4')
        return sc

class aclass2(object):
    def __init__(self, i):
        self.i = i
 
    def plot(self, ax):
        ax.set_ylim(-1.1, 1.1)
        ax.set_xlim(0, 10)
        pl = plt.plot(self.i, self.i, marker='x', c='#1f77b4')
        return pl

o0 = aclass(1)
o1 = aclass2(2)
o2 = aclass(3)
o3 = aclass2(4)

lit_of_o = [o0, o1, o2, o3]

def update(o, ax):
    temp_t = datetime.datetime.now()
    print('UPDATE',o.i)
    print(datetime.datetime.now() - temp_t)
    return o.plot(ax),
    
    
ani = FuncAnimation(fig, update, frames=lit_of_o, fargs=(ax,), interval=100, blit=False, repeat=False)
plt.show()