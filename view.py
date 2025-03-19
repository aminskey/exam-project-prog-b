from tkinter import *
from tkinter import ttk

from io import BytesIO
from PIL import Image, ImageTk

import matplotlib.pyplot as plt
import numpy as np
import UI_widgets as ui

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

    def reset(self):
        for child in self.root.winfo_children():
            child.destroy()


    def run(self, data, curr):

        names = [i["symbol"].upper() for i in data]

        self.reset()
        self.drawPlot(data[-1], curr)
        buff = self.plotToImg()
        img = ImageTk.PhotoImage(buff) # buff.resize((buff.width*3//4, buff.height*3//4))

        leftColumn = Frame(self.root)
        infoBox = ui.InfoBox(leftColumn, None, data[-1], relief="raised", height=self.root.winfo_height()//2)


        uname = Label(leftColumn, text="NAME", padx=10, pady=10, font=("Calibri", 25))
        dropdown = ttk.Combobox(leftColumn, values=names)

        lb = Label(self.root, image=img, borderwidth=7, relief="sunken")
        trade = Button(self.root, text="Buy/Sell", padx=5, pady=2, font=("Calibri", 20, "bold"))

        uname.grid(row=0, column=0)
        dropdown.grid(row=1, column=0)
        infoBox.grid(row=5, column=0, pady=(10, 0))
        leftColumn.grid(row=0, column=0, sticky="nw", padx=20)

        lb.grid(row=0, column=1)
        trade.grid(row=1, column=1, sticky="ne", pady=(10, 0))

        self.root.mainloop()
