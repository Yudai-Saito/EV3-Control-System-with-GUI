#coding:utf-8

import tkinter as tk
from tkinter import ttk

import pathlib
from PIL import Image, ImageTk

import pub

class Home(tk.Menu, ttk.Notebook):
    flag = True
    ip = "192.168.0.1"

    def __init__(self, master):
        super().__init__(master)
        self.create_note(master)
        self.create_menu(master)
        
    def create_note(self, master):
        note = ttk.Notebook(master)

        notes = [Port(note, "Port")]

        for i in notes:
            note.add(i, text=i.ret_name())

        note.bind("<Any-KeyPress>", self.callkey)
        note.bind("<Any-KeyRelease>", self.back)
        note.bind("<<NotebookTabChanged>>", self.note_stat)

        note.pack(fill=tk.BOTH, expand=True) 
        note.focus_set()

    def create_menu(self, master):
        menubar = tk.Menu(master)
        
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="IP Setting", command = lambda app = master: self.ip_set(app))
        filemenu.add_command(label="Exit", command = lambda: exit())

        menubar.add_cascade(label="File", menu=filemenu)
        
        master.config(menu=menubar)

    def ip_set(self, app):
        newWindow = tk.Toplevel(app)
        newWindow.title("modal dialog")
        newWindow.geometry("300x100")

        label = tk.Entry(newWindow, relief="groove", font=("", 15, "bold"), justify="center")
        label.insert(0, Home.ip)
        label.pack()

        button = tk.Button(newWindow, text="SET")
        button.configure(command=lambda label = label, window = newWindow : self.get_ip(label, window))
        button.pack()

    def get_ip(self, label, window):
        Home.ip = label.get()
        window.destroy()

    def note_stat(self, event):
        note = event.widget

        if note.tab(note.select(), "text") == "Port":
            Home.flag = True
        else:
            Home.flag = False

    def callkey(self, event):
        if Home.flag == True:
            if event.keysym == "w" or event.keysym == "a" or event.keysym == "s" or event.keysym == "d" or event.keysym == "q" or event.keysym == "e" or event.keysym == "r" or event.keysym == "f" or event.keysym == "t" or event.keysym == "g":
                pub.key_event(event.keysym, "press")

    def back(self, event):
        if Home.flag == True:
            if event.keysym == "w" or event.keysym == "a" or event.keysym == "s" or event.keysym == "d" or event.keysym == "q" or event.keysym == "e" or event.keysym == "r" or event.keysym == "f" or event.keysym == "t" or event.keysym == "g":
                pub.key_event(event.keysym, "release")


