#coding:utf-8

import tkinter as tk
from tkinter import ttk

#import pub


class Gui(ttk.Notebook):
    def __init__(self, master):
        super().__init__(master)
        note = ttk.Notebook(master)

        port_page = Port(note, "Port")
        linetrace_page = Trace(note, "LineTrace")

        array = [port_page, linetrace_page]

        for i in array:
            note.add(i, text=i.ret_name())

        note.pack(fill=tk.BOTH, expand=True) 


class Port(tk.Frame):
    def __init__(self, master=None, txt=None):
        super().__init__(master)
        self.name = txt
        page = tk.Frame(master)
        self.widget(txt)

    def widget(self, txt):
        label = tk.Label(self, text=txt, font=("", 30))
        label.pack()
    
    def ret_name(self):
        return self.name


class Trace(tk.Frame):
    def __init__(self, master=None, txt=None):
        super().__init__(master)
        self.name = txt
        page = tk.Frame(master)
        self.widget(txt)

    def widget(self, txt):
        label = tk.Label(self, text=txt, font=("", 30))
        label.pack()
    
    def ret_name(self):
        return self.name


class Menu(tk.Menu):
    def __init__(self, master):
        super().__init__(master)
        self.create_menu(master)

    def create_menu(self, master):
        menubar = tk.Menu(master)
        
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open")
        filemenu.add_command(label="Save")
        filemenu.add_command(label="Exit")
        
        menubar.add_cascade(label="File", menu=filemenu)
        
        master.config(menu=menubar)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1100x600")
    root.title("EV3 Control System with GUI")

    app = Gui(master=root)
    Menu(root)

    root.mainloop()