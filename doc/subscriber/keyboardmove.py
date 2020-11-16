#coding:utf-8

import sub
import json
import threading
from ev3dev.auto import *

import portset

motors = None
steer_motor = None


def set_key_motor(client, userdata, msg):
    
    global steer_motor, motors

    try:
        motors = ["portA", "portB", "portC", "portD"]
        steer_motor = []

        msg = msg.payload.decode("utf-8")

        steer_motor = json.loads(msg)

        motors.remove(steer_motor[0])
        motors.remove(steer_motor[1])
    except:
        pass

    client.on_message = sub.separate


def press_key(client, userdata, msg):
    
    global steer_motor, motors

    msg = msg.payload.decode("utf-8")

    key_info = json.loads(msg)

    if len(steer_motor) == 2:
        if key_info[0] == "q":
            portset.port_stat[steer_motor[0]][0].run_forever(speed_sp=key_info[1] * -10)
        elif key_info[0] == "a":
            portset.port_stat[steer_motor[0]][0].run_forever(speed_sp=key_info[1] * 10)
        elif key_info[0] == "w":
            portset.port_stat[steer_motor[0]][0].run_forever(speed_sp=key_info[1] * 10)
            portset.port_stat[steer_motor[1]][0].run_forever(speed_sp=key_info[1] * 10)
        elif key_info[0] == "s":
            portset.port_stat[steer_motor[0]][0].run_forever(speed_sp=key_info[1] * -10)
            portset.port_stat[steer_motor[1]][0].run_forever(speed_sp=key_info[1] * -10)
        elif key_info[0] == "e":
            portset.port_stat[steer_motor[1]][0].run_forever(speed_sp=key_info[1] * -10)
        elif key_info[0] == "d":
            portset.port_stat[steer_motor[1]][0].run_forever(speed_sp=key_info[1] * 10)
        elif key_info[0] == "r":
            portset.port_stat[motors[0]][0].run_forever(speed_sp=key_info[1] * -10)
        elif key_info[0] == "f":
            portset.port_stat[motors[0]][0].run_forever(speed_sp=key_info[1] * 10)
        elif key_info[0] == "t":
            portset.port_stat[motors[1]][0].run_forever(speed_sp=key_info[1] * -10)
        elif key_info[0] == "g":
            portset.port_stat[motors[1]][0].run_forever(speed_sp=key_info[1] * 10)
    else:
        if key_info[0] == "q":
            portset.port_stat[motors[0]][0].run_forever(speed_sp=key_info[1] * -10)
        elif key_info[0] == "a":
            portset.port_stat[motors[0]][0].run_forever(speed_sp=key_info[1] * 10)
        elif key_info[0] == "w":
            portset.port_stat[motors[1]][0].run_forever(speed_sp=key_info[1] * -10)
        elif key_info[0] == "s":
            portset.port_stat[motors[1]][0].run_forever(speed_sp=key_info[1] * 10)
        elif key_info[0] == "e":
            portset.port_stat[motors[2]][0].run_forever(speed_sp=key_info[1] * -10)
        elif key_info[0] == "d":
            portset.port_stat[motors[2]][0].run_forever(speed_sp=key_info[1] * 10)
        elif key_info[0] == "r":
            portset.port_stat[motors[3]][0].run_forever(speed_sp=key_info[1] * -10)
        elif key_info[0] == "f":
            portset.port_stat[motors[3]][0].run_forever(speed_sp=key_info[1] * 10)

    client.on_message = sub.separate


def release_key(client, userdata, msg):

    stop_motors = ["portA", "portB", "portC", "portD"]

    for i in range(len(stop_motors)):
        try:
            portset.port_stat[stop_motors[i]][0].stop(stop_action="coast")
        except:
            pass
        
    client.on_message = sub.separate

