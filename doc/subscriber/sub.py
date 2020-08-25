#coding:utf-8

import json
import threading
import paho.mqtt.client as mqtt

import portset
#import linetrace


def on_connect(client, userdata, flags, rc):

    print("Connected with result code " + str(rc))
    client.subscribe("test")


def divide(client, userdata, msg):

    msg = msg.payload.decode("utf-8")

    if msg == "set_port":
        print("setport")
        client.on_message = portset.set_port


if __name__ == "__main__":
    try:
        client = mqtt.Client()
        client.connect("localhost", 1883, 60)

        client.on_message = divide
        client.on_connect = on_connect

    except:
        quit()

    client.loop_forever()
