# Homework 11 -- More fun with OpenAI Gym!

## Submission
Run the script in docker. The following setup allows the edited script to run, as well as making use of the swap memory. 
```
sudo docker run --rm --net=host --runtime nvidia --memory 7G --memory-swap 30G --memory-swappiness 50 -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix:rw --privileged -v /data/videos:/tmp/videos -v "$(pwd)":/src -it lander python3 /src/run_lunar_lander.py
```

List of MP4s:
* `default_parms_frame50000.mp4`

	This is trained using the default setting to 50K steps

* `alter1_params_frame50000.mp4`
	```
	model.fit(np.array(X_train),np.array(y_train).reshape(len(y_train),1), epochs = 20, batch_size=100)
	```

	THis is trained with the following model with 20 epochs every time the model is fit

	```
	def nnmodel(input_dim):
	    model = Sequential()
	    model.add(Dense(400, input_dim=input_dim, activation='relu'))
	    model.add(BatchNormalization())
	    model.add(Dense(200, activation='relu'))
	    model.add(BatchNormalization())
	    model.add(Dense(1))
	    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mse'])
	    return model
	```
	After 50000 steps, the loss (MSE) was around 80. The changes I made were:
	* more epochs: it does look like the loss were decreasing shapely at 10th epoch, so I extended it to 20 since training time is not a big constraint here
	* more neurons: increase the neurals so that the model handles more complex relationships
	* batch normalization:

* `alter2_params_frame5000.mp4`

	```
	model.fit(np.array(X_train),np.array(y_train).reshape(len(y_train),1), epochs = 20, batch_size=int(steps/50))
	```
	```
	def nnmodel(input_dim):
	    model = Sequential()
	    model.add(Dense(128, input_dim=input_dim, activation='relu'))
	    model.add(BatchNormalization())
	    model.add(Dense(64, activation='relu'))
	    model.add(BatchNormalization())
	    model.add(Dense(32, activation='relu'))
	    model.add(BatchNormalization())
	    model.add(Dense(1))
	    model.compile(loss='mean_squared_error', optimizer='adamax', metrics=['mse'])
	    return model
	```

## Original README
In this homework, you will be training a Lunar Lander to land properly **using your Jetson TX2**. There is a video component to this file, so use a display or VNC.

There are two python scripts used for this process. The first file, `lunar_lander.py`, defines the Lunar Lander for OpenAI Gym. It also defines the keras model.

The second file, `run_lunar_lander.py`, instantiates the Lunar Lander environment and runs it.

The code that creates the model in `lunar_lander.py` is:

```
def nnmodel(input_dim):
    model = Sequential()
    model.add(Dense(32, input_dim=input_dim, activation='relu'))
    model.add(Dense(16, activation='sigmoid'))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    return model
```
 
In its current state, the model which is created is not very good and the process is very slow.

For this homework, you should adjust the model parameters and the training parameters (total iterations and threshold) to get better results. You should do a little research into how the parameters affect the resulting model. For example, is `adam` better than `adamax`? Is there a better optimizer than both of them? Are there better options for the loss and metrics paremeters of the model? Would more/denser layers help? Fewer layers?

You should try at least three different configurations (one can be the initial "base" configuration) and compare your results. The goal is to increase the number of successful landings (noted by the output "Landed it!").

**Hint: The video display/collecting does not contribute to the training of the model **

Some training parameters are in the `run_lunar_lander.py` file:

```
...
    model = nnmodel(10)

...
    training_thr = 3000
    total_itrs = 50000
...
        if steps > training_thr and steps %1000 ==0:
            # re-train a model
            print("training model model")
            modelTrained = True
            model.fit(np.array(X_train),np.array(y_train).reshape(len(y_train),1), epochs = 10, batch_size=20)
...

``` 

Some are in the `lunar_lander.py` file:

```
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
```

To run the environment, use these commands (ensure you have all the files from the hw11 github folder in your current directory):

```
sudo docker build -t lander -f Dockerfile.lander .
xhost +
sudo docker run --rm --net=host --runtime nvidia  -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix:rw --privileged -v /data/videos:/tmp/videos -v "$(pwd)":/src -it lander python3 /src/run_lunar_lander.py
```

You will have a lot of mp4 files in `/data/videos` on your TX2. You can use VLC or Chrome to watch the videos of your landing attempts to see the improvement of your model over the iterations.

## To Turn In
You should upload three videos showing your best model to Cloud Object Storage and provide links using the instructions below.

Also, submit a write-up of the tweaks you made to the model and the effect they had on the results. 
Questions to answer:
What parameters did you change? 
What values did you try?
Did you try any other changes that made things better or worse?
Did they improve or degrade the model?
Based on what you observed, what conclusions can you draw about the different parameters and their values? 

Grading is based on the changes made and the observed output, not on the accuracy of the model.

We will compare results in class.


#### Enable http access to Cloud Object Storage

```
Here's how to enable http access to the S3 COS:
1) create a bucket & upload a file, remember the resiliency you pick and the location
2) Go to Buckets -> Access Policies -> Public Access
3) click the "Create access policy" button
4) Go to Endpoint (on the left menu) and select your resiliency to find your endpoint (mine was "Regional" because that's how I created my COS)
5) Your endpoint is the Public location plus your bucket name plus the file

Example: https://s3.eu-gb.cloud-object-storage.appdomain.cloud/brooklyn-artifacts/IBM_MULTICLOUD_MANAGER_3.1.2_KLUS.tar.gz

In this example, the bucket is "brooklyn-artifacts" and the single Region is eu-gb
```
