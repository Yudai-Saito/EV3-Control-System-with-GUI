#coding:utf-8

import json
import threading
from tkinter import messagebox
import paho.mqtt.client as mqtt

client = mqtt.Client()

port_stat = { "port1" : ["none", "none"], 
                "port2" : ["none", "none"],
                "port3" : ["none", "none"],
                "port4" : ["none", "none"],
                "portA" : ["none", "none"],
                "portB" : ["none", "none"], 
                "portC" : ["none", "none"],
                "portD" : ["none", "none"]
}

#接続時のフラグと切断時のフラグ管理が必要。 未接続の場合にボタンを押した場合のエラーを防ぐ。

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

def set_port(sensor_port, sensor_mode, motor_port, motor_mode):

    client.publish("test", "set_port")

    port_info = sensor_port + motor_port
    port_mode = sensor_mode + motor_mode
    
    for key, port, mode in zip(port_stat, port_info, port_mode):
        port_stat[key][0] = port.get()
        port_stat[key][1] = mode.get()
    
    port_stat_json = json.dumps(port_stat)

    client.publish("test", port_stat_json)
    
    #client.publish("topic/motor/dt", port_stat_json)

def connect(button):

    connect_th = threading.Thread(target=connect_t, args=(button,))
    connect_th.setDaemon(True)
    connect_th.start()