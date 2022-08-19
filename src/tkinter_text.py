#!/usr/bin/python3
# Tkinter
# Text demo
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


import tkinter
from tkinter import ttk


FONT_NORM = ("DejaVu Sans", 10, "normal")
FONT_BOLD = ("DejaVu Sans", 10, "bold")
TEXT = tkinter.__doc__


class TextDemo(tkinter.Tk):
    
    def __init__(self):
        super().__init__()
        # Window manager
        self.title("* Text demo *")
        self.geometry("+{}+{}".format(self.winfo_screenwidth() // 2 - 298,
                                      self.winfo_screenheight() // 2 - 199))
        self.resizable(False, False)
        # Data
        self.tag = tkinter.StringVar()
        self.tag.trace_add("write", self.format)
        # Style
        self.style = ttk.Style()
        self.style.theme_use("default")
        ## compatability
        self.config(bg=self.style.lookup("TFrame", "background"))
        self.style.configure("TButton", font=FONT_NORM)
        self.style.configure("TLabel", font=FONT_NORM)
        ##
        self.style.configure("B.TButton", font=FONT_BOLD)
        self.style.configure("I.TButton", font=("DejaVu Sans", 10,
                                                "bold italic"))
        self.style.configure("Fg.TButton", font=FONT_BOLD, foreground="red")
        self.style.configure("Bg.TButton", font=FONT_BOLD, background="yellow")
        # Widgets
        self.frame = ttk.Frame(self)
        self.frame.pack(padx=8, pady=8)
        # Buttons
        self.btnframe = ttk.Frame(self.frame)
        self.btnframe.pack(pady=4, fill="both")
        self.insertbtn = ttk.Button(self.btnframe, text="Insert",
                                    command=self.insert)
        self.insertbtn.pack(side="left")
        self.deletebtn = ttk.Button(self.btnframe, text="Delete",
                                    command=self.delete, state="disabled")
        self.deletebtn.pack(side="left", padx=8)
        self.label = ttk.Label(self.btnframe, text="Formatting:")
        self.label.pack(side="left", padx=4)
        self.boldbtn = ttk.Button(self.btnframe, text="B", width=2,
            style="B.TButton", command=lambda *e: self.tag.set("bold"))
        self.boldbtn.pack(side="left")
        self.italicbtn = ttk.Button(self.btnframe, text="I", width=2,
            style="I.TButton", command=lambda *e: self.tag.set("italic"))
        self.italicbtn.pack(side="left", padx=4)
        self.fgbtn = ttk.Button(self.btnframe, text="A", width=2,
            style="Fg.TButton", command=lambda *e: self.tag.set("fg"))
        self.fgbtn.pack(side="left")
        self.bgbtn = ttk.Button(self.btnframe, text="A", width=2,
            style="Bg.TButton", command=lambda *e: self.tag.set("bg"))
        self.bgbtn.pack(side="left", padx=4)
        self.unformatbtn = ttk.Button(self.btnframe, text="\u274C", width=2,
            command=self.unformat)
        self.unformatbtn.pack(side="left")
        # Text
        self.scrollfrm = ttk.Frame(self.frame)
        self.scrollfrm.pack(fill="both")
        self.text = tkinter.Text(self.scrollfrm, width=70, height=20,
                                 font=("DejaVu Sans Mono", 10, "normal"))
        self.text.tag_config("bold", font=("DejaVu Sans Mono", 10, "bold"))
        self.text.tag_config("italic", font=("DejaVu Sans Mono", 10, "italic"))
        self.text.tag_config("fg", foreground="red")
        self.text.tag_config("bg", background="yellow")        
        self.text.pack(side="left", fill="both", expand=True)
        self.scroll = ttk.Scrollbar(self.scrollfrm)
        self.scroll.pack(side="right", fill="y")
        self.text.config(yscrollcommand=self.scroll.set)
        self.scroll.config(command=self.text.yview)

    def insert(self):
        self.text.insert("1.0", TEXT)
        self.deletebtn.config(state="normal")
        self.insertbtn.config(state="disabled")

    def delete(self):
        self.text.delete("1.0", "end")
        self.insertbtn.config(state="normal")
        self.deletebtn.config(state="disabled")

    def format(self, *args):
        try:
            if self.tag.get() not in self.text.tag_names("sel.first"):
                self.text.tag_add(self.tag.get(), "sel.first", "sel.last")
            else:
                self.text.tag_remove(self.tag.get(), "sel.first", "sel.last")
        except Exception:
            pass

    def unformat(self):
        for tag in self.text.tag_names()[1:]:
            self.text.tag_remove(tag, "1.0", "end")
        


if __name__ == "__main__":
    demo = TextDemo()
    demo.mainloop()

