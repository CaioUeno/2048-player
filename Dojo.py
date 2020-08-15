#!/usr/bin/env python
# coding: utf-8

# In[1]:


import BoardGame
import Player
from joblib import Parallel, delayed
import multiprocessing
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from keras.models import load_model


# In[2]:


def opa(i):
    d.scores[i] = d.players[i].play_game(BoardGame.board())


# In[3]:


class Darwin(object):

    def __init__(self, n=10):

        self.players = {i: Player.Player() for i in range(n)}
        self.scores = {i: 0 for i in range(n)}
        self.n = n
        self.history = []

    def trainning(self, epochs=2):

        for epoch in tqdm(range(epochs)):
            for n in range(10):
                for i in range(self.n):
                    self.scores[i] = self.players[i].play_game(BoardGame.board())

            best = min(self.scores, key=self.scores.get)
#             print('Melhor jogador: '+str(best))
#             print('Score:'+str(self.scores[best]))
            self.history.append(self.scores[best])
            self.remove_worst()
            self.reset_scores()
        self.players[max(self.scores, key=self.scores.get)].save_model()

    def remove_worst(self):

        for i in range(int(self.n * 0.9)):
            worst = min(self.scores, key=self.scores.get)
            self.players[worst].evolve()
            self.scores[worst] = np.inf

    def reset_scores(self):

        self.scores = {i: 0 for i in range(self.n)}

    def plot_history(self):

        plt.plot(self.history[-100:], color='crimson')
        plt.title('Melhor score por época')
        plt.xlabel('Época')
        plt.ylabel('Score')
        plt.grid(True)
        plt.savefig('history_scores.png')

    def get_best(self):

        return self.players[max(self.scores, key=self.scores.get)]

    def recall_players(self, n):

        self.__init__(n)
        for i in range(self.n):
            self.players[i].model = load_model('best_player.h5')
