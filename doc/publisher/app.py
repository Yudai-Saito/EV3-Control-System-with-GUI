#coding:utf-8

import tkinter as tk
from tkinter import ttk

import pathlib
from PIL import Image, ImageTk

#import pub

class Home(tk.Menu, ttk.Notebook):
    def __init__(self, master):
        super().__init__(master)
        self.create_note(master)
        self.create_menu(master)
        
        
    def create_note(self, master):
        note = ttk.Notebook(master)

        notes = [Port(note, "Port"), Trace(note, "LineTrace")]

        for i in notes:
            note.add(i, text=i.ret_name())


        note.pack(fill=tk.BOTH, expand=True) 

    def create_menu(self, master):
        menubar = tk.Menu(master)
        
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command= lambda: exit())

        menubar.add_cascade(label="File", menu=filemenu)
        
        master.config(menu=menubar)


class Port(tk.Frame):
    def __init__(self, master=None, txt=None):
        super().__init__(master)
        self.name = txt
        
        self.sensor_combobox()
        self.motor_combobox()

    def sensor_combobox(self):

        sensor_pic_path = { "none" : "../../pic/none.png", 
                            "color" : "../../pic/color_sensor.jpg", 
                            "jayro" : "../../pic/jayro_sensor.jpg", 
                            "touch" : "../../pic/touch_sensor.jpg", 
                            "ultrasonic" : "../../pic/ultrasonic_sensor.jpg"
                            }
        # 設定ボタン押す -> port1変数へ格納 -> subへ送信 -> 送信情報を元にifでport設定
        sensor_port_name = ["1", "2", "3", "4"]

        y = 0.15
        for i in sensor_port_name:
            label = tk.Label(self, text=i, relief="groove", font=("", 15, "bold"))
            label.place(relx=0.04, rely=y-0.1, relwidth=0.03, relheight=0.05)

            label = tk.Label(self, text="mode")
            label.place(relx=0.2, rely=y+0.07)

            label = tk.Label(self, text="sensor")
            label.place(relx=0.2, rely=y)

            sensor_port = ttk.Combobox(self, state="readonly",values=["NONE", "Color Sensor", "Jayro Sensor", "Touch Sensor", "Ultrasonc Sensor"])
            sensor_port.place(relx=0.25, rely=y)
            sensor_port.current(0)
            sensor_port.bind("<<ComboboxSelected>>", (lambda e, sensor_port=sensor_port: print(sensor_port.get())))

            y += 0.23
            

        y = 0.1
        for i in range(4):

            sensor_img = Image.open(pathlib.Path(sensor_pic_path["none"]))
            sensor_img = sensor_img.resize((100,100))
            sensor_img = ImageTk.PhotoImage(sensor_img)

            sensor_img_lbl = tk.Label(self, image=sensor_img)
            sensor_img_lbl.photo = sensor_img
            sensor_img_lbl.place(relx=0.09, rely=y)

            y += 0.23

    def motor_combobox(self):

        motor_pic_path = { "none" : "../../pic/none.png", 
                            "large" : "../../pic/large_motor.jpg", 
                            "midium" : "../../midium_motor.jpg"
                            }

        sensor_port_name = ["A", "B", "C", "D"]

        y = 0.15
        for i in sensor_port_name:
            label = tk.Label(self, text=i, relief="groove", font=("", 15, "bold"))
            label.place(relx=0.54, rely=y-0.1, relwidth=0.03, relheight=0.05)

            label = tk.Label(self, text="motor")
            label.place(relx=0.7, rely=y)

            motor_port = ttk.Combobox(self, state="readonly",values=["NONE", "Medium Motor", "Large Motor"])
            motor_port.place(relx=0.75, rely=y)
            motor_port.current(0)
            motor_port.bind("<<ComboboxSelected>>", (lambda e, motor_port=motor_port: print(motor_port.get())))

            y += 0.23

        y = 0.1
        for i in range(4):

            sensor_img = Image.open(pathlib.Path(motor_pic_path["none"]))
            sensor_img = sensor_img.resize((100,100))
            sensor_img = ImageTk.PhotoImage(sensor_img)

            sensor_img_lbl = tk.Label(self, image=sensor_img)
            sensor_img_lbl.photo = sensor_img
            sensor_img_lbl.place(relx=0.6, rely=y)

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


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1100x600")
    root.title("EV3 Control System with GUI")

    app = Home(master=root)

    root.mainloop()