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
        if self.miniWindow is not None:
            self.miniWindow.destroy()
        for child in self.root.winfo_children():
            child.destroy()


    def update_graph(self, names: list, cbox, *args):
        item = cbox.get()
        self.cIndex = names.index(item)

        plt.clf()
        self.reset()

        self.root.after(0, self.run, "dkk")
        self.root.mainloop()


    def new_window(self):
        if self.miniWindow is not None:
            self.miniWindow.destroy()
        self.miniWindow = Toplevel(self.root)
        self.miniWindow.geometry("500x500")
        self.miniWindow.title("window")

        self.miniWindow.resizable(False, False)
        self.miniWindow.mainloop()

    def start_move(self, event, win):
        win.x = event.x
        win.y = event.y

    def move_win(self, event, win):
        new_x = win.winfo_x() + (event.x - win.x)
        new_y = win.winfo_y() + (event.y - win.y)

        win.geometry("+{}+{}".format(new_x, new_y))

    def error_window(self, data):
        win = Toplevel(self.root)
        win.overrideredirect(True)
        win.attributes("-topmost", True)
        win.geometry("300x150")

        content = Frame(win)
        title_bar = Frame(win, bg="blue", relief="raised", bd=5, height=30)

        buff = Image.open("Warning.png").resize((50, 50))
        img = ImageTk.PhotoImage(buff)
        icon = Label(content, image=img)
        icon.pack(side="left")

        msg = Label(content, text=f"{data['msg']}", font=("Tahoma", 16))
        msg.pack()


        title_bar.pack(fill="x")
        content.pack(fill="both")

        t1 = Label(title_bar, text="Error", bg="blue", fg="white", font=("Tahoma", 12))
        t1.pack(side="left")

        close_btn = Button(title_bar, text="X", command=win.destroy, bg="red", fg="white", bd=0)
        close_btn.pack(side="right")

        win.bind("<ButtonPress-1>", lambda event: self.start_move(event, win))
        win.bind("<B1-Motion>", lambda event: self.move_win(event, win))

        win.mainloop()

    def run(self, curr):

        data = self.controller.all_coins
        player = self.controller.current_player
        print(data)

        names = [i for i in data]
        currentCoin = names[self.cIndex]

        self.reset()
        self.drawPlot(data[currentCoin].meta, curr)
        buff = self.plotToImg()
        img = ImageTk.PhotoImage(buff)

        leftColumn = Frame(self.root)
        infoColumn = Frame(leftColumn, bg="skyblue3")
        uname = Label(leftColumn, text=player.name, padx=10, pady=10, font=("Calibri", 25))
        dropdown = ttk.Combobox(leftColumn, values=names, state="readonly")


        blnc = ui.InfoBox(infoColumn, "Balance: ", player.money)

        amnt_owned = player.coins[data[currentCoin].meta['name']].amount if data[currentCoin].meta['name'] in player.coins.keys() else "0"

        owned = ui.InfoBox(infoColumn, f"{data[currentCoin].meta['symbol'].upper()} Owned:", amnt_owned)
        day_pct = ui.InfoBox(infoColumn, "24hr change:", f"{data[currentCoin].meta['price_change_percentage_24h']}%")

        dropdown.set(names[self.cIndex])
        c_owned = Button(self.root, text="View owned crypto-stocks", padx=5, pady=2, font=("Calibri", 15), command= self.new_window)

        lb = Label(self.root, image=img, borderwidth=7, relief="sunken", name="graph")
        trade = Button(self.root, text="Buy/Sell", padx=5, pady=2, font=("Calibri", 20, "bold"), command= self.new_window)

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

        self.root.mainloop()
