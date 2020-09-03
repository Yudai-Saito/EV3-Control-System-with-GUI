#coding:utf-8

import app
import tkinter as tk

if __name__ == "__main__":
    
    root = tk.Tk()
    root.geometry("1100x600")
    
    root.title("EV3 Control System with GUI")

    root = app.Home(master=root)
    
    root.mainloop()