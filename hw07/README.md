# Homework 7 - Neural face detection pipeline

## Submission

* Docker: we are using the image from lab5 `docker run --privileged --rm -v "$(pwd)":/notebooks/tf_trt_models/hw07 -p 8888:8888 -d w251/tensorrtlab05:dev-tx2-4.3_b132`

* Please see the example notebook at https://github.com/zengm71/michael_zeng_w251_hw/blob/master/hw07/hw07_michael_zeng.ipynb for sample code for face detection. 

* Please see images at http://251hw07mz.s3.us-south.cloud-object-storage.appdomain.cloud/face_<picture_number>.png, the `picture_number` can be from 1 to 10.

## Answers:

* Describe your solution in detail.  What neural network did you use? What dataset was it trained on? What accuracy does it achieve?

    I used the model from https://github.com/yeephycho/tensorflow-face-detection. I didn't retrain it, but I believe it is originally trained on the http://shuoyang1213.me/WIDERFACE/ dataset.

* Does it achieve reasonable accuracy in your empirical tests? Would you use this solution to develop a robust, production-grade system?
    
    It tests pretty well, recognizes multiple faces

* What framerate does this method achieve on the Jetson? Where is the bottleneck?
    
    The framerate is a bit low, it about 12 frames a second. I think the bottleneck is I didn't successfully resize the image: the image I sent in is (480, 640, 3).

* Which is a better quality detector: the OpenCV or yours?

    I think this one tests equally well as the OpenCV detector, especially in the sense that the false positve rate is pretty low.

## Pipeline 
### On Jetson

1. Create a bridge network
`docker network create --driver bridge hw07`

2. MQTT broker

    * Build the image (we can reuse the image from HW3)

        `sudo docker build -t mqtt_broker -f dockerfile_tx2_mqtt_broker .`

    * Spin up container and establish broker

        `sudo docker run --rm --name mqtt_broker --network hw07 -p 1883:1883 -ti mqtt_broker /usr/sbin/mosquitto`

3. MQTT forwarder

    This spins up the forwarder that connects with both broker, so make sure the broker is up on VSI as well (see below).

    * Build the image (we can reuse the image from HW3)

        `sudo docker build -t mqtt_forwarder -f dockerfile_tx2_mqtt_forwarder .`

    * Spin up container and run `tx2_forwarder.py`

        `sudo docker run --rm --name mqtt_forwarder --network hw07 -v /home/zengm71/Documents/W251/michael_zeng_w251_hw/hw07/:/home/ -ti mqtt_forwarder /bin/sh /home/tx2_run_forwarder.sh`

4. OpenCV face detector

    * Build the image

        `sudo docker build -t face_detector07 -f dockerfile_tx2_face_detector .`

    * Spin up the container and run `tx2_face_detector.py`

        `sudo docker run --rm --privileged -e DISPLAY --name face_detector --network hw07 -v /home/zengm71/Documents/W251/michael_zeng_w251_hw/hw07/:/home/ -ti face_detector07 /bin/bash /home/tx2_run_face_detector.sh`

    * Note that in `tx2_face_detector.py` I added in a timeout of 10 seconds as well as a single digit counter to keep track of faces/pictures. These were used just so that I don't overwhelm the output with tons of images. Tests have been done with these two restrictions removed and it still works nicely. 

### On VSI

1. Create a bridge network
`sudo docker network create --driver bridge hw07`

2. MQTT broker

    * Build the image

        `sudo docker build -t mqtt_broker -f dockerfile_vsi_mqtt_broker .`

    * Spin up container and establish broker

        `sudo docker run --rm --name mqtt_broker --network hw07 -p 1883:1883 -ti mqtt_broker /usr/sbin/mosquitto`

3. MQTT receiver

    * Build the image

        Unfortunately, I didn't find a way to decode the bytes message without openCV, so this receiver image is the same with the image for face detector, except that I also needed to add `s3cmd`. It is bigger than I idealy wanted, but it works for now.

        `sudo docker build -t mqtt_receiver -f dockerfile_vsi_mqtt_receiver .`

    * Spin up container and run `vsi_receiver.py`

        `sudo docker run --rm --name mqtt_receiver --network hw07 -v ~/michael_zeng_w251_hw/hw07/:/home/ -v ~/.s3cfg:/root/.s3cfg -ti mqtt_receiver /bin/bash /home/vsi_run_receiver.sh`

4. Note on S3 buckets

    The newer version of S3 buckets support public access much easier. `s3cmd` still works with the newer buckets, but one needs to create new credential with HMAC checked to see the access_key and secret_access_key.

## Original README
### Overview
The objective of this homework is simple: modify the processing pipeline that you implemented in 
[homework 3](https://github.com/MIDS-scaling-up/v2/blob/master/week03/hw/README.md) and replace the OpenCV-based face detector with 
a Deep Learning-based one. You could, for instance, rely on what you learned in 
[TensorRT lab 5](https://github.com/MIDS-scaling-up/v2/blob/master/week05/labs/lab_tensorrt.md) or 
[Digits lab 5](https://github.com/MIDS-scaling-up/v2/blob/master/week05/labs/lab_digits.md)

### Hints
* You have the freedom to choose the neural network that does the detection, but don't overthink it; this is a credit / no credit assignment that is not supposed to take a lot of time.
* There is no need to train the network in this assignment, just find and use a pre-trained model that is trained on a face dataset.
* Your neural detector should run on the Jetson.
* Just like the OpenCV detector, your neural detector needs to take a frame as input and return an array of rectangles for each face detected.
* Most neural object detectors operate on a frame of a given size, so you may need to resize the frame you get from your webcam to that resolution.
* Note that face detection is not the same as face recognition; you don't need to discriminate between different faces
* Here's a [sample notebook](hw07-hint.ipynb) that loads and uses [one face detector](https://github.com/yeephycho/tensorflow-face-detection)
* A more graceful solution would involve using a face detector from [TensorFlow's Model Zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md) -- [this network](http://download.tensorflow.org/models/object_detection/facessd_mobilenet_v2_quantized_320x320_open_image_v4.tar.gz), to be exact, but at the moment, simply loading it as we did in [TensorRT lab 5](https://github.com/MIDS-scaling-up/v2/blob/master/week05/labs/lab_tensorrt.md)  does not work due to [this bug](https://stackoverflow.com/questions/53563976/tensorflow-object-detection-api-valueerror-anchor-strides-must-be-a-list-wit)

### Questions
* Describe your solution in detail.  What neural network did you use? What dataset was it trained on? What accuracy does it achieve?
* Does it achieve reasonable accuracy in your empirical tests? Would you use this solution to develop a robust, production-grade system?
* What framerate does this method achieve on the Jetson? Where is the bottleneck?
* Which is a better quality detector: the OpenCV or yours?

### To turn in:

Please provide answers to questions above, a copy of the code related to the neural face detector along with access to the location (object storage?) containing the detected face images. Note that this homework is NOT graded, credit / no credit only.
