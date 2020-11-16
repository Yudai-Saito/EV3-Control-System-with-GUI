#coding:utf-8

import json
import paho.mqtt.client as mqtt

import portset
import keyboardmove

def on_connect(client, userdata, flags, rc):

    print("Connected with result code " + str(rc))
    client.subscribe("test")


def separate(client, userdata, msg):

    msg = msg.payload.decode("utf-8")

    if msg == "set_port":
        client.on_message = portset.set_port
    elif msg == "key_motor":
        client.on_message = keyboardmove.set_key_motor
    elif msg == "press":
        client.on_message = keyboardmove.press_key
    elif msg == "release":
        client.on_message = keyboardmove.release_key


if __name__ == "__main__":
    try:
        client = mqtt.Client()
        client.connect("localhost", 1883, 60)
        client.on_message = separate
        client.on_connect = on_connect
    
    except:
        quit()
    
    client.loop_forever()
    