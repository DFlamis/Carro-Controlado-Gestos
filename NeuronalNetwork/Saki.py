from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers.core import Dense
import random
import numpy as np
import collections

class QLAgent(object):
    def __init__(self, params):
        self.reward = 0  # recompensa
        self.gamma = 0.9  # parametro de confianza
        self.short_memory = np.array([])  # memoria de estados a corto plazo
        self.agent_target = 1  # inicializacion del target
        self.agent_predict = 0  # inicializacion de las predicciones
        self.learning_rate = params['learning_rate']  # tasa de aprendizaje de la red
        self.epsilon = 1  # parametro que controla la aleatoriedad de las acciones
        self.first_layer = params['first_layer_size']  # neuronas 1ra capa oculta
        self.second_layer = params['second_layer_size']  # neuronas 2ra capa oculta
        self.memory = collections.deque(maxlen=params['memory_size'])  # para guardar estados y acciones en memoria
        self.weights = params['weights_path']  # pesos de la red
        self.load_weights = params['load_weights']  # para cargar red pre-entrenada
        self.model = self.network()  # iniciamos el modelo

    def network(self):
        model = Sequential()
        model.add(Dense(activation="relu", input_dim=4, units=self.first_layer))
        model.add(Dense(activation="relu", units=self.second_layer))
        model.add(Dense(activation="softmax", units=3))
        
        opt = Adam(self.learning_rate)
        model.compile(loss='mse', optimizer=opt)

        if self.load_weights:
            model.load_weights(self.weights)
        return model

    def get_state(self, crash, sensors):
        state = [
            1 - sensors[0],
            1 - sensors[1],
            1 - sensors[2],
            crash
        ]

        return np.asarray(state)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay_new(self, memory, batch_size):
        if len(memory) > batch_size:
            minibatch = random.sample(memory, batch_size)
        else:
            minibatch = memory
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(np.array([next_state]))[0])
            target_f = self.model.predict(np.array([state]))
            target_f[0][np.argmax(action)] = target
            self.model.fit(np.array([state]), target_f, epochs=1, verbose=0)

    def train_short_memory(self, state, action, reward, next_state, done):
        target = reward
        if not done:
            target = reward + self.gamma * np.amax(self.model.predict(next_state.reshape((1, -1)))[0])
        target_f = self.model.predict(state.reshape((1, -1)))
        target_f[0][np.argmax(action)] = target
        self.model.fit(state.reshape((1, -1)), target_f, epochs=1, verbose=0)