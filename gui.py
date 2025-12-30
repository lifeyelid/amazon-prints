from tkinter import *
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
import os


def on_drop(event):
    paths = event.data.split()
    # for path in paths:
    #     filename = os.path.basename(path.strip("{}"))
    #     drop_box.insert(END, filename)
    #     print(f"Dropped file: {filename}")
    for path in paths:
        filename = os.path.basename(path.strip("{}"))
        print(f"Dropped file: {filename}")

app = TkinterDnD.Tk()
app.title("Amazon PDF Uploader")
app.geometry("400x200")

drop_box = Listbox(app, width=50, height=10)
drop_box.pack(pady=20)

drop_box.drop_target_register(DND_FILES)


drop_box.dnd_bind("<<Drop>>", on_drop)

button = Button(app, text="Process Files")
button.pack(pady=10)

app.mainloop()