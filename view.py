from tkinter import *
from tkinter import ttk

from io import BytesIO
from PIL import Image, ImageTk

import matplotlib.pyplot as plt
import numpy as np

class View:
    def __init__(self):
        self.controller = None
        self.root = Tk()

    def drawPlot(self, data, currency="dkk"):
        sparkline = data["sparkline_in_7d"]["price"]
        usd_val = sparkline[-1]
        cus_val = data["current_price"]

        coeff = cus_val/usd_val
        sparkline = [i*coeff for i in sparkline]

        plt.plot(range(0, len(sparkline)), sparkline, label=data["symbol"].upper())

        ticks = np.linspace(0, len(sparkline) - 1, 7, dtype=int)
        tick_names = [str(i) for i in range(7)]

        plt.xlabel("Day")
        plt.xticks(ticks, tick_names)
        plt.ylabel(f"Value in {currency}")
        plt.title(f"7 Day sparkline of {data['name']}")
        plt.legend()
        plt.grid()

    def plotToImg(self):
        buff = BytesIO()
        plt.savefig(buff)
        buff.seek(0)
        return Image.open(buff)

    def viewCoin(self, data, curr):
        print(data)
        for child in self.root.winfo_children():
            child.destroy()
        self.drawPlot(data, curr)
        img = ImageTk.PhotoImage(self.plotToImg())

        graph = Label(self.root, image=img, width=img.width(), height=img.height(), borderwidth=7, relief="sunken")
        graph.grid(row=0, column=0)
        self.root.mainloop()

    def run(self, data, curr):
        v = 0
        r = 0
        for i in data:
            tmp = Menubutton(self.root, text=f"{i['name']}", cursor="hand2")
            tmp.grid(row=r, column=v, sticky="nw", pady=5, padx=2)
            if v < 7:
                v += 1
            else:
                r += 1
                v = 0
        self.root.mainloop()
