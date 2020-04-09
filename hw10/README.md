# Submission

Please see notebook `gym_mz.ipynb` with my edits. I changed the size of the network as well as the activation function, and was able to solve it after 549 trials.

* Model
```
# Init model
self.model = Sequential()
# the model takes four inputs as the state (cart position, velocity, stick angle, velocity at tip)
# https://github.com/openai/gym/wiki/CartPole-v0
self.model.add(Dense(128, input_dim=4, activation='elu'))
self.model.add(Dense(512, activation='elu'))
# model outputs two numbers - cumulative rewards for two available actions 
self.model.add(Dense(2, activation='linear'))
self.model.compile(loss='mse', optimizer=Adam(lr=self.alpha, decay=self.alpha_decay))
```

* Log
```
[Episode 0] - Mean survival time over last 100 episodes was 13.0 ticks.
[Episode 100] - Mean survival time over last 100 episodes was 20.82 ticks.
[Episode 200] - Mean survival time over last 100 episodes was 35.09 ticks.
[Episode 300] - Mean survival time over last 100 episodes was 68.74 ticks.
[Episode 400] - Mean survival time over last 100 episodes was 142.63 ticks.
[Episode 500] - Mean survival time over last 100 episodes was 166.04 ticks.
[Episode 600] - Mean survival time over last 100 episodes was 191.11 ticks.
Ran 649 episodes. Solved after 549 trials ✔
```

* Note: there is a bug in `display_animation`. I had to edit `/usr/local/lib/python3.6/dist-packages/matplotlib/animation.py`  
 from 

 `399         out = TextIOWrapper(BytesIO(out)).read()`

 `400         err = TextIOWrapper(BytesIO(err)).read()`

 to 

 `399         out = TextIOWrapper(BytesIO(out.encode('utf-8'))).read()`

 `400         err = TextIOWrapper(BytesIO(err.encode('utf-8'))).read()`

 for it to work. 


# Original Readme
OpenAI Gym Framework

OpenAI Gym is a framework that allows developing, training and testing of learning agents; one of it's applications is reinforcement learning, during this homework we will experiment with a Jupyter notebook aiming to train an agent to play a game using Reinforcement learning and Deep Learning.

OpenAI provides a common python interface to interact with the standarized set of environments, it is compatible with computational libraries liuke TensorFlow or Theano.

There are two basic concepts in reinforcement learning: the environment and the agent. The agent sends actions to the environment, and the environment replies with observations and rewards (that is, a score).

# General steps 
1. reset(self): Reset the environment's state. Returns observation.
2. step(self, action): Step the environment by one timestep. Returns observation, reward, done, info.
3. render(self, mode='human'): Render one frame of the environment. The default mode will do something human friendly, such as pop up a window.

More information [Gym getting started](https://gym.openai.com/docs/)


## Dockerfile instructions example
```
clone the github repo including the Docker file and the gym.ipynb in the same directory
 
Build the docker file: docker build -t gym .
Run it: docker run --name gymweek10 -d -p 8888:8888 -p 6006:6006 gym:latest
Access the Jupyter notebook endpoint: http://XX.XX.XX.XX:8888/tree?  (tip look for docker logs containerID to get the token)
Run the gym.ipynb Notebook annotate your results 
```

## Docker pull instructions
```
docker pull eariasn/w251-eariasn:hw10
Run it: docker run --name gymweek10 -d -p 8888:8888 -p 6006:6006 eariasn/w251-eariasn:hw10
Access the Jupyter notebook endpoint: http://XX.XX.XX.XX:8888/tree?  (tip look for docker logs containerID to get the token)
Run the gym.ipynb Notebook annotate your results

```
## Submission
Submit a document with evidence of the playbook run, changes you made and observations.


