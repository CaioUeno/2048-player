#!/usr/bin/env python
# coding: utf-8

# In[42]:


import numpy as np


# In[61]:


class board(object):
    
    def __init__(self):
        self.board = np.random.randint(0, 2, size=(4, 4)) * 2
        self.old_board = np.random.randint(5, 10, size=(4, 4)) * 2
        self.beta = 0.9
        self.min_elem = 2
        self.spam_flag = False
            
    def move_left(self, up=False):
        if not up:
            self.old_board = self.board.copy()
        for persistance in range(4):
            for line in range(4):
                for column in range(3):
                    if self.board[line][column] == self.board[line][column+1] or                                                         self.board[line][column] == 0:
                        self.board[line][column] += self.board[line][column+1]
                        self.board[line][column+1] = 0
        self.att_board()
    
    def move_right(self, down=False):
        if not down:
            self.old_board = self.board.copy()
        for persistance in range(4):
            for line in range(4):
                for column in range(1, 4):
                    if self.board[line][column] == self.board[line][column-1] or                                                         self.board[line][column] == 0:
                        self.board[line][column] += self.board[line][column-1]
                        self.board[line][column-1] = 0
        self.att_board()
                        
    def move_up(self):
        self.old_board = self.board.copy()
        self.board = self.board.T
        self.move_left(up=True)
        self.board = self.board.T
        self.att_board()
        
    def move_down(self):
        self.old_board = self.board.copy()
        self.board = self.board.T
        self.move_right(down=True)
        self.board = self.board.T
        self.att_board()
        
    def spam_elements(self):
        prob = np.random.random((4,4))
        prob = prob * (prob >= self.beta) * (self.board == 0)
        prob = prob.astype(bool) * self.min_elem
        if not prob.any():
            self.spam_flag = True
        else:
            self.spam_flag = False
        self.board += prob
        
    def att_board(self):
        self.spam_elements()
        if self.spam_flag:
            self.beta -= 0.1
        else:
            self.beta += 0.2
            
    def check_endgame(self):
        
        return (self.board == self.old_board).all() and (self.board != 0).all()
    
    def can_move(self):
        
        movements = [self.move_left, self.move_right, 
                     self.move_up, self.move_down]
        for move in movements:
            board_aux = self.board.copy()
            old_board_aux = self.old_board.copy() 
            move()
#             print(board_aux)
#             print(self.board)
#             print((board_aux != self.board).any())
            Flag = (board_aux != self.board).any()
            self.board = board_aux.copy()
            self.old_board = old_board_aux.copy()
            if Flag:
                return Flag
        return False

