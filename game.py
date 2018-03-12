import thinice as ThinIce
#from IPython.display import clear_output
import random
import numpy as np


from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop

#state = ThinIce.initGrid()
#print(ThinIce.dispGrid(state))

#state = ThinIce.makeMove(state, 2) #Left 1 unit
#state = ThinIce.makeMove(state, 3) #Right 1 unit
#state = ThinIce.makeMove(state, 1) #Down 1 unit
# state = ThinIce.makeMove(state, 2) #Left 1 unit
# state = ThinIce.makeMove(state, 2) #Left 1 unit
# state = ThinIce.makeMove(state, 0) #Up 1 unit
# state = ThinIce.makeMove(state, 0) #Up 1 unit


# print('Reward: %s' % (ThinIce.getReward(state),))
# print(ThinIce.dispGrid(state))


model = Sequential()
model.add(Dense(164, input_shape=(64,), kernel_initializer="lecun_uniform"))
model.add(Activation('relu'))
#model.add(Dropout(0.2)) I'm not using dropout, but maybe you wanna give it a try?

model.add(Dense(150, kernel_initializer="lecun_uniform"))
model.add(Activation('relu'))
#model.add(Dropout(0.2))

model.add(Dense(4, kernel_initializer="lecun_uniform"))
model.add(Activation('linear')) #linear output so we can have range of real-valued outputs

rms = RMSprop()
model.compile(loss='mse', optimizer=rms, metrics=['accuracy'])

#print(model.predict(state.reshape(1,64), batch_size=1))


epochs = 100
gamma = 0.95 #since it may take several moves to goal, making gamma high
epsilon = 1
for i in range(epochs):
    
    state = ThinIce.initGrid()
    status = 1
    #while game still in progress
    while(status == 1):
        #We are in state S
        #Let's run our Q function on S to get Q values for all possible actions
        qval = model.predict(state.reshape(1,64), batch_size=1, verbose=1,steps=None)
        if (random.random() < epsilon): #choose random action
            action = np.random.randint(0,4)
        else: #choose best action from Q(s,a) values
            action = (np.argmax(qval))
        #Take action, observe new state S'
        new_state = ThinIce.makeMove(state, action)
        #Observe reward
        if(new_state == state).all():
            reward = -1
        else:
            reward = ThinIce.getReward(new_state)


        #Get max_Q(S',a)
        newQ = model.predict(new_state.reshape(1,64), batch_size=1, verbose=1, steps=None)
        print(newQ)
        maxQ = np.max(newQ)
        y = np.zeros((1,4))
        y[:] = qval[:]
        if (reward == 1 or reward == -1): #non-terminal state
            update = (reward + (gamma * maxQ))
        else: #terminal state
            update = reward

        y[0][action] = update #target output
        print("Game #: %s" % (i,))
        history = model.fit(state.reshape(1,64), y, batch_size=1, nb_epoch=1, verbose=1)
        state = new_state
        print('Reward: %s' % (reward,))
        if (reward != 1 and reward != -1):
            status = 0
        print(ThinIce.dispGrid(state))
        #clear_output(wait=True)
    if epsilon > 0.1:
        epsilon -= (1/epochs)


# print(state) 

