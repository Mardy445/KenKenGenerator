import tkinter as tk

"""
This file contains a custom Tkinter Frame for KenKen display purposes
"""


class TileFrame(tk.Frame):
    possibilities_list = []

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
        self.l2 = tk.Label(self, text=number, bg="white", fg="blue", anchor="center", width=10, height=3)
        self.l3 = tk.Label(self, text="", bg="white", fg="red", anchor="w", width=10, height=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=1)

        self.l1.grid(row=0, column=0, padx=(0, east), sticky="nw")
        self.l2.grid(row=1, column=0, padx=(0, east), sticky="nw")
        self.l3.grid(row=2, column=0, padx=(0, east), pady=(0, south), sticky="nw")

    def position_in_grid(self, r, c):
        self.grid(row=r, column=c)

    def focus(self):
        self.l1["bg"] = "grey"
        self.l2["bg"] = "grey"
        self.l3["bg"] = "grey"

    def unfocus(self):
        self.l1["bg"] = "white"
        self.l2["bg"] = "white"
        self.l3["bg"] = "white"

    def set_number(self,number):
        self.l2["text"] = number

    def add_number_to_possibilities_list(self, number):
        if number not in self.possibilities_list:
            self.possibilities_list.append(number)
            string = ""
            for n in self.possibilities_list:
                string = string + ("" if string == "" else ",") + n
            self.l3["text"] = string

    def clear_possibilities_list(self):
        self.possibilities_list = []
        self.l3["text"] = ""

    def reset(self):
        self.clear_possibilities_list()
        self.l2["text"] = ""
