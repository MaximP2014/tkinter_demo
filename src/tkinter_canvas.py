#!/usr/bin/python3
# Tkinter
# Canvas demo
#
#
# Copyright (C) 2022 Maksim Petrenko
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import random
import tkinter
from tkinter import ttk


COLORS = ["red", "orange", "yellow",
          "green", "brown", "light blue",
          "dark blue", "purple", "white"]
COORDINATES = [(4, 4, 104, 104), (112, 4, 212, 104), (220, 4, 320, 104),
               (4, 112, 104, 212), (112, 112, 212, 212), (220, 112, 320, 212),
               (4, 220, 104, 320), (112, 220, 212, 320), (220, 220, 320, 320)]


class CanvasDemo(tkinter.Tk):
    
    def __init__(self):
        super().__init__()
        # Window manager
        self.title("* Canvas demo *")
        self.geometry("+{}+{}".format(self.winfo_screenwidth() // 2 - 194,
                                      self.winfo_screenheight() // 2 - 171))
        self.resizable(False, False)
        # Data
        self.count = tkinter.IntVar(value=9)
        self.count.trace_add("write", self.is_free)
        self.coords = COORDINATES.copy()
        self.colors = COLORS.copy()
        # Style
        self.style = ttk.Style()
        self.style.theme_use("default")
        ## compatability
        self.config(bg=self.style.lookup("TFrame", "background"))
        self.style.configure("TButton", font=("DejaVu Sans", 16, "normal"),
                             width=2)
        # Widgets
        self.frame = ttk.Frame(self)
        self.frame.pack(padx=8, pady=8)
        # Canvas
        self.canvas = tkinter.Canvas(self.frame, width=324, height=324,
                                     bg="black")
        self.canvas.pack(side="left")
        # Buttons
        self.btnframe = ttk.Frame(self.frame)
        self.btnframe.pack(side="right", padx=4, anchor="n")
        self.rectbtn = ttk.Button(self.btnframe, text="\u25A0",
                                  command=self.rectangle)
        self.rectbtn.pack()
        self.ovalbtn = ttk.Button(self.btnframe, text="\u2B24",
                                  command=self.oval)
        self.ovalbtn.pack(pady=8)
        self.polybtn = ttk.Button(self.btnframe, text="\u25B2",
                                  command=self.polygon)
        self.polybtn.pack()
        self.cleanbtn = ttk.Button(self.btnframe, text="\u274C",
                                   command=self.clean)
        self.cleanbtn.pack(pady=8)

    def is_free(self, *args):
        if self.count.get() == 0:
            self.rectbtn.config(state="disabled")
            self.ovalbtn.config(state="disabled")
            self.polybtn.config(state="disabled")

    def rectangle(self):
        self.count.set(self.count.get()-1)
        coords = self.coords.pop(random.randint(0, len(self.coords)-1))
        color = self.colors.pop(random.randint(0, len(self.colors)-1))
        self.canvas.create_rectangle(coords, fill=color)

    def oval(self):
        self.count.set(self.count.get()-1)
        coords = self.coords.pop(random.randint(0, len(self.coords)-1))
        color = self.colors.pop(random.randint(0, len(self.colors)-1))
        self.canvas.create_oval(coords, fill=color)

    def polygon(self):
        self.count.set(self.count.get()-1)
        x1, y1, xn, yn = self.coords.pop(random.randint(0, len(self.coords)-1))
        coords = x1, yn-7, x1+50, y1+7, xn, yn-7
        color = self.colors.pop(random.randint(0, len(self.colors)-1))
        self.canvas.create_polygon(coords, fill=color)

    def clean(self):
        self.canvas.delete(*self.canvas.find_all())
        self.coords = COORDINATES.copy()
        self.colors = COLORS.copy()
        self.count.set(9)
        self.rectbtn.config(state="normal")
        self.ovalbtn.config(state="normal")
        self.polybtn.config(state="normal")



if __name__ == "__main__":
    demo = CanvasDemo()
    demo.mainloop()

