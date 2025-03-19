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



    def update_graph(self, event, names: list, data, w):
        item = w.get()
        i = names.index(item)

        plt.clf()
        for w in self.root.winfo_children():
            if w.winfo_name() == "graph":
                w.destroy()

        self.drawPlot(data[i], "dkk")
        buff = self.plotToImg()
        img = ImageTk.PhotoImage(buff)
        lb = Label(self.root, image=img, borderwidth=7, relief="sunken", name="graph")
        lb.grid(row=0, column=1)

        self.root.mainloop()




    def run(self, data, curr):

        names = [i["name"] for i in data]

        self.reset()
        self.drawPlot(data[-1], curr)
        buff = self.plotToImg()
        img = ImageTk.PhotoImage(buff) # buff.resize((buff.width*3//4, buff.height*3//4))

        leftColumn = Frame(self.root)
        infoBox = ui.InfoBox(leftColumn, None, data[-1], relief=RAISED, height=self.root.winfo_height()//2)


        uname = Label(leftColumn, text="NAME", padx=10, pady=10, font=("Calibri", 25))
        dropdown = ttk.Combobox(leftColumn, values=names, state="readonly")
        dropdown.set(names[-1])
        c_owned = Button(self.root, text="View owned crypto-stocks", padx=5, pady=2, font=("Calibri", 15))

        lb = Label(self.root, image=img, borderwidth=7, relief="sunken", name="graph")
        trade = Button(self.root, text="Buy/Sell", padx=5, pady=2, font=("Calibri", 20, "bold"))

        dropdown.bind("<<ComboboxSelected>>", lambda event: self.update_graph(event, names, data, dropdown))

        uname.grid(row=0, column=0)
        dropdown.grid(row=1, column=0)
        infoBox.grid(row=2, column=0, pady=(10, 0))
        leftColumn.grid(row=0, column=0, sticky="nw", padx=20)
        c_owned.grid(row=1, column=0, sticky="ne", padx=5, pady=(10, 5))

        lb.grid(row=0, column=1)
        trade.grid(row=1, column=1, sticky="ne", pady=(10, 0))

        self.root.mainloop()