class Port(tk.Frame):
    sensor_pic_path = { "none" : "../../pic/none.jpg", 
                        "color" : "../../pic/color_sensor.jpg", 
                        "gyro" : "../../pic/gyro_sensor.jpg", 
                        "touch" : "../../pic/touch_sensor.jpg", 
                        "ultrasonic" : "../../pic/ultrasonic_sensor.jpg"
                        }

    sensor_comboboxes = []
    sensor_mode_comboboxes = []
    sensor_text_labels = []

    motor_comboboxes = []
    motor_mode_comboboxes = []
    motor_text_labels = []
    motor_check = []

    connect_button = None
    origin_color = None
    chk = None
    
    motor_power = 50

    def __init__(self, master=None, txt=None):
        super().__init__(master)
        self.name = txt
        
        self.sensor_combobox()
        self.motor_combobox()
        self.button()

    def button(self):
        Port.connect_button = tk.Button(self, text="CONNECT")
        Port.connect_button.configure(command=lambda : pub.connect())
        Port.connect_button.place(relx=0.1, rely=0.02)

        Port.origin_color = Port.connect_button.cget("background")

        button = ttk.Button(self, text="SET", command=lambda : pub.set_port(self.sensor_comboboxes, self.sensor_mode_comboboxes, self.motor_comboboxes, self.motor_mode_comboboxes))
        button.place(relx=0.2, rely=0.02)

        Port.chk = tk.BooleanVar()
        chk = tk.Checkbutton(self, text="minus", variable=Port.chk)
        chk.place(relx=0.5, rely=0.02)

        #power display
        label = tk.Entry(self, relief="groove", font=("", 15, "bold"), justify="center")
        label.insert(0, Port.motor_power)
        label.configure(state="readonly")
        label.place(relx=0.58, rely=0.02, relwidth=0.07, relheight=0.05)

        #+10 button
        plus_button = tk.Button(self, text="+10", font=("", 15))
        plus_button.configure(command=lambda poewerbox = label : self.increment(10, poewerbox))
        plus_button.place(relx=0.66, rely=0.02, relwidth=0.05, relheight=0.05)

        #+1 button
        plus_button = tk.Button(self, text="+1", font=("", 15))
        plus_button.configure(command=lambda poewerbox = label : self.increment(1, poewerbox))
        plus_button.place(relx=0.71, rely=0.02, relwidth=0.05, relheight=0.05)

        #-1 button
        minus_button = tk.Button(self, text="-1", font=("", 15))
        minus_button.configure(command=lambda poewerbox = label : self.increment(-1, poewerbox))
        minus_button.place(relx=0.76, rely=0.02, relwidth=0.05, relheight=0.05)

        #-10 button
        minus_button = tk.Button(self, text="-10", font=("", 15))
        minus_button.configure(command=lambda poewerbox = label : self.increment(-10, poewerbox))
        minus_button.place(relx=0.81, rely=0.02, relwidth=0.05, relheight=0.05)


    def increment(self, power, poewerbox):
        Port.motor_power += power

        if Port.motor_power > 100:
            Port.motor_power = 100
        elif Port.motor_power < 0:
            Port.motor_power = 0
        
        poewerbox.configure(state="normal")
        poewerbox.delete(0, tk.END)
        poewerbox.insert(0, Port.motor_power)
        poewerbox.configure(state="readonly")


    def sensor_combobox(self):

        sensor_port_name = ["1", "2", "3", "4"]

        array_count = 0
        y = 0.1
        for i in sensor_port_name:
            #port num txt
            label = tk.Label(self, text=i, relief="groove", font=("", 15, "bold"))
            label.place(relx=0.04, rely=y, relwidth=0.03, relheight=0.05)

            #port value
            Port.sensor_text_labels.append(tk.Label(self, relief="sunken", font=("", 15, "bold")))
            Port.sensor_text_labels[array_count].place(relx=0.25, rely=y+0.12, relwidth=0.16, relheight=0.07)

            #mode txt
            label = tk.Label(self, text="mode")
            label.place(relx=0.2, rely=y+0.07)

            #mode combobox
            self.sensor_mode_comboboxes.append(ttk.Combobox(self, state="readonly",values="NONE"))
            self.sensor_mode_comboboxes[array_count].place(relx=0.25, rely=y+0.07)
            self.sensor_mode_comboboxes[array_count].current(0)

            #picture
            sensor_img = Image.open(pathlib.Path(self.sensor_pic_path["none"]))
            sensor_img = sensor_img.resize((100,100))
            sensor_img = ImageTk.PhotoImage(sensor_img)

            sensor_img_lbl = tk.Label(self, image=sensor_img)
            sensor_img_lbl.photo = sensor_img
            sensor_img_lbl.place(relx=0.09, rely=y)

            #name txt
            label = tk.Label(self, text="sensor")
            label.place(relx=0.2, rely=y)

            #combobox
            self.sensor_comboboxes.append(ttk.Combobox(self, state="readonly",values=["NONE", "Color Sensor", "Gyro Sensor", "Touch Sensor", "Ultrasonc Sensor"]))
            self.sensor_comboboxes[array_count].place(relx=0.25, rely=y)
            self.sensor_comboboxes[array_count].current(0)
            self.sensor_comboboxes[array_count].bind("<<ComboboxSelected>>", (lambda e,x = 0.09, y = y, dest_sensor=sensor_img_lbl, sensor_port=self.sensor_comboboxes[array_count], sensor_mode = self.sensor_mode_comboboxes[array_count]: self.sensor_pic_change(x, y, dest_sensor, sensor_port.get(), sensor_mode)))

            array_count += 1
            y += 0.23


    def sensor_pic_change(self, x, y, dest_sensor, sensor_type, sensor_mode):

        if sensor_type == "NONE":
            sensor_type = "none"
            mode = ["NONE"]
        elif sensor_type == "Color Sensor":
            sensor_type = "color"
            mode = ["REFLECT", "AMBIENT", "COLOR", "REF-RAW", "RGB-RAW"]
        elif sensor_type == "Gyro Sensor":
            sensor_type = "gyro"
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

    motor_pic_path = { "none" : "../../pic/none.jpg", 
                        "large" : "../../pic/large_motor.jpg", 
                        "midium" : "../../pic/medium_motor.jpg"
                        }

    def motor_combobox(self):

        sensor_port_name = ["A", "B", "C", "D"]

        array_count = 0
        y = 0.1
        for i in sensor_port_name:
            #port name txt
            label = tk.Label(self, text=i, relief="groove", font=("", 15, "bold"))
            label.place(relx=0.54, rely=y, relwidth=0.03, relheight=0.05)

            #checkbox
            Port.motor_check.append(tk.BooleanVar())
            chk = tk.Checkbutton(self, variable=Port.motor_check[array_count])
            chk.place(relx=0.54, rely=y + 0.05)

            #port value
            Port.motor_text_labels.append(tk.Label(self, relief="sunken", font=("", 15, "bold")))
            Port.motor_text_labels[array_count].place(relx=0.75, rely=y+0.12, relwidth=0.16, relheight=0.07)
            
            #mode txt
            label = tk.Label(self, text="mode")
            label.place(relx=0.7, rely=y+0.07)
            
            #name txt
            label = tk.Label(self, text="motor")
            label.place(relx=0.7, rely=y)

            #mode combobox
            self.motor_mode_comboboxes.append(ttk.Combobox(self, state="readonly",values="NONE"))
            self.motor_mode_comboboxes[array_count].place(relx=0.75, rely=y+0.07)
            self.motor_mode_comboboxes[array_count].current(0)

            #picture
            motor_img = Image.open(pathlib.Path(self.motor_pic_path["none"]))
            motor_img = motor_img.resize((100,100))
            motor_img = ImageTk.PhotoImage(motor_img)

            motor_img_lbl = tk.Label(self, image=motor_img)
            motor_img_lbl.photo = motor_img
            motor_img_lbl.place(relx=0.6, rely=y)

            #name txt
            label = tk.Label(self, text="motor")
            label.place(relx=0.7, rely=y)


            self.motor_comboboxes.append(ttk.Combobox(self, state="readonly",values=["NONE", "Medium Motor", "Large Motor"]))
            self.motor_comboboxes[array_count].place(relx=0.75, rely=y)
            self.motor_comboboxes[array_count].current(0)
            self.motor_comboboxes[array_count].bind("<<ComboboxSelected>>", (lambda e,x = 0.6, y = y, dest_motor=motor_img_lbl, motor_port=self.motor_comboboxes[array_count]: self.motor_pic_change(x, y, dest_motor, motor_port.get())))

            array_count += 1
            y += 0.23

    def motor_pic_change(self, x, y, dest_motor, motor_type):

        if motor_type == "NONE":
            motor_type = "none"
            mode = ["NONE"]
        elif motor_type == "Medium Motor":
            motor_type = "midium"
        elif motor_type == "Large Motor":
            motor_type = "large"

        dest_motor.destroy()

        motor_img = Image.open(pathlib.Path(self.motor_pic_path[motor_type]))
        motor_img = motor_img.resize((100,100))
        motor_img = ImageTk.PhotoImage(motor_img)

        motor_img_lbl = tk.Label(self, image=motor_img)
        motor_img_lbl.photo = motor_img
        motor_img_lbl.place(relx=x, rely=y)

    def ret_name(self):
        return self.name
