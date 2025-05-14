import pathlib
import random
import appdirs
import shelve

import tkinter
from tkinter import ttk
import tkinter.filedialog

user_data_dir = pathlib.Path(appdirs.user_data_dir('FileRandomizer', 'Vebyast'))
user_data_dir.mkdir(parents=True, exist_ok=True)


def build_app(root, user_data_shelve):
    root.title("File Randomizer")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    selected_dir = tkinter.StringVar()
    selected_file = tkinter.StringVar()

    selected_dir.set(user_data_shelve['target_directory'])

    def select_dir_callback():
        user_data_shelve['target_directory'] = tkinter.filedialog.askdirectory(mustexist=True)
        selected_dir.set(user_data_shelve['target_directory'])

    def pick_file_callback():
        d = pathlib.Path(user_data_shelve['target_directory'])
        files = [p for p in d.iterdir() if p.is_file()]
        user_data_shelve['picked_file'] = random.choice(files).name
        selected_file.set(user_data_shelve['picked_file'])

    ttk.Label(mainframe, textvariable=selected_dir).grid(column=2, row=1, sticky=(tkinter.W, tkinter.E))
    ttk.Label(mainframe, textvariable=selected_file).grid(column=2, row=2, sticky=(tkinter.W, tkinter.E))
    ttk.Button(mainframe, text="Select Directory", command=select_dir_callback).grid(column=1, row=1, sticky=(tkinter.W, tkinter.E))
    ttk.Button(mainframe, text="Pick Random File", command=pick_file_callback).grid(column=1, row=2, sticky=(tkinter.W, tkinter.E))

def main():

    root = tkinter.Tk()
    
    with shelve.open(user_data_dir / 'settings') as user_data_shelve:
        build_app(root, user_data_shelve)
        root.mainloop()        


if __name__ == "__main__":
    main()
