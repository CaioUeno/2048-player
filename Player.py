#!/usr/bin/env python
# coding: utf-8

# In[22]:


from keras.layers import Input, Dense, LSTM, Flatten
from keras.models import Model
import BoardGame
import numpy as np
from joblib import Parallel, delayed
import multiprocessing
import pickle


# In[29]:


class Player(object):

    def __init__(self):

        self.prob = 0.75
        self.score = 0

        in_layer = Input((4,4), name='in_layer')
        lstm_layer_1 = LSTM(4, return_sequences=True, name='lstm_layer_1')(in_layer)
        lstm_layer_2 = LSTM(2, return_sequences=True, name='lstm_layer_2')(lstm_layer_1)
        dense_layer_1 = Dense(2, activation='tanh', name='dense_layer_1')(lstm_layer_2)
        flatten_layer = Flatten(name='flatten_layer')(dense_layer_1)
        dense_layer_2 = Dense(4, activation='tanh', name='dense_layer_2')(flatten_layer)
        out_layer = Dense(4, activation='sigmoid', name='out_layer')(dense_layer_2)

        self.model = Model(inputs=in_layer, outputs=out_layer)
        self.model.compile(optimizer='adam', loss='categorical_crossentropy')

    def one_play(self, board):

        pred = np.argmax(self.model.predict([[board.board]]))
        if pred == 0:
            board.move_left()
        elif pred == 1:
            board.move_up()
        elif pred == 2:
            board.move_down()
        else:
            board.move_right()

        self.score = self.compute_score()
#         print(board.board)

    def random_play(self, board):
        movement = np.random.choice([board.move_left, board.move_right,
                                     board.move_up, board.move_down])
        movement()
        self.score -= self.score // 10

    def compute_score(self):

        return self.score + 1

    def evolve(self):

        for layer in self.model.layers[1:]:
            weights_and_bias = []
            for params in layer.get_weights():
                new_params = params
                new_params += np.random.uniform(-1, 1, size=params.shape) *                                np.random.choice([True, False], size=params.shape,
                                                p=[self.prob, 1-self.prob])
                weights_and_bias.append(new_params)
            layer.set_weights(weights_and_bias)

    def save_model(self):

        self.model.save('best_player.h5')

    ## API to trainning

    def play_game(self, board, delay=False):

        while not board.check_endgame():
            board_aux = board.board.copy()
            self.one_play(board)
            while (board.board == board_aux).all() and board.can_move():
                self.random_play(board)

            if not board.can_move():
                break

        self.score += np.max(board.board)
        if delay:
            print(board.board)
        return self.score
