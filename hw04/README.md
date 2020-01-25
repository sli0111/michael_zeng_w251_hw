# Homework 3

## On Jetson

1. Create a bridge network
`docker network create --driver bridge hw03`

2. MQTT broker

    * Build the image

        `sudo docker build -t mqtt_broker -f dockerfile_tx2_mqtt_broker .`

    * Spin up container and establish broker

        `sudo docker run --rm --name mqtt_broker --network hw03 -p 1883:1883 -ti mqtt_broker /usr/sbin/mosquitto`

3. MQTT forwarder

    This spins up the forwarder that connects with both broker, so make sure the broker is up on VSI as well (see below).

    * Build the image

        `sudo docker build -t mqtt_forwarder -f dockerfile_tx2_mqtt_forwarder .`

    * Spin up container and run `tx2_forwarder.py`

        `sudo docker run --rm --name mqtt_forwarder --network hw03 -v ~/Documents/W251/v2/week03/hw_mz/:/home/ -ti mqtt_forwarder /bin/sh /home/tx2_run_forwarder.sh`

4. OpenCV face detector

    * Build the image

        `sudo docker build -t face_detector -f dockerfile_tx2_face_detector .`

    * Spin up the container and run `tx2_face_detector.py`

        `sudo docker run --rm --privileged -e DISPLAY --name face_detector --network hw03 -v ~/Documents/W251/v2/week03/hw_mz/:/home/ -ti face_detector /bin/bash /home/tx2_run_face_detector.sh`

    * Note that in `tx2_face_detector.py` I added in a timeout of 10 seconds as well as a single digit counter to keep track of faces/pictures. These were used just so that I don't overwhelm the output with tons of images. Tests have been done with these two restrictions removed and it still works nicely. 

## On VSI

1. Create a bridge network
`sudo docker network create --driver bridge hw03`

2. MQTT broker

    * Build the image

        `sudo docker build -t mqtt_broker -f dockerfile_vsi_mqtt_broker .`

    * Spin up container and establish broker

        `sudo docker run --rm --name mqtt_broker --network hw03 -p 1883:1883 -ti mqtt_broker /usr/sbin/mosquitto`

3. MQTT receiver

    * Build the image

        Unfortunately, I didn't find a way to decode the bytes message without openCV, so this receiver image is the same with the image for face detector, except that I also needed to add `s3cmd`. It is bigger than I idealy wanted, but it works for now.

        `sudo docker build -t mqtt_receiver -f dockerfile_vsi_mqtt_receiver .`

    * Spin up container and run `vsi_receiver.py`

        `sudo docker run --rm --name mqtt_receiver --network hw03 -v ~/W251/HW/hw03/:/home/ -v ~/.s3cfg:/root/.s3cfg -ti mqtt_receiver /bin/bash /home/vsi_run_receiver.sh`

4. Note on S3 buckets

    The newer version of S3 buckets support public access much easier. `s3cmd` still works with the newer buckets, but one needs to create new credential with HMAC checked to see the access_key and secret_access_key.

## Submission

1. The repo for the code can be found at `https://github.com/zengm71/v2/tree/master/week03/hw`, please let me know if there is any trouble accessing it.

2. The link to the faces can be found at `https://251hw03mz.s3.us-south.cloud-object-storage.appdomain.cloud/face_<picture_number>.png`, where `picture_number` goes from 0 to 9. As discussed above, I kept a counter that loops from 0 to 9, just so that we don't overwhelm the output.

3. Naming of the MQTT topics: I created a simple single-level topic for the MQTT topic `homework3` for this simple task. Since we are only markin the face and transfer the picture, I don't see we need multiple levels of topic. If, however, we are doing classifications, we could set levels in topic: for example faces/my_face, faces/wife_face, backpacks/my_backpack, backpacks/wife_backpack and such.

4. Choice of QoS: I picked QoS 0 for this task, which is also commonly known as "fire and forgot". I picked it because we are streaming the pictures to the cloud, which means we are sending a big amount of pictures in bytes, though each one is relatively small. Having higher QoS level is not necessary, because most of the pictures are highly repetitive in this case: it is ok if we lost one or two packages.