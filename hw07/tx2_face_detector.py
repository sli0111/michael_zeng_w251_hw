import numpy as np
import cv2
import paho.mqtt.client as mqtt
import time


# start MQTT client ================================================================================
LOCAL_MQTT_HOST="mqtt_broker"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="homework3"

def on_connect_local(client, userdata, flags, rc):
        print("connected to local broker with rc: " + str(rc))
        client.subscribe(LOCAL_MQTT_TOPIC)
	

def on_message(client, userdata, msg):
  try:
    print("message received!")	
    # if we wanted to re-publish this message, something like this should work
    # msg = msg.payload
    # remote_mqttclient.publish(REMOTE_MQTT_TOPIC, payload=msg, qos=0, retain=False)
  except:
    print("Unexpected error:", sys.exc_info()[0])

# set up tensorflow ================================================================================
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tensorflow as tf
import tensorflow.contrib.tensorrt as trt

output_dir=''
FROZEN_GRAPH_NAME = 'data/frozen_inference_graph_face.pb'
frozen_graph = tf.GraphDef()
with open(os.path.join(output_dir, FROZEN_GRAPH_NAME), 'rb') as f:
  frozen_graph.ParseFromString(f.read())
  
INPUT_NAME='image_tensor'
BOXES_NAME='detection_boxes'
CLASSES_NAME='detection_classes'
SCORES_NAME='detection_scores'
MASKS_NAME='detection_masks'
NUM_DETECTIONS_NAME='num_detections'

input_names = [INPUT_NAME]
output_names = [BOXES_NAME, CLASSES_NAME, SCORES_NAME, NUM_DETECTIONS_NAME]

trt_graph = trt.create_inference_graph(
    input_graph_def=frozen_graph,
    outputs=output_names,
    max_batch_size=1,
    max_workspace_size_bytes=1 << 25,
    precision_mode='FP16',
    minimum_segment_size=50
)
print("graph created")
tf_config = tf.ConfigProto()
tf_config.gpu_options.allow_growth = True

tf_sess = tf.Session(config=tf_config)

# use this if you want to try on the optimized TensorRT graph
# Note that this will take a while
# tf.import_graph_def(trt_graph, name='')

# use this if you want to try directly on the frozen TF graph
# this is much faster
tf.import_graph_def(frozen_graph, name='')

tf_input = tf_sess.graph.get_tensor_by_name(input_names[0] + ':0')
tf_scores = tf_sess.graph.get_tensor_by_name('detection_scores:0')
tf_boxes = tf_sess.graph.get_tensor_by_name('detection_boxes:0')
tf_classes = tf_sess.graph.get_tensor_by_name('detection_classes:0')
tf_num_detections = tf_sess.graph.get_tensor_by_name('num_detections:0')

# start capturing faces ============================================================================
# 1 should correspond to /dev/video1 , your USB camera. The 0 is reserved for the TX2 onboard camera
print("start detecting faces")
cap = cv2.VideoCapture(1)

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
local_mqttclient.on_message = on_message
i = 0
while(True):
  # Capture frame-by-frame
  ret, image = cap.read()
  image_resized = np.array(image)
  scores, boxes, classes, num_detections = tf_sess.run([tf_scores, tf_boxes, tf_classes, tf_num_detections], 
                                                         feed_dict={tf_input: image_resized[None, ...]})
  boxes = boxes[0] # index by 0 to remove batch dimension
  scores = scores[0]
  classes = classes[0]
  num_detections = num_detections[0]
  
  # suppress boxes that are below the threshold.. 
  DETECTION_THRESHOLD = 0.5
  # plot boxes exceeding score threshold
  for j in range(int(num_detections)):
    if scores[j] < DETECTION_THRESHOLD:
        continue
    # scale box to image coordinates
    box = boxes[j] * np.array([image.shape[0], image.shape[1], image.shape[0], image.shape[1]])
    box  = box.astype(int)
    image = cv2.rectangle(image,(box[1], box[0]), (box[3], box[2]),(255,0,0),2)

  rc,png = cv2.imencode('.png', image)
  msg = png.tobytes()
  # payload = str(i)+str(msg)
  print(msg[0:20])
  # send it to brokers
  local_mqttclient.publish(LOCAL_MQTT_TOPIC, payload = msg, qos = 0, retain = False)
  # let's try keep track of faces detec
  i += 1
  if (i == 10): i = 0
  print(i)
  time.sleep(10)