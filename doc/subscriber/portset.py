#coding:utf-8

import sub
import time
import json
import threading
from ev3dev.auto import *

connect_flag = False

port_names = ["port1", "port2", "port3", "port4", "portA", "portB", "portC", "portD"]
set_ports = ["in1", "in2", "in3", "in4", "outA", "outB", "outC", "outD"]

def set_port(client, userdata, msg):
    global connect_flag
    connect_flag = False
    
    msg = msg.payload.decode("utf-8")
    
    port_stat = json.loads(msg)

    for port_name, set_port in zip(port_names, set_ports):
    
        try:
            if port_stat[port_name][0] == "NONE":
                port_stat[port_name][0] = "NONE"

            elif port_stat[port_name][0] == "Color Sensor":
                port_stat[port_name][0] = ColorSensor(set_port)
                if port_stat[port_name][1] == "REFLECT":
                    port_stat[port_name][0].mode = "COL-REFLECT"
                elif port_stat[port_name][1] == "AMBIENT":
                    port_stat[port_name][0].mode = "COL-AMBIENT"
                elif port_stat[port_name][1] == "COLOR":
                    port_stat[port_name][0].mode = "COL-COLOR"
                elif port_stat[port_name][1] == "REF-RAW":
                    port_stat[port_name][0].mode = "REF-RAW"
                elif port_stat[port_name][1] == "RGB-RAW":
                    port_stat[port_name][0].mode = "RGB-RAW"

            elif port_stat[port_name][0] == "Gyro Sensor":
                port_stat[port_name][0] = GyroSensor(set_port)
                if port_stat[port_name][1] == "ANGLE":
                    port_stat[port_name][0].mode = "GYRO-ANG"
                elif port_stat[port_name][1] == "RATE":
                    port_stat[port_name][0].mode = "GYRO-RATE"
                elif port_stat[port_name][1] == "FAS":
                    port_stat[port_name][0].mode = "GYRO-FAS"
                elif port_stat[port_name][1] == "G&A":
                    port_stat[port_name][0].mode = "GYRO-G&A"
                elif port_stat[port_name][1] == "CAL":
                    port_stat[port_name][0].mode = "GYRO-CAL"

            elif port_stat[port_name][0] == "Touch Sensor":
                port_stat[port_name][0] = TouchSensor(set_port)
                port_stat[port_name][0].mode = "TOUCH"

            elif port_stat[port_name][0] == "Ultrasonc Sensor":
                port_stat[port_name][0] = UltrasonicSensor(set_port)
                if port_stat[port_name][1] == "DIST-CM":
                    port_stat[port_name][0].mode = "US-DIST-CM"
                elif port_stat[port_name][1] == "DIST-IN":
                    port_stat[port_name][0].mode = "US-DIST-IN"
                elif port_stat[port_name][1] == "LISTEN":
                    port_stat[port_name][0].mode = "US-LISTEN"
                elif port_stat[port_name][1] == "SI-CM":
                    port_stat[port_name][0].mode = "US-SI-CM"
                elif port_stat[port_name][1] == "SI-IN":
                    port_stat[port_name][0].mode = "US-SI-IN"

            elif port_stat[port_name][0] == "Medium Motor":
                port_stat[port_name][0] = MediumMotor(set_port)
                port_stat[port_name][0].state
                """
                This process is checking connections.
                if port_stat[port_name][0].state raise error, This device is not connected motor.
                """

            elif port_stat[port_name][0] == "Large Motor":
                port_stat[port_name][0] = LargeMotor(set_port)
                port_stat[port_name][0].state

        except :
            port_stat[port_name][0] = "NONE"

    send_port_info(client, port_stat)

    sub.client.on_message = sub.divide


def send_port_info(client, port_stat):
    global connect_flag
    connect_flag = True

    send_port_info_th = threading.Thread(target=send_port_info_t, args=(client, port_stat,))
    send_port_info_th.setDaemon(True)
    send_port_info_th.start()


def send_port_info_t(client, port_stat):

    while connect_flag == True:

        port_info = []

        try:
            for port_name in port_names:
                if port_stat[port_name][0] == "NONE":
                    port_info.append(None)

                elif port_stat[port_name][0].mode == "TOUCH":
                    port_info.append(port_stat[port_name][0].is_pressed)

                elif port_stat[port_name][0].mode == "COL-REFLECT":
                    port_info.append(port_stat[port_name][0].reflected_light_intensity)
        except:
            break

        port_stat_json = json.dumps(port_info)

        client.publish("sub", port_stat_json)
        
        time.sleep(0.05)