from tkinter import *

class View:
    def __init__(self):
        self.controller = None
        self.root = Tk()

    def run(self, data):
        v = 1
        r = 0
        for i in data:
            tmp = Label(self.root, bd=5, text=f"{i['name']}")
            tmp.grid(row=r, column=v)
            if v < 7:
                v += 1
            else:
                r += 1
                v = 0

        self.root.mainloop()
        pass