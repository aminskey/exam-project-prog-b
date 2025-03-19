import tkinter as tk

class InfoBox(tk.Frame):
    def __init__(self, root, player, data, *args, **kwargs):
        tk.Frame.__init__(self, root, bg="skyblue3", *args, **kwargs)
        self.player = player
        self.root = root
        self.data = data
        self.font = ("Calibri", 15)

        self.lb1 = tk.Label(self, text="Balance:", font=self.font, bg="skyblue3")
        self.lb2 = tk.Label(self, text=f"{self.data['symbol'].upper()} owned:", font=self.font, bg="skyblue3")

        self.value1 = tk.Label(self, text="1000 kr", bg="skyblue3")
        self.value2 = tk.Label(self, text="2", bg="skyblue3")

        self.lb1.pack(pady=(10, 0), anchor="nw")
        self.value1.pack(padx=(5, 0), pady=(0, 15), anchor="nw")

        self.lb2.pack(pady=(10, 0), anchor="nw")
        self.value2.pack(padx=(5, 0), pady=(0, 15), anchor="nw")