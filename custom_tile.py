import tkinter as tk

"""
This file contains a custom Tkinter Frame for KenKen display purposes
"""


class TileFrame(tk.Frame):
    def __init__(self, root, border_code, value_sign="", number=""):
        tk.Frame.__init__(self, root)
        self["bg"] = "black"
        self.border_code = border_code

        east = 0
        south = 0
        if "e" in self.border_code:
            east = 3
        if "s" in self.border_code:
            south = 3

        self.l1 = tk.Label(self, text=value_sign, bg="white", anchor="nw", width=10, height=1)
        self.l2 = tk.Label(self, text=number, bg="white", anchor="center", width=10, height=4)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)

        self.l1.grid(row=0, column=0, padx=(0, east), sticky="nw")
        self.l2.grid(row=1, column=0, padx=(0, east), pady=(0, south), sticky="nw")

    def position_in_grid(self, r, c):
        self.grid(row=r, column=c)
