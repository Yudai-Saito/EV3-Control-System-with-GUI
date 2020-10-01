#coding:utf-8

import json
import threading
from tkinter import messagebox
import paho.mqtt.client as mqtt

import app

connect_flag = False

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

def disconnect(client, userdata, flag, rc):
    connect_flag = False
    pass


def connect(button):

    connect_th = threading.Thread(target=connect_t, args=(button,), daemon=True)
    connect_th.start()
    

def connect_t(button):

    try:
        #IPは選択できるように後改変。
        client.connect("192.168.0.1",1883,60)
        
        button.configure(bg="#94FF33", state="disable")

        messagebox.showinfo("notice", "Connection complete.")

        connect_flag = True

        client.on_message = set_text
        client.on_disconnect = disconnect

        client.subscribe("sub")

        client.loop_forever()
    except:
        button.configure(state="normal")
        
        messagebox.showinfo("notice", "Connection timeout.")


def set_text(client, userdata, msg):
    ret_port_stat = msg.payload.decode("utf-8")
    ret_port_stat = json.loads(ret_port_stat)
    
    set_text_th = threading.Thread(target=set_text_t, args=(ret_port_stat,), daemon=True)
    set_text_th.start()


def set_text_t(ret_port_stat):

    text_labels = app.Port.sensor_text_labels + app.Port.motor_text_labels

    for i in range(len(text_labels)):
        text_labels[i].configure(text=ret_port_stat[i])
            

def set_port(sensor_port, sensor_mode, motor_port, motor_mode):

    if connect_flag == False:
        messagebox.showinfo("notice", "No connection to the EV3.")
        return

    client.publish("test", "set_port")

    port_info = sensor_port + motor_port
    port_mode = sensor_mode + motor_mode
    
    for key, port, mode in zip(port_stat, port_info, port_mode):
        port_stat[key][0] = port.get()
        port_stat[key][1] = mode.get()

    port_stat_json = json.dumps(port_stat)

    client.publish("test", port_stat_json)