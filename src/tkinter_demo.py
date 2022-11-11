#!/usr/bin/python3
# Tkinter demo
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


# Standard library
import concurrent.futures
import time
import tkinter
from tkinter import ttk


# Constants
FONT = ("DejaVu Sans", 10, "normal")
START = "Waiting...\n"
PROC = "Processing...\n"
OUTPUT = "Done! Your number:\n\"{}\""


########################################################################
# BACKEND

def call_exec(arg):
    future = executor.submit(func, arg)
    future.add_done_callback(callback)

def func(arg):
    time.sleep(5)
    return arg

def callback(future):
    result = future.result()
    win.stop(result)


########################################################################
# FRONTEND

class MainWindow(tkinter.Tk):
    """Tkinter demo"""

    def __init__(self):
        super().__init__()
        # Window manager
        self.title("* Tkinter demo *")
        self.geometry("+{}+{}".format(self.winfo_screenwidth() // 2 - 133,
                                      self.winfo_screenheight() // 2 - 132))
        self.resizable(False, False)
        # Data
        self.theme = tkinter.StringVar()
        self.theme.trace_add("write",
                             lambda *args: self.set_theme(self.theme.get()))
        self.data = tkinter.StringVar()
        self.data.trace_add("write",
            lambda *args: self.entrylbl.config(foreground="black"))
        # Style
        self.style = ttk.Style()
        # Widgets
        self.mainframe = ttk.Frame(self)
        self.mainframe.pack()
        self.option = ttk.OptionMenu(self.mainframe, self.theme, "default",
                                     *self.style.theme_names())
        self.option.pack(anchor="ne")
        self.frame = ttk.Frame(self.mainframe)
        self.frame.pack(padx=8, pady=8)
        # Input section
        self.inputfrm = ttk.Labelframe(self.frame, text="Input")
        self.inputfrm.pack(pady=4, fill="both")
        self.entrylbl = ttk.Label(self.inputfrm, text="Enter a number:")
        self.entrylbl.pack(side="left")
        self.entryvalid = self.register(
            lambda act, char: act=="0" or char.isdigit())
        self.entry = ttk.Entry(self.inputfrm, textvariable=self.data, width=16,
            validate="key", validatecommand=(self.entryvalid, "%d", "%S"),
            font=FONT)
        self.entry.pack(side="right", padx=4, pady=4)
        # Button
        self.button = ttk.Button(self.frame, text="Start", padding=8,
                                 command=self.start)
        self.button.pack(pady=8)
        # Output section
        self.outputfrm = ttk.Labelframe(self.frame, text="Output")
        self.outputfrm.pack(pady=4, fill="both")
        self.progress = ttk.Progressbar(self.outputfrm, mode="indeterminate")
        self.progress.pack(pady=4, fill="both")
        self.outputlbl = ttk.Label(self.outputfrm, text=START, padding=8,
                                   anchor="center", justify="center",
                                   relief="solid")
        self.outputlbl.pack(fill="both")

    def set_theme(self, theme):
        self.style.theme_use(theme)
        ## compatability
        self.style.configure("TLabelframe.Label", font=FONT)
        self.style.configure("TLabel", font=FONT)
        ##
        self.style.configure("TButton", font=("DejaVu Sans", 12, "bold"))

    def start(self):
        if self.data.get():
            self.button.config(state="disabled")
            self.entry.config(state="disabled")
            self.progress.start()
            self.outputlbl.config(text=PROC, font=FONT)
            # Call executor
            call_exec(self.data.get())
        else:
            self.entrylbl.config(foreground="red")
            self.outputlbl.config(text=START, font=FONT)

    def stop(self, output):
        self.progress.stop()
        self.outputlbl.config(text=OUTPUT.format(output),
                              font=("DejaVu Sans", 10, "bold"))
        self.data.set("")
        self.entry.config(state="normal")
        self.button.config(state="normal")


########################################################################
# EXECUTION

if __name__ == "__main__":
    executor = concurrent.futures.ThreadPoolExecutor()
    win = MainWindow()
    win.mainloop()
    executor.shutdown()

