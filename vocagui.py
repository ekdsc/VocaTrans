import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import sys
import vocatrans

root = tk.Tk()


root.title("VocaTrans!")
root.minsize(400,300)
file_location = tk.StringVar(value="song.vpr")
bad_file = ""

def file_open():
    file_path = tk.filedialog.askopenfilename()
    if file_path:
        if (file_path.endswith(".vpr")):
            file_location.set(file_path)
            bad_file = ""
        else:
            bad_file = "Bad file!"

def translate():
    sys.argv = ['vocatrans.py', file_location.get()]
    vocatrans.main()

menu = [
    tk.Label(root, text="Converts .VPR files from English to Japanese using the table in phoneme.csv"),
    ttk.Button(root, text="Select .VPR to translate", command=file_open),
    ttk.Entry(root, textvariable=file_location),
    tk.Label(root, text=bad_file),
    ttk.Button(root, text="Translate!", command=translate),
    tk.Label(root, text="Version 0.2", height=10, pady=10)
]

for widget in menu:
    widget.pack(padx=5, pady=5, fill="x")

if bad_file == 1:
        tk.Label(root, text="Not a .VPR file!").pack()
else:
    pass

root.mainloop()