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
    app.Port.connect_button.configure(background=app.Port.origin_color, state="enable")


def connect():

    connect_th = threading.Thread(target=connect_t, daemon=True)
    connect_th.start()
    

def connect_t():
    global connect_flag

    try:
        app.Port.connect_button.configure(state="disable")

        #IPは選択できるように後改変。
        client.connect(app.Home.ip,1883,30)

        messagebox.showinfo("notice", "Connection complete.")

        connect_flag = True

        app.Port.connect_button.configure(background="#94FF33")

        client.on_message = res_check
        client.on_disconnect = disconnect

        client.subscribe("sub")

        client.loop_forever()
    except:
        app.Port.connect_button.configure(background=app.Port.origin_color, state="normal")
        
        messagebox.showinfo("notice", "Connection timeout.")


def res_check(client, useredate, msg):

    if msg.payload.decode("utf-8") == "complete":
        client.on_message = set_text

        set_key_motor()


def set_text(client, userdata, msg):

    if msg.payload.decode("utf-8") == "complete":
        set_key_motor()
    else:
        ret_port_stat = msg.payload.decode("utf-8")
        ret_port_stat = json.loads(ret_port_stat)

        set_text_th = threading.Thread(target=set_text_t, args=(ret_port_stat,), daemon=True)
        set_text_th.start()


def set_text_t(ret_port_stat):

    text_labels = app.Port.sensor_text_labels + app.Port.motor_text_labels

    for i in range(len(text_labels)):
        text_labels[i].configure(text=ret_port_stat[i])

    client.publish("test", "lblset")
            

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

    # send each port infomation
    client.publish("test", port_stat_json)

    # port_stat送ったあとに、portsetが別メソッドでリッスンして、そこにキーボード用のポートをpublishする。
    # sub側に送る内容。[速度, A, D] ... [速度, B, C]
    # 1.subでキーボード用に使うポートを2つゲットする。
    # 2.wasdで登録する。(これはソフトの仕様で、A~Dで早い順に、右左とする。)
    # 3.余ったキーは、qとeに登録する。(これも早い順に。)


def set_key_motor():

    client.publish("test", "key_motor")

    key_motor = []
    
    port_names = ["portA", "portB", "portC", "portD"]

    true_motor_count = 0
    for i in range(4):
        if app.Port.motor_check[i].get() == True:
            key_motor.append(port_names[i])
            true_motor_count += 1

    if true_motor_count == 1:
        messagebox.showinfo("notice", "Cannot select only 1 motors.")
        return
    elif true_motor_count > 2:
        messagebox.showinfo("notice", "Cannot select over 2 motors.")
        return
    elif true_motor_count == 0:
        key_motor_json = json.dumps(key_motor)
        client.publish("test", key_motor_json)
        return

    key_motor_json = json.dumps(key_motor)

    client.publish("test", key_motor_json)


key_stat = None

# keyinput時のメソッド
def key_event(key, stat):

    global key_stat

    key_info_json = None

    if stat == "press":
        if key_stat == None:
            client.publish("test", "press")

            if app.Port.chk.get() == True:
                key_info = [key, app.Port.motor_power * -1]
            else:
                key_info = [key, app.Port.motor_power]

            key_info_json = json.dumps(key_info)

            client.publish("test", key_info_json)

            key_stat = "press"

    elif stat == "release":
        if key_stat == "press":
            client.publish("test", "release")

            client.publish("test", key_info_json)

            key_stat = None