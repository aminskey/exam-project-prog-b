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

        self.root.after(0, self.main, "dkk")
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

        self.miniWindow.resizable(False, False)
        self.miniWindow.mainloop()

    def start_move(self, event, win):
        win.x = event.x
        win.y = event.y

    def move_win(self, event, win):
        new_x = win.winfo_x() + (event.x - win.x)
        new_y = win.winfo_y() + (event.y - win.y)

        win.geometry("+{}+{}".format(new_x, new_y))

    def winShadow(self, win, shdw):
        w, h = win.winfo_width(), win.winfo_height()
        x, y = win.winfo_x(), win.winfo_y()
        shdw.geometry(f"{w}x{h}+{x+15}+{y+30}")
        win.after(1, self.winShadow, win, shdw)

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


    def error_window(self, data):
        win = Toplevel(self.root)
        win.overrideredirect(True)
        win.attributes("-topmost", True)
        #win.geometry("300x150")

        shdw = Toplevel(win, bg="black")
        shdw.overrideredirect(True)
        shdw.attributes("-alpha", 0.5)

        content = Frame(win, relief="sunken", bd=4)
        title_bar = Frame(win, bg="blue", relief="raised", bd=5, height=30)

        buff = Image.open("Warning.png").resize((50, 50))
        img = ImageTk.PhotoImage(buff)

        crs = Image.open("cross.png")
        exitico = ImageTk.PhotoImage(crs)

        icon = Label(content, image=img)
        icon.pack(side="left", pady=10, padx=10)

        msg = Label(content, text=f"{data['msg']}", font=("Tahoma", 16))
        msg.pack(side="right")

        t1 = Label(title_bar, text=data["error"], bg="blue", fg="white", font=("Tahoma", 12))
        t1.pack(side="left")

        title_bar.pack(fill="x")
        content.pack(fill="both")

        close_btn = Button(title_bar, image=exitico, command=win.destroy, bg="#c0c0c0", bd=3, font=("Tahoma Mono", 10), relief="raised")
        close_btn.pack(side="right", pady=5, padx=5)

        win.bind("<ButtonPress-1>", lambda event: self.start_move(event, win))
        win.bind("<B1-Motion>", lambda event: self.move_win(event, win))
        win.protocol("WM_DELETE_WINDOW", self.controller.on_closing)

        win.after(0, self.winShadow, win, shdw)
        win.mainloop()

    def choosePlayer(self, inp):
        item = None
        if isinstance(inp, ttk.Combobox):
            item = inp.get()
        elif isinstance(inp, str):
            item = inp
        for i in self.controller.model.players:
            if i == item:
                self.controller.current_player = self.controller.model.players[item]
                break

        self.root.geometry("")

        plt.clf()
        self.reset()
        self.main("dkk")


    def login(self):
        self.reset()
        self.root.geometry("400x400")

        names = [name for name in self.controller.model.players]

        title = Label(self.root, text="Welcome!", font=("Calibri", 35))
        sub = Label(self.root, text="Select a player", font=("Consolas", 14))
        cbox = ttk.Combobox(self.root, values=names, state="readonly")
        btn = Button(self.root, text="Login", font=("Calibri", 15), command=lambda: self.choosePlayer(cbox), pady=2, padx=3)

        title.place(relx=0.5, rely=0.3, anchor="s")
        sub.place(relx=0.5, rely=0.45, anchor="s")
        cbox.place(relx=0.5, rely=0.5, anchor="center")
        btn.place(relx=0.5, rely=0.6, anchor="n")

        self.root.mainloop()

    def run(self, *args, **kwargs):
        self.login()
    def main(self, curr):

        data = self.controller.all_coins
        player = self.controller.current_player
        print(data)


        names = [i for i in data]
        currentCoin = names[self.cIndex]

        self.reset()
        self.drawPlot(data[currentCoin].meta, curr)
        buff = self.plotToImg()
        img = ImageTk.PhotoImage(buff)

        menu = Frame(self.root, bd=3)
        op1 = Menubutton(menu, text="Switch Users", relief="groove")
        op1.pack()

        op1.menu = Menu(op1, tearoff=0)
        op1["menu"] = op1.menu

        for i in self.controller.model.players:
            if i != player.name:
                k = i
                op1.menu.add_command(label=i, command=lambda: self.choosePlayer(k))

        leftColumn = Frame(self.root)
        infoColumn = Frame(leftColumn, bg="skyblue3")
        uname = Label(leftColumn, text=player.name, padx=10, pady=10, font=("Calibri", 25))
        dropdown = ttk.Combobox(leftColumn, values=names, state="readonly")


        blnc = ui.InfoBox(infoColumn, "Balance: ", player.money)

        amnt_owned = player.coins[data[currentCoin].meta['name']].amount if data[currentCoin].meta['name'] in player.coins.keys() else "0"

        owned = ui.InfoBox(infoColumn, f"{data[currentCoin].meta['symbol'].upper()} Owned:", amnt_owned)
        day_pct = ui.InfoBox(infoColumn, "24hr change:", f"{data[currentCoin].meta['price_change_percentage_24h']}%")

        dropdown.set(names[self.cIndex])
        c_owned = Button(self.root, text="View owned crypto-stocks", padx=5, pady=2, font=("Calibri", 15), command= self.crypto_owned_window)

        lb = Label(self.root, image=img, borderwidth=7, relief="sunken", name="graph")
        trade = Button(self.root, text="Buy/Sell", padx=5, pady=2, font=("Calibri", 20, "bold"), command= self.buy_sell_window)

        dropdown.bind("<<ComboboxSelected>>", lambda *args: self.update_graph(names, dropdown, *args))

        menu.grid(row=0, column=0, sticky="nw")
        uname.grid(row=1, column=0)
        dropdown.grid(row=2, column=0)
        blnc.grid(row=1, column=0, pady=(5, 0), sticky="nw")
        owned.grid(row=2, column=0, sticky="nw")
        day_pct.grid(row=3, column=0, pady=(0, 5), sticky="nw")
        infoColumn.grid(row=3, column=0, pady=(10, 0))
        leftColumn.grid(row=1, column=0, sticky="nw", padx=20)
        c_owned.grid(row=2, column=0, sticky="ne", padx=5, pady=(10, 5))

        lb.grid(row=1, column=1)
        trade.grid(row=2, column=1, sticky="ne", pady=(10, 0))

        self.root.mainloop()