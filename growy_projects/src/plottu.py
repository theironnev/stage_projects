import random

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
import numpy as np
import serial as sr
from matplotlib.animation import FuncAnimation
from itertools import count

# ------global variables
data = np.array([])
cond = False



# -----Main GUI code-----
root = tk.Tk()
root.title('Real Time Plot')
root.configure(background='light blue')
root.geometry("700x500")  # set the window size

# ------create Plot object on GUI----------
# add figure canvas
fig = Figure()
ax = fig.add_subplot(111)

# ax = plt.axes(xlim=(0,100),ylim=(0, 120)); #displaying only 100 samples

lines = ax.plot([], [])[0]

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.get_tk_widget().place(x=10, y=10, width=500, height=400)
canvas.draw()


# -----plot data-----
def animate(i):
    global cond, data

    a = random.randint(500, 5000)

    ax.cla()
    ax.set_xticks([])
    ax.set_title('gutter scale')
    ax.set_xlabel('Time')
    ax.set_ylabel('weight(g)')
    ax.set_ylim(-0.5, 5000)
    ax.set_yticks([0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000])

    if (len(data) < 100):
        data = np.append(data, a)
        print(data)
    else:
        data[0:99] = data[1:100]
        data[99] = a

    ax.plot(np.arange(0, len(data)),data)



ani = FuncAnimation(fig, animate, interval=100)



if __name__ == '__main__':
    root.mainloop()