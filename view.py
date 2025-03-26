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
        self.cIndex = 0
        self.miniWindow = None

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

    def update_graph(self, names: list, cbox, *args):
        item = cbox.get()
        self.cIndex = names.index(item)


        plt.clf()
        self.reset()

        self.root.after(0, self.run, "dkk")
        self.root.mainloop()

#lav new_window om til to funktioner, en for hver knap

    def new_window(self, title="window", geoSet=False):
        if self.miniWindow is not None:
            self.miniWindow.destroy() 
        self.miniWindow = Toplevel(self.root)
        if geoSet:
            self.miniWindow.geometry("500x500")
        self.miniWindow.title(title)

        new_label = Label(self.miniWindow, borderwidth=7, text=title, font=("Calibri", 25))
        new_label.grid(row=0, column=0)

        self.miniWindow.resizable(0, 0)

    def crypto_owned_window(self):
        self.new_window("crypto coins owned", True)
        crypto_text=Label(self.miniWindow, text="BTC: 100")
        crypto_text.grid(row=1, column=0, sticky="nw")
       
        self.miniWindow.mainloop()


    def buy_sell_window(self):
        self.new_window("buy/sell", True)

        amount_input = Entry(self.miniWindow)
        amount_input.grid(row=1, column=0)

        buy_button = Button(self.miniWindow, text="Buy")
        buy_button.grid(row=2, column=0, sticky="nw")

        sell_button = Button(self.miniWindow, text="Sell")
        sell_button.grid(row=2, column=0, sticky="ne")

        self.miniWindow.mainloop()

    def run(self, curr):

        data = self.controller.model.get_coins()
        print(data)


        names = [i for i in data]
        currentCoin = names[self.cIndex]


        self.reset()
        self.drawPlot(data[currentCoin].meta, curr)
        buff = self.plotToImg()
        img = ImageTk.PhotoImage(buff)

        leftColumn = Frame(self.root)
        infoColumn = Frame(leftColumn, bg="skyblue3")
        uname = Label(leftColumn, text="Johan", padx=10, pady=10, font=("Calibri", 25))
        dropdown = ttk.Combobox(leftColumn, values=names, state="readonly")


        blnc = ui.InfoBox(infoColumn, "Balance: ", "1000kr")
        owned = ui.InfoBox(infoColumn, f"{data[currentCoin].meta['symbol'].upper()} Owned:", "5")
        day_pct = ui.InfoBox(infoColumn, "24hr change:", f"{data[currentCoin].meta['price_change_percentage_24h']}%")

        dropdown.set(names[self.cIndex])
        c_owned = Button(self.root, text="View owned crypto-stocks", padx=5, pady=2, font=("Calibri", 15), command= self.crypto_owned_window)

        lb = Label(self.root, image=img, borderwidth=7, relief="sunken", name="graph")
        trade = Button(self.root, text="Buy/Sell", padx=5, pady=2, font=("Calibri", 20, "bold"), command= self.buy_sell_window)

        dropdown.bind("<<ComboboxSelected>>", lambda *args: self.update_graph(names, dropdown, *args))

        uname.grid(row=0, column=0)
        dropdown.grid(row=1, column=0)
        blnc.grid(row=0, column=0, pady=(5, 0), sticky="nw")
        owned.grid(row=1, column=0, sticky="nw")
        day_pct.grid(row=2, column=0, pady=(0, 5), sticky="nw")
        infoColumn.grid(row=2, column=0, pady=(10, 0))
        leftColumn.grid(row=0, column=0, sticky="nw", padx=20)
        c_owned.grid(row=1, column=0, sticky="ne", padx=5, pady=(10, 5))

        lb.grid(row=0, column=1)
        trade.grid(row=1, column=1, sticky="ne", pady=(10, 0))

        self.root.resizable(0, 0)

        self.root.mainloop()
