#coding:utf-8

import json
import threading
import paho.mqtt.client as mqtt

#import linetrace

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("topic/motor/dt")


def divide(client, userdata, msg):

    msg = msg.payload.decode("utf-8")

    if msg == "set_port":
        print("setport")
        client.on_message = set_port


def set_port(client, userdata, msg):
    msg = msg.payload.decode("utf-8")
    
    port_stat = json.loads(msg)

    port_names = ["port1", "port2", "port3", "port4", "portA", "portB", "portC", "portD"]
    set_ports = ["INPUT_1", "INPUT2", "INPUT_3", "INPUT_4", "OUTPUT_A", "OUTPUT_B", "OUTPUT_C", "OUTPUT_D"]

    for port_name, set_port in port_names, set_ports:
    
        if port_stat[port_name][0] == "none":
            port_stat[port_name[0] == None

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

        elif port_stat[port_name][0] == "Large Motor":
            port_stat[port_name][0] = LargeMotor(set_port)

    client.publish("test", "Port setting was complete.")

    client.on_message = divide


if __name__ == "__main__":
    try:
        client = mqtt.Client()
        client.connect("localhost", 1883, 60)

        client.on_message = divide
        client.on_connect = on_connect

        
    except:
        quit()

    client.loop_forever()
