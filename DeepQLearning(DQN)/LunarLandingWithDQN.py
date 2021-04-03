import gym
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import random

class DQLAgent:
    def __init__(self, env):
        # parameter / hyperparameter
        self.state_size = env.observation_space.shape[0]
        self.action_size = env.action_space.n
        
        self.gamma = 0.99
        self.learning_rate = 0.001
        
        self.epsilon = 1 #explore
        self.epsilon_decay = 0.9993
        self.epsilon_min = 0.01
        
        self.memory = deque(maxlen = 4000)
        
        self.model = self.build_model()
        self.target_model = self.build_model()
    
    def build_model(self):
        # neural network for deep q learning
        model = Sequential()
        model.add(Dense(64, input_dim=self.state_size, activation="relu"))
        model.add(Dense(64, activation="relu"))
        model.add(Dense(self.action_size, activation="linear"))
        model.compile(loss="mse", optimizer=Adam(lr=self.learning_rate))
        return model
    
    def remember(self, state, action, reward, next_state, done):
        # storage
        self.memory.append((state, action, reward, next_state, done))
    
    def act(self, state):
        # acting explore or exploit
        if np.random.rand() <= self.epsilon:
            return np.random.choice(self.action_size)
        act_values = self.model.predict(s)
        return np.argmax(act_values[0])
    
    def replay(self,batch_size):
        "vectorized replay method"
        if len(agent.memory) < batch_size:
            return
        # Vectorized method for experience replay
        minibatch = random.sample(self.memory, batch_size)
        minibatch = np.array(minibatch)
        not_done_indices = np.where(minibatch[:, 4] == False)
        y = np.copy(minibatch[:, 2])

        # If minibatch contains any non-terminal states, use separate update rule for those states
        if len(not_done_indices[0]) > 0:
            predict_sprime = self.model.predict(np.vstack(minibatch[:, 3]))
            predict_sprime_target = self.target_model.predict(np.vstack(minibatch[:, 3]))
            
            # Non-terminal update rule
            y[not_done_indices] += np.multiply(self.gamma, predict_sprime_target[not_done_indices, np.argmax(predict_sprime[not_done_indices, :][0], axis=1)][0])
        
        actions = np.array(minibatch[:, 1], dtype=int)
        y_target = self.model.predict(np.vstack(minibatch[:, 0]))
        y_target[range(batch_size), actions] = y
        self.model.fit(np.vstack(minibatch[:, 0]), y_target, epochs=1, verbose=0)
            
    def adaptiveEGreedy(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
            
    def targetModelUpdate(self):
        self.target_model.set_weights(self.model.get_weights())

# initialize env and egent
env = gym.make("LunarLander-v2")
agent = DQLAgent(env)
state_number = env.observation_space.shape[0]

batch_size = 32
episodes = 50000
for e in range(episodes):
    
    # initialize environment
    state = env.reset()
    state = np.reshape(state, [1, state_number])
    
    total_reward = 0
    for time in range(1000):
        
        # env.render()
        
        # act
        action = agent.act(state) # select an action
        
        # step
        next_state, reward, done, _ = env.step(action)
        next_state = np.reshape(state, [1, state_number])
        
        # remember / storage
        agent.remember(state, action, reward, next_state, done)
        
        # update state
        state = next_state
        
        # replay
        agent.replay(batch_size)
        
        total_reward += reward
        
        if done:
            agent.targetModelUpdate()
            break
    
    # adjust epsilon
    agent.adaptiveEGreedy()
    
    print("Episode: {}, Reward: {}".format(e, total_reward))

# test
import time
trained_model = agent
state = env.reset()
state = np.reshape(state, [1, env.observation_space.shape[0]])
while True:
    env.render()
    action = trained_model.act(state)
    next_state, reward, done, _ = env.step(action)
    next_state = np.reshape(next_state, [1, env.observation_space.shape[0]])
    state = next_state
    
    if done:
        break
print("Done")