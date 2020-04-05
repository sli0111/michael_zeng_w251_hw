# Homework 13: Deep Learning SDK (the unofficial one, by Dustin Franklin)

We find that Dusty's repo has been one of the best places to find cool examples and cool code for doing something practical, so hopefully you'll enjoy it as well.  In this homework, you'll be using transfer learning to create a model that classifies plants, directly on your TX2!

# Submission

* Please submit the time it took you to train the model along with the final accuracy top1/top5 that you were able to achieve. 

    It took the TX2 about 4 hours to train 36 epochs. The best accuracy I have is 41.586% for top1 and 75.066% for top 5. See screen shot below. 

    ```
    Epoch: [34] completed, elapsed time 342.343 seconds
    Test: [  0/142]	Time  0.424 ( 0.424)	Loss 2.9997e+00 (2.9997e+00)	Acc@1  12.50 ( 12.50)	Acc@5  25.00 ( 25.00)
    Test: [ 10/142]	Time  0.076 ( 0.118)	Loss 1.5620e+00 (1.8617e+00)	Acc@1  62.50 ( 45.45)	Acc@5  87.50 ( 76.14)
    Test: [ 20/142]	Time  0.075 ( 0.103)	Loss 1.7048e+00 (1.6709e+00)	Acc@1  50.00 ( 52.38)	Acc@5  62.50 ( 79.17)
    Test: [ 30/142]	Time  0.072 ( 0.099)	Loss 1.0812e+00 (1.7445e+00)	Acc@1  62.50 ( 50.00)	Acc@5 100.00 ( 76.61)
    Test: [ 40/142]	Time  0.073 ( 0.094)	Loss 2.8683e+00 (1.8986e+00)	Acc@1   0.00 ( 44.21)	Acc@5  62.50 ( 74.39)
    Test: [ 50/142]	Time  0.073 ( 0.090)	Loss 9.0853e-01 (1.7440e+00)	Acc@1  75.00 ( 49.26)	Acc@5  87.50 ( 76.23)
    Test: [ 60/142]	Time  0.073 ( 0.088)	Loss 6.5021e-01 (1.6337e+00)	Acc@1  62.50 ( 52.46)	Acc@5 100.00 ( 78.69)
    Test: [ 70/142]	Time  0.072 ( 0.087)	Loss 9.6111e-01 (1.7742e+00)	Acc@1  75.00 ( 48.77)	Acc@5  75.00 ( 74.82)
    Test: [ 80/142]	Time  0.071 ( 0.085)	Loss 3.9203e+00 (1.7938e+00)	Acc@1   0.00 ( 48.46)	Acc@5   0.00 ( 74.69)
    Test: [ 90/142]	Time  0.085 ( 0.085)	Loss 1.9582e+00 (1.8923e+00)	Acc@1  37.50 ( 45.33)	Acc@5  75.00 ( 72.66)
    Test: [100/142]	Time  0.074 ( 0.084)	Loss 2.4907e+00 (1.8781e+00)	Acc@1  12.50 ( 45.42)	Acc@5  62.50 ( 74.26)
    Test: [110/142]	Time  0.071 ( 0.083)	Loss 2.7248e+00 (1.8725e+00)	Acc@1   0.00 ( 44.59)	Acc@5  87.50 ( 75.11)
    Test: [120/142]	Time  0.073 ( 0.083)	Loss 2.6053e+00 (1.8870e+00)	Acc@1   0.00 ( 43.70)	Acc@5  62.50 ( 75.72)
    Test: [130/142]	Time  0.081 ( 0.083)	Loss 3.4190e+00 (1.9503e+00)	Acc@1  12.50 ( 41.32)	Acc@5  50.00 ( 74.62)
    Test: [140/142]	Time  0.093 ( 0.083)	Loss 2.3361e+00 (1.9262e+00)	Acc@1  12.50 ( 41.49)	Acc@5  62.50 ( 75.00)
    * Acc@1 41.586 Acc@5 75.066`
    ```

* Could you increase the batch size? Why? How long did the training take you? 
    
    Yes, the default is 8 and I tried increase it to 64. The TX2 still has more memory left, so I could increase this further if I want to. This time the taining is faster, 250 sec/epoch vs 350 sec/epoch before. 35 epochs took about 2 and half hours. 

Please save your trained model, we'll use it for the lab.

# Original Readme
## Setting up

* Review the [github repo](https://github.com/dusty-nv/jetson-inference)
* Review the Docker file (Dockerfile.inf) required the build the container
* Try building on the TX2, e.g. ``` docker build -t inf -f Dockerfile.inf .``` This will take a few minutes.
* Start the container in interactive mode, e.g.
```
# this needs to be done on the jetson
xhost +
docker run --rm --privileged -v /tmp:/tmp -v /data:/data -v /var:/var -v /home/nvidia/models:/models --net=host --ipc=host --env DISPLAY=$DISPLAY -ti w251/inf:dev-tx2-4.3_b132 bash
```
* Pytorch and torchvision should already be installed for you, just make sure you use python3 for all commands instead of regular python (which points to python2)
* Swap should also be already set up for you ( we did this in homework 1)

## Training the model
We suggest that you generally follow [these instructions](https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-plants.md) to train ResNet-18 on the PlantCLEF dataset.  Just a few notes:
* Review the [train script](https://github.com/dusty-nv/pytorch-imagenet/blob/master/train.py)
* Once again, please use python3 for all commands
* Note that in the instructions above, you passed through /data to your container.  Create the dataset directory, download the dataset / uncompress there.
* Train for 100 epochs
* You are running on the tx2, so the training will take less time than on the nano (which is what Dusty benchmarked on)

### Note:
if you see the ```ImportError: cannot import name 'PILLOW_VERSION'``` error, downgrade it:
```
pip3 install Pillow==6.1%
```
## To submit
Please submit the time it took you to train the model along with the final accuracy top1/top5 that you were able to achieve. Could you increase the batch size? Why? How long did the training take you? Please save your trained model, we'll use it for the lab.


Credit / no credit only
