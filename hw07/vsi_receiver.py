import paho.mqtt.client as mqtt
from cv2 import imdecode, IMREAD_COLOR, imwrite
import numpy as np
from os import system

LOCAL_MQTT_HOST="mqtt_broker"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="homework3"

def on_connect_local(client, userdata, flags, rc):
        print("connected to local broker with rc: " + str(rc))
        client.subscribe(LOCAL_MQTT_TOPIC)
	

def on_message_local(client, userdata, msg):
  try:
    i = int(msg.payload[0])   # get message number
    png = msg.payload[1:]
    print(str(i) + "th message received locally!")	    
    png_new = imdecode(np.fromstring(png, dtype=np.uint8),IMREAD_COLOR)
    imwrite('/home/faces/face_' + str(i) + '.png', png_new)
    print(str(i) + "th message saved to png!")
    system('s3cmd sync /home/faces/ s3://251hw03mz/')
    print(str(i) + "th message synced to s3!")
  except:
    print("Unexpected error:", sys.exc_info()[0])


local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
local_mqttclient.on_message = on_message_local

local_mqttclient.loop_forever()