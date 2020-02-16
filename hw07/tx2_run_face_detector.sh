apt install -y python3-opencv python-pip vim-tiny mosquitto-clients libopencv-dev
pip install paho-mqtt
wget https://github.com/yeephycho/tensorflow-face-detection/blob/master/model/frozen_inference_graph_face.pb?raw=true -O 'data/frozen_inference_graph_face.pb'

python /home/tx2_face_detector.py