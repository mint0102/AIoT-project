import sys
from Adafruit_IO import MQTTClient
import time
import random
from simple_ai import *
from uart import *

AIO_FEED_IDs = ["button1", "button2"]
AIO_USERNAME = "Mintmin"
AIO_KEY = "aio_tJiz116WHHfFHHZhaBWDhbl4f90n"

def connected(client):
    print("Ket noi thanh cong ...")
    for topic in AIO_FEED_IDs:
        client.subscribe(topic)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Nhan du lieu: " + payload + ", feed id: " + feed_id)
    if feed_id == "button1":
        if payload == "0":
            writeData(1)
        else:
            writeData(2)
    if feed_id == "button2":
        if payload == "0":
            writeData(3)
        else:
            writeData(4)
client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe     #call back
client.connect()
client.loop_background() 
counter = 10
sensor_type = 0
counter_ai = 5

while True:
    # counter -= 1
    # if counter <= 0:
    #     counter = 10 # 10s lặp 1 lần
    #     #TODO
    #     print("Random data is publishing...")
    #     if sensor_type == 0:
    #         print("Temperature...")
    #         temp = random.randint(10, 50) #random temperature
    #         client.publish("sensor1", temp)
    #         sensor_type = 1
    #     elif sensor_type == 1:
    #         print("Light...")   
    #         light = random.randint(50, 500) #random light
    #         client.publish("sensor2", light)
    #         sensor_type = 2
    #     elif sensor_type == 2:
    #         print("Humidity...")   
    #         humi = random.randint(20,80) #random humidity
    #         client.publish("sensor3", humi) 
    #         sensor_type = 0
    
    counter_ai -= 1
    if counter_ai <= 0:
        counter_ai = 5 
        ai_result = image_detector()
        print("AI result: ", ai_result)   
        client.publish("ai", ai_result)
    
    # #Recive from hardware
    readSerial(client) 
    time.sleep(1) #if you want to sent data more then 1s, you must used to loop!
    # # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break
