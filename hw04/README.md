# Homework 4

## Submission
### ConvnetJS MNIST demo
* Name all the layers in the network, make sure you understand what they do.
    - `layer_defs.push({type:'input', out_sx:24, out_sy:24, out_depth:1});`

        *Comments*: this crops out a 24 by 24 window out of every 28 by 28 MNIST image. 
    
    - `layer_defs.push({type:'conv', sx:5, filters:8, stride:1, pad:2, activation:'relu'});`
    
        *Comments*: This is a convolutional layer, with 8 kernels, each of size 5 by 5, and strides through the original image with stride of 1 pixel. It creates a 2 pixel wide pad around each image. `relu` is picked as the activation function for the output
    
    - `layer_defs.push({type:'pool', sx:2, stride:2});`

        *Comments*: Max pooling with filter of size 2 by 2 is applied with stride of 2. 

    - `layer_defs.push({type:'conv', sx:5, filters:16, stride:1, pad:2, activation:'relu'});`

        *Comments*: This is a convolutional layer, with 16 kernels, each of size 5 by 5, and strides through the original image with stride of 1 pixel. It creates a 2 pixel wide pad around each image. `relu` is picked as the activation function for the output

    - `layer_defs.push({type:'pool', sx:3, stride:3});`

        *Comments*: Max pooling with filter of size 3 by 3 is applied with stride of 3. 

    - `layer_defs.push({type:'softmax', num_classes:10});`

        *Comments*: This is the final (output) layer, which applies a softmax function of size 10, picking 1 out of 10 digits as the prediction.

* Experiment with the number and size of filters in each layer. Does it improve the accuracy

    Not necessarily, the default setup already achieves pretty good accuracy. Increasing the size of the filter, however, enlarges the difference in accuracy between train and validation set. Intuitively picking smaller size filter improves the accuray, because the original image is only 28 by 28, therefore the local features are going to be more important. 

* Remove the pooling layers. Does it impact the accuracy?

    Removing the pooling layer reduces the accuracy, because pooling is an effectively step of feature engineering.  

* Add one more conv layer. Does it help with accuracy?

    Adding another conv layer it makes the difference in accuracy bigger between the training and validation set. 

* Increase the batch size. What impact does it have?

    Increasing the batch size makes the training slower, also the gradient seem to be smaller therefore the loss goes down slower. 

* What is the best accuracy you can achieve? Are you over 99%? 99.5%?
    
    The best validation accuray I saw is 99%. 

### Build your own model in Keras

Please see the notebook downloaded as `w251_homework04.html`.

## On Cloud

1. Install Docker
```
# Validate these at https://docs.docker.com/install/linux/docker-ce/ubuntu/
apt-get update
apt install apt-transport-https ca-certificates 
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic test" 
apt update 
apt install docker-ce
# Validated 09/14/19 - Darragh
# Test if docker hello world is working
docker run hello-world
```

2. Ensure that the VSI is sectured from SSH attacks
```
apt-get update
apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
```

3. Run the jupyter notebook
`docker run --rm -it -p 8888:8888 w251/tensorflow_hw04:latest`



