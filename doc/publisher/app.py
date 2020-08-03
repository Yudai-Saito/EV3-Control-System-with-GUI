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
    sensor_pic_path = { "none" : "../../pic/none.jpg", 
                        "color" : "../../pic/color_sensor.jpg", 
                        "jayro" : "../../pic/jayro_sensor.jpg", 
                        "touch" : "../../pic/touch_sensor.jpg", 
                        "ultrasonic" : "../../pic/ultrasonic_sensor.jpg"
                        }

    def __init__(self, master=None, txt=None):
        super().__init__(master)
        self.name = txt
        
        self.sensor_combobox()
        self.motor_combobox()

    def sensor_combobox(self):

        sensor_port_name = ["1", "2", "3", "4"]

        py = 0.1
        by = 0.1
        for i in sensor_port_name:
            #port num txt
            label = tk.Label(self, text=i, relief="groove", font=("", 15, "bold"))
            label.place(relx=0.04, rely=by, relwidth=0.03, relheight=0.05)

            #mode txt
            label = tk.Label(self, text="mode")
            label.place(relx=0.2, rely=by+0.07)

            #mode combobox
            sensor_mode = ttk.Combobox(self, state="readonly",values="NONE")
            sensor_mode.place(relx=0.25, rely=by+0.07)
            sensor_mode.current(0)

            #picture
            sensor_img = Image.open(pathlib.Path(self.sensor_pic_path["none"]))
            sensor_img = sensor_img.resize((100,100))
            sensor_img = ImageTk.PhotoImage(sensor_img)

            sensor_img_lbl = tk.Label(self, image=sensor_img)
            sensor_img_lbl.photo = sensor_img
            sensor_img_lbl.place(relx=0.09, rely=py)

            #name txt
            label = tk.Label(self, text="sensor")
            label.place(relx=0.2, rely=by)

            #combobox
            sensor_port = ttk.Combobox(self, state="readonly",values=["NONE", "Color Sensor", "Jayro Sensor", "Touch Sensor", "Ultrasonc Sensor"])
            sensor_port.place(relx=0.25, rely=by)
            sensor_port.current(0)
            sensor_port.bind("<<ComboboxSelected>>", (lambda e,x = 0.09, y = py, dest_sensor=sensor_img_lbl, sensor_port=sensor_port, sensor_mode = sensor_mode: self.sensor_pic_change(x, y, dest_sensor, sensor_port.get(), sensor_mode)))

            py += 0.23
            by += 0.23

    def sensor_pic_change(self, x, y, dest_sensor, sensor_type, sensor_mode):

        if sensor_type == "NONE":
            sensor_type = "none"
            mode = ["NONE"]
        elif sensor_type == "Color Sensor":
            sensor_type = "color"
            mode = ["REFLECT", "AMBIENT", "COLOR", "REF-RAW", "RGB-RAW"]
        elif sensor_type == "Jayro Sensor":
            sensor_type = "jayro"
            mode = ["ANGLE", "RATE", "FAS", "G&A", "CAL"]
        elif sensor_type == "Touch Sensor":
            sensor_type = "touch"
            mode = ["TOUCH"]
        elif sensor_type == "Ultrasonc Sensor":
            sensor_type = "ultrasonic"
            mode = ["DIST-CM", "DIST-IN", "LISTEN", "SI-CM", "SI-IN"]

        sensor_mode.configure(values=mode)
        sensor_mode.current(0)
        
        dest_sensor.destroy()

        sensor_img = Image.open(pathlib.Path(self.sensor_pic_path[sensor_type]))
        sensor_img = sensor_img.resize((100,100))
        sensor_img = ImageTk.PhotoImage(sensor_img)

        sensor_img_lbl = tk.Label(self, image=sensor_img)
        sensor_img_lbl.photo = sensor_img
        sensor_img_lbl.place(relx=x, rely=y)

    def motor_combobox(self):

        motor_pic_path = { "none" : "../../pic/none.jpg", 
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