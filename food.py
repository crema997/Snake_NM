# -*- coding: utf-8 -*-
"""
Created on Wed May 27 09:55:09 2020

@author: User
"""

from numpy.random import randint

class food(object):
    def __init__(self,rows=-1,column=-1,_x=0,_y=0):
        if rows != -1 and column !=-1:
            self.x=randint(0,rows,1)[0]
            self.y=randint(0,column,1)[0]
        else:
            self.x=_x
            self.y=_y
            
    def set_x(self,_x):
        self.x=_x
        
    def set_y(self,_y):
        self.y=_y
        
    def set_position(self, pos):
        self.x=pos[0]
        self.y=pos[1]