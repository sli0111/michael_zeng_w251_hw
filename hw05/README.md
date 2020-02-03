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
    --how_many_training_steps=400 \
    --model_dir=tf_files/models/ \
    --learning_rate=0.005 \
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

    The core open source library to help you develop and train ML models. Get started quickly by running Colab notebooks directly in your browser. Google is the leading contributor to Tensorflow. 

2. What is TensorRT? How is it different from TensorFlow?

    NVIDIA TensorRT™ is an SDK for high-performance deep learning inference. It includes a deep learning inference optimizer and runtime that delivers low latency and high-throughput for deep learning inference applications. TensorRT-based applications perform up to 40x faster than CPU-only platforms during inference. With TensorRT, you can optimize neural network models trained in all major frameworks, calibrate for lower precision with high accuracy, and finally deploy to hyperscale data centers, embedded, or automotive product platforms

    It is an SDK, while Tensorflow is a library. By combining the two, users can get better performance for GPU inference in a simple way.

3. What is ImageNet? How many images does it contain? How many classes?

    ImageNet is an image dataset organized according to the WordNet hierarchy. Each meaningful concept in WordNet, possibly described by multiple words or word phrases, is called a "synonym set" or "synset". There are more than 100,000 synsets in WordNet, majority of them are nouns (80,000+). In ImageNet, we aim to provide on average 1000 images to illustrate each synset. Images of each concept are quality-controlled and human-annotated. In its completion, we hope ImageNet will offer tens of millions of cleanly sorted images for most of the concepts in the WordNet hierarchy.

4. Please research and explain the differences between MobileNet and GoogleNet (Inception) architectures.

    The difference is that MobileNet forms a factorized convolutions. Factorizing convolutions indicates factorizing a standard convolution into a depthwise convolution and a pointwise convolution. This is called depthwise separable convolution.

    In depthwise separable convolution, we first split each channel of the input and the filter, and convolve the input with the corresponding filter, or in a depthwise manner. And then concatenate the output together. This is depthwise convolution. After that, we do pointwise convolution, which is the same as 1x1 convolution. This drastically decreases the computational burden.

5. In your own words, what is a bottleneck?

    A bottleneck is input data to the final layer of the network: it has been put through layers of transformation in every layer of the network except for the final one.

6. How is a bottleneck different from the concept of layer freezing?

    Layer freezing is more related to how training is done. One can pick a layer and apply layer freezing such that the weights for that layer does not get updated in the training. In that sense bottlenet is like applying layer freezing to all layers except the very last one. However, on a different aspect, bottleneck is also more related to output -- the tranformed data by every layer but the last from the network. One would compute the bottlenecks for all images and cache them before training, yet one don't use that concept together witth layer freezing.

7. In the TF1 lab, you trained the last layer (all the previous layers retain their already-trained state). Explain how the lab used the previous layers (where did they come from? how were they used in the process?)

    The previous layer was downloaded directly, and they are used to calculated the bottlencks for every image. They are in a sense all freezed, since only the final layer needs to be retrained. 

8. How does a low --learning_rate (step 7 of TF1) value (like 0.005) affect the precision? How much longer does training take?

    This make the training slower but not a whole lot to show for mere 400 steps. 400 steps with 0.005 took roughly 120 secs and had a  final accuracy of 89.8%, while with 0.01 took about 110 secs and had a final accuracy of 89.1%.

9. How about a --learning_rate (step 7 of TF1) of 1.0? Is the precision still good enough to produce a usable graph?

    The training took about 105 sec, which is similar to learning rate of 0.01 but it is mostly because the number of steps is too small. The final accuracy is 86.5%, it is still somewhat usable, yet it also has bigger variance: I repreated the experiment a few time and saw wide range of final accuracies. 

10. For step 8, you can use any images you like. Pictures of food, people, or animals work well. You can even use ImageNet images. How accurate was your model?

11. Were you able to train it using a few images, or did you need a lot?

12. Run the TF1 script on the CPU (see instructions above) How does the training time compare to the default network training (section 4)? Why?
    ```
    docker run --rm -p 6006:6006 -v "$(pwd)":/tmp/ --memory-swap -1 --memory-swappiness 100 -ti w251/tensorflow:dev-tx2-4.3_b132-tf1 bash
    ```
    Running with learning rate 0.01 for 400 steps took 130 secs while `tegrastats` showing `GR3D_FREQ` of 0%. GPU is better suited for the operations involved in the neural network training. 
13. Try the training again, but this time do export ARCHITECTURE="inception_v3" Are CPU and GPU training times different?

14. Given the hints under the notes section, if we trained Inception_v3, what do we need to pass to replace ??? below to the label_image script? Can we also glean the answer from examining TensorBoard?