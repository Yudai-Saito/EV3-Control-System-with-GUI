#coding:utf-8

import threading
from tkinter import messagebox
import paho.mqtt.client as mqtt

client = mqtt.Client()

def connect_t(button):
    
    button.configure(state="disable")
    
    try:
        #IPは選択できるように後改変。
        client.connect("192.168.0.1",1883,60)

        button.configure(bg="#94FF33")

        messagebox.showinfo("notice", "Connection complete.")

        client.loop_forever()
    except:
        button.configure(state="normal")
        
        messagebox.showinfo("notice", "Connection timeout.")

def set_port(port_info):

    client.publish("topic/motor/dt", str(0) + "," + str(0))

def connect(button):

    connect_th = threading.Thread(target=connect_t, args=(button,))
    connect_th.setDaemon(True)
    connect_th.start()