#coding:utf-8

import tkinter as tk
from tkinter import ttk

#import pub


class Gui(ttk.Notebook):
    def __init__(self, master):
        super().__init__(master)
        note = ttk.Notebook(master)

        # --- fix this logic later
        port_page = Port(note, "Port")
        linetrace_page = Trace(note, "LineTrace")

        array = [port_page, linetrace_page]

        for i in array:
            note.add(i, text=i.ret_name())
        # ---

        note.pack(fill=tk.BOTH, expand=True) 


class Port(tk.Frame):
    def __init__(self, master=None, txt=None):
        super().__init__(master)
        self.name = txt
        
        self.sensor_combobox()
        self.motor_combobox()

    def sensor_combobox(self):
        # 設定ボタン押す -> port1変数へ格納 -> subへ送信 -> 送信情報を元にifでport設定

        y = 0.15
        for i in range(4):
            label = tk.Label(self, text="sensor")
            label.place(relx=0.2, rely=y)

            sensor_port = ttk.Combobox(self, state="readonly",values=["NONE", "Color Sensor", "Jayro Sensor", "Touch Sensor", "Ultrasonc Sensor"])
            sensor_port.place(relx=0.25, rely=y)

            sensor_port.current(0)
            sensor_port.bind("<<ComboboxSelected>>", lambda e: print(sensor_port.get()))
            y += 0.23

    def motor_combobox(self):

        y = 0.15
        for i in range(4):
            label = tk.Label(self, text="motor")
            label.place(relx=0.7, rely=y)

            motor_port = ttk.Combobox(self, state="readonly",values=["NONE", "Medium Motor", "Large Motor"])
            motor_port.place(relx=0.75, rely=y)
            motor_port.current(0)
            y += 0.23

    def ret_name(self):
        return self.name


class Trace(tk.Frame):
    def __init__(self, master=None, txt=None):
        super().__init__(master)
        self.name = txt

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
        filemenu.add_command(label="Exit", command= lambda: exit())

        menubar.add_cascade(label="File", menu=filemenu)
        
        master.config(menu=menubar)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1100x600")
    root.title("EV3 Control System with GUI")

    app = Gui(master=root)
    Menu(root)

    root.mainloop()