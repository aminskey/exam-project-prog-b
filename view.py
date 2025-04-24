from tkinter import *
from tkinter import ttk

from io import BytesIO
from PIL import Image, ImageTk

from player import Coin

import matplotlib.pyplot as plt
import numpy as np
import UI_widgets as ui

class View:
    def __init__(self):
        self.controller = None
        self.root = Tk()
        self.cIndex = 0
        self.chosenPlayer = None
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

    def reset(self, killWindow=True):
        if self.miniWindow is not None and killWindow:
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

    
    def process_transaction(self, amount_input, action):
        input_data = amount_input.get().strip()

        if not input_data:
            print("Empty")
            return
        
        try:
            amount = int(input_data)
            if amount <= 0:
                print("Must be greater than zero")
                return
            
            coin_name = list(self.controller.all_coins.keys())[self.cIndex]
            coin_data = self.controller.all_coins[coin_name].meta
            coin_price = coin_data["current_price"]
            player = self.controller.current_player

            if action == "buy":
                total_cost = amount * coin_price

                if player.money >= total_cost:
                    player.invest(Coin(coin_name, coin_price), amount)
                    print(f"succes buy {amount}")
                else:
                    print("not enough money")

            elif action == "sell":
                if player.getAmountOfCoin(coin_name) >= amount:
                    player.sell(Coin(coin_name, coin_price), amount)
                    print(f"succes sell {amount}")
                else:
                    print("not enough coin")

        except ValueError:
            print("Invalid input")    
        

        plt.clf()
        self.reset(killWindow=False)

        self.root.after(0, self.main, "dkk")
        self.root.mainloop()
        
    def crypto_owned_window(self):
        self.new_window("Crypto Coins Owned", False)
        player_coins = self.controller.current_player.coins

        container = Frame(self.miniWindow)
        container.grid(row=1, column=0, sticky="nsew")

        canvas = Canvas(container, highlightthickness=0)
        canvas.grid(row=0, column=0, sticky="nsew")

        scrollbar = Scrollbar(container, orient=VERTICAL, command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")  

        scrollable_frame = Frame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        
        def on_frame_configure(*args):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scrollable_frame.bind("<Configure>", on_frame_configure)
        canvas.configure(yscrollcommand=scrollbar.set)

        
        def _on_mouse_wheel(event):
            canvas.yview_scroll(-1 * (event.delta // 120), "units")

        self.miniWindow.bind("<MouseWheel>", _on_mouse_wheel)  
        
        for i, coins in enumerate(player_coins.values(), start=1):
            for k, coin in enumerate(coins.arr, start=1):
                coin_label = Label(scrollable_frame, text=f"{coin.type}: {coin.amount}", font=("Calibri", 14))
                coin_label.grid(row=k+i, column=0, sticky="w", padx=10, pady=5)

        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.miniWindow.mainloop()



    def buy_sell_window(self):
        self.new_window("Buy or Sell stocks", False)

        frm = Frame(self.miniWindow)

        coin = list(self.controller.all_coins.keys())[self.cIndex]
        symbol = self.controller.all_coins[coin].meta["symbol"].upper()

        lbl = Label(self.miniWindow, text=symbol, font=("Calibri", 16))

        amount_input = Entry(frm)
        amount_input.grid(row=1, column=0)


        buy_button = Button(frm, text="Buy", command=lambda: self.process_transaction(amount_input, "buy"))
        buy_button.grid(row=2, column=0, sticky="nw")

        sell_button = Button(frm, text="Sell", command=lambda: self.process_transaction(amount_input, "sell"))
        sell_button.grid(row=2, column=0, sticky="ne")

        lbl.grid(row=1, column=0, sticky="nw")
        frm.grid(row=1, column=0, sticky="ne", padx=10, pady=10)
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
        icon.grid(row=0, column=0, pady=10, padx=10)


        message = Frame(content)

        if len(data['msg'].split()) < 4:
            msg = Label(message, text=f"{data['msg']}", font=("Tahoma", 11))
            msg.grid(row=0, column=0, padx=(10, 0), sticky="nw")
        else:
            tmp = ""
            j = 0
            i = 0
            for word in data['msg'].split():
                tmp += word + " "
                if (i % 4 == 0 and i > 0) or i >= len(data['msg'].split()) - 1:
                    msg = Label(message, text=f"{tmp}", font=("Tahoma", 11))
                    msg.grid(row=j, column=0, padx=(10, 0), sticky="nw")

                    tmp = ""
                    j += 1
                i += 1

        message.grid(row=0, column=1, sticky="nw")

        t1 = Label(title_bar, text=data["error"], bg="blue", fg="white", font=("Tahoma", 12))
        t1.pack(side="left")

        title_bar.pack(fill="x")
        content.pack(fill="both")

        close_btn = Button(title_bar, image=exitico, command=win.destroy, bg="#c0c0c0", bd=3, font=("Tahoma Mono", 10), relief="raised")
        close_btn.pack(side="right", pady=5, padx=5)

        win.bind("<ButtonPress-1>", lambda event: self.start_move(event, win))
        win.bind("<B1-Motion>", lambda event: self.move_win(event, win))
        win.protocol("WM_DELETE_WINDOW", lambda: self.controller.on_closing(True))

        win.after(0, self.winShadow, win, shdw)
        win.mainloop()

    def choosePlayer(self, inp, index=None):
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

        plt.clf()
        self.reset()
        self.drawPlot(data[currentCoin].meta, curr)
        buff = self.plotToImg()
        img = ImageTk.PhotoImage(buff)

        menu = Frame(self.root, bd=3)
        op1 = Menubutton(menu, text="Options", relief="groove")
        op1.pack()

        op1.menu = Menu(op1, tearoff=0)
        op1["menu"] = op1.menu

        op1.menu.add_command(label="Switch User", command=self.login)
        op1.menu.add_separator()
        op1.menu.add_command(label="Quit", command=self.controller.on_closing)

        leftColumn = Frame(self.root)
        infoColumn = Frame(leftColumn, bg="skyblue3")
        uname = Label(leftColumn, text=player.name, padx=10, pady=10, font=("Calibri", 25))
        dropdown = ttk.Combobox(leftColumn, values=names, state="readonly")


        blnc = ui.InfoBox(infoColumn, "Balance: ", player.money)

        amnt_owned = player.getAmountOfCoin(data[currentCoin].meta['name'])

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

        self.root.after(60000, self.controller.retrieveCoinData)
        self.root.after(60001, self.main, curr)
        self.root.mainloop()