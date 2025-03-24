import tkinter as tk

class InfoBox(tk.Frame):
    def __init__(self, root, heading, value, *args, **kwargs):
        tk.Frame.__init__(self, root, bg="skyblue3", *args, **kwargs)
        #self.player = player
        self.root = root
        #self.data = data
        self.font = ("Calibri", 20)
        self.subfont = ("Calibri", 15)

        self.lb1 = tk.Label(self, text=heading, font=self.font, bg="skyblue3")
        self.value1 = tk.Label(self, text=value, font=self.subfont, bg="skyblue3")

        self.lb1.pack(pady=(10, 0), anchor="nw")
        self.value1.pack(padx=(5, 0), pady=(0, 15), anchor="nw")

