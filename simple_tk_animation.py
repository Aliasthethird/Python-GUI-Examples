# https://www.tutorialspoint.com/embedding-a-matplotlib-animation-into-a-tkinter-frame
import tkinter
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib import pyplot as plt, animation
import numpy as np

plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True
plt.rcParams['lines.linestyle'] = '--'

root = tkinter.Tk()
root.wm_title("Embedding in Tk")

# plt.axes()
fig = plt.Figure(dpi=200)
ax = fig.add_subplot(xlim=(0, 2), ylim=(-1.1, 1.1))
line, = ax.plot([], [], lw=2)

canvas = FigureCanvasTkAgg(fig, master=root)
# canvas.draw()
# canvas.mpl_connect(
#     "key_press_event", lambda event: print(f"you pressed {event.key}"))
# canvas.mpl_connect("key_press_event", key_press_handler)
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

button = tkinter.Button(master=root, text="Quit", command=root.quit)
button.pack(side=tkinter.BOTTOM)

toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
toolbar.update()
toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)



def init():
    line.set_data([], [])
    return line,

def animate(i):
    x = np.linspace(0, 2, 1000)
    y = np.sin(2 * np.pi * (x - 0.01 * i))
    line.set_data(x, y)
    return line,

anim = animation.FuncAnimation(fig, animate, init_func=init,frames=200, interval=20, blit=True)

tkinter.mainloop()