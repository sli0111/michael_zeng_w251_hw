# TF2
* Run the container:
    ```
    docker run --privileged --rm \
    -p 8888:8888 \
    -v "$(pwd)":/notebooks/ \
    --memory-swap -1 \
    --memory-swappiness 100 \
    -d w251/keras:dev-tx2-4.3_b132
    ```

# TF1
* Run the container: 

    `docker run --privileged --rm -p 6006:6006 -v "$(pwd)":/tmp/ --memory-swap -1 --memory-swappiness 100 -ti w251/tensorflow:dev-tx2-4.3_b132-tf1 bash`
* Clone git repo:

    `git clone https://github.com/googlecodelabs/tensorflow-for-poets-2`
    `cd tensorflow-for-poets-2`
* Download training image
    `curl http://download.tensorflow.org/example_images/flower_photos.tgz \    | tar xz -C tf_files`

* start TensorBoard
    `tensorboard --logdir tf_files/training_summaries &`

* Run the training
    `docker exec -i -t trusting_stallman bash`
    ```
    python3 -m scripts.retrain \
    --bottleneck_dir=tf_files/bottlenecks \
    --how_many_training_steps=4000 \
    --model_dir=tf_files/models/ \
    --summaries_dir=tf_files/training_summaries/mobilenet_0.50_224 \
    --output_graph=tf_files/retrained_graph.pb \
    --output_labels=tf_files/retrained_labels.txt \
    --architecture=mobilenet_0.50_224 \
    --image_dir=tf_files/flower_photos
    ```

* Classifying an image
    ```
    python3 -m scripts.label_image \
    --graph=tf_files/retrained_graph.pb  \
    --image=tf_files/flower_photos/roses/2414954629_3708a1a04d.jpg 
    ```

# Submission

1. What is TensorFlow? Which company is the leading contributor to TensorFlow?
2. What is TensorRT? How is it different from TensorFlow?
3. What is ImageNet? How many images does it contain? How many classes?
4. Please research and explain the differences between MobileNet and GoogleNet (Inception) architectures.
5. In your own words, what is a bottleneck?
6. How is a bottleneck different from the concept of layer freezing?
7. In the TF1 lab, you trained the last layer (all the previous layers retain their already-trained state). Explain how the lab used the previous layers (where did they come from? how were they used in the process?)
8. How does a low --learning_rate (step 7 of TF1) value (like 0.005) affect the precision? How much longer does training take?
9. How about a --learning_rate (step 7 of TF1) of 1.0? Is the precision still good enough to produce a usable graph?
10. For step 8, you can use any images you like. Pictures of food, people, or animals work well. You can even use ImageNet images. How accurate was your model? 11. Were you able to train it using a few images, or did you need a lot?
12. Run the TF1 script on the CPU (see instructions above) How does the training time compare to the default network training (section 4)? Why?
13. Try the training again, but this time do export ARCHITECTURE="inception_v3" Are CPU and GPU training times different?
14. Given the hints under the notes section, if we trained Inception_v3, what do we need to pass to replace ??? below to the label_image script? Can we also glean the answer from examining TensorBoard?