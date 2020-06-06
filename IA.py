# -*- coding: utf-8 -*-
"""
Created on Fri May 29 15:00:02 2020

@author: User
"""
from grid import grid
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten
#18 input neurons
#16 hidden
#8 hidden or 16 hidden
#4 final

class IA(object):
    
    def __init__(self):
        self.Grid=grid()
        
        #create model
        self.model = Sequential()
        #add model layers
        self.model.add(Conv2D(16, kernel_size=1, activation='relu', input_shape=(18,1,1)))
        self.model.add(Conv2D(8, kernel_size=1, activation='relu'))
        self.model.add(Flatten())
        self.model.add(Dense(4, activation='softmax'))
        
    def get_weights_as_nparray(self):
        array=self.model.get_weights()
        i=0
        Weights = np.arange(0, dtype="float32")
    
        for  x in array:    
            if i==0:
                for y in x[0][0][0]:
                    Weights=np.append(Weights,[y], axis=0)
                
            elif i==2:
                for y in x[0][0]:
                    for z in y:
                        Weights=np.append(Weights,[z], axis=0)
            elif i == 4:
                for y in x:
                    for z in y:
                        Weights=np.append(Weights,[z], axis=0)
            elif i%2==1:
                for y in x:
                    Weights=np.append(Weights,[y], axis=0)
            i+=1
        
        return Weights
    
    def set_weights_as_nparray(self, weights):
        i=0
        j=0 #counter of weights
        array=self.model.get_weights()
        
        for  x in array:    
            if i==0:
                k=0
                for y in x[0][0][0]:
                    array[i][0][0][0][k]=weights[j]
                    j+=1
                    k+=1
            
            elif i==2:
                k=0
                
                for y in x[0][0]:
                    l=0
                    for z in y:
                        array[i][0][0][k][l]=weights[j]
                        j+=1
                        l+=1
                    k+=1
                    
            elif i==4:
                k=0
               
                for y in x:
                    l=0
                    for z in y:
                        array[i][k][l]=weights[j]
                        l+=1
                        j+=1
                    k+=1
                    
            elif i%2==1:
                k=0
                
                for y in x:
                    array[i][k]=weights[j]
                    k+=1
                    j+=1
         
            
            i+=1
        self.model.set_weights(array)
        

    def get_points(self):
        return self.Grid.get_points()

    def set_points(self, points):
         self.Grid.set_points(points)
         
         
def get_point(Ia):
    return Ia.get_points()

def order_IA(ia):
    ia.sort(key=get_point, reverse=True)
    return ia