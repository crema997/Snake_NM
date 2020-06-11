# -*- coding: utf-8 -*-
"""
Created on Fri May 29 15:00:02 2020

@author: User
"""
from numpy.random import randint
from random import random
from random import gauss
from grid import grid
import tkinter as tk
from tkinter import Canvas
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from keras.models import Sequential
from keras.layers import Dense, Conv1D, Flatten
#18 input neurons
#16 hidden
#8 hidden or 16 hidden
#4 final

class IA:
    
    def __init__(self):
        self.Grid=grid()
        #create model
        self.model = Sequential()
        #add model layers
        self.model.add(Conv1D(16, kernel_size=1, activation='relu', input_shape=(18,1)))
        self.model.add(Conv1D(8, kernel_size=1, activation='relu'))
        self.model.add(Flatten())
        self.model.add(Dense(4, activation='softmax'))
        
    def get_weights_as_nparray(self):
        array=self.model.get_weights()
        i=0
        Weights = np.arange(0, dtype="float32")
    
        for  x in array:    
            if i==0:
                for y in x[0][0]:
                    Weights=np.append(Weights,[y], axis=0)
                
            elif i==2:
                for y in x[0]:
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
        j=0 #counter of weights
        array=self.model.get_weights()
        
        for i,  x in enumerate(array):    
            if i==0:
                for k, y in enumerate(x[0][0]):
                    array[i][0][0][k]=weights[j]
                    j+=1
            
            elif i==2:
                for l, y in enumerate(x[0]):
                    for m, z in enumerate(y):
                        array[i][0][l][m]=weights[j]
                        j+=1
        
            elif i==4:              
                for k, y in enumerate(x):
                    for l, z in enumerate(y):
                        array[i][k][l]=weights[j]
                        j+=1
         
            elif i%2==1:
                for k, y in enumerate(x):
                    array[i][k]=weights[j]
                    j+=1
         
            
        self.model.set_weights(array)
        

    def get_points(self):
        return self.Grid.get_points()

    def set_points(self, points):
         self.Grid.set_points(points)
    
    def check_direction(self, versor): 
        boolean = True
        body_found= False
        i=1
        distance_body=50
        distance_wall=50
        while boolean:
            pos=[x + i*y for x, y in zip(self.Grid.snake.position[0], versor)]
            if pos[0]<0 or pos[0]>39 or pos[1]<0 or pos[1]>39:
                distance_wall = i-1
                boolean=False
            else:
                if self.Grid.grid [pos[0]] [pos[1]] == 1:
                    if (not body_found):
                        distance_body = i 
                        body_found=True
            i+=1
        return [distance_body, distance_wall]
                
                
                
    def calculate_distances(self):
        """calculate the distance(in x and y) between the head of the snake an the food. 
           Also looks in 8 directions to check if there is a part of the body of the snake or a wall"""
        self.Grid.update_grid()
        distances=[]
        x_dist=self.Grid.food.x-self.Grid.snake.position[0][0]
        y_dist=self.Grid.food.y-self.Grid.snake.position[0][1]
        distances.append(x_dist)
        distances.append(y_dist)
        
        #versor (1,0)
        distances+=self.check_direction([1,0])
        #versor (1,1)
        distances+=self.check_direction([1,1])
        #versor (0,1)
        distances+=self.check_direction([0,1])
        #versor (-1,1)
        distances+=self.check_direction([-1,1])
        #versor (-1,0)
        distances+=self.check_direction([-1,0])
        #versor (-1,-1)
        distances+=self.check_direction([-1,-1])
        #versor (0,-1)
        distances+=self.check_direction([0,-1])
        #versor (1,-1)
        distances+=self.check_direction([1,-1])
        
        distances_np=np.array(distances)
        return distances_np
    
    def draw(self):
        window=tk.Tk()
        window.geometry("839x839")
        window.title("prova")
        window.resizable(False,False)
        window.configure(background="black")

        c=Canvas(window,height=839,width=839,bg="black")
        c.pack()
    
        self.Grid.update_grid()
    
        squares =[[c.create_rectangle(0,0,20,20,fill="black")]*self.Grid.column for _ in [c.create_rectangle(0,0,20,20,fill="black")]*self.Grid.rows]
        for i, x in enumerate(squares):
            for j, y in enumerate(x):
                squares[i][j]=c.create_rectangle(0+21*i,0+21*j,20+21*i,20+21*j,fill="white")
        
        print (self.Grid.food.x)
        print (self.Grid.food.y)
        print (self.Grid.snake.position[0])
        self.Grid.draw(c, squares)
        
        def keypress(event, ia, c ,squares,window):
            ia.Grid
            if event.char == "a": ia.Grid.move_left()
            elif event.char == "d": ia.Grid.move_right()
            elif event.char == "w": ia.Grid.move_up()
            elif event.char == "s": ia.Grid.move_down()
    
            if ia.Grid.status==False:
                window.destroy()
       
            else:
                ia.Grid.update_grid()
                ia.Grid.draw(c, squares)
                
        window.bind("<Key>", lambda event: keypress(event, self, c, squares,window))
        window.mainloop()

        
    def predict(self, data):
        data=data.reshape(1,18,1)
        return self.model.predict([data])

    def move_up(self):
        self.Grid.move_up()
      
    def move_down(self):
        self.Grid.move_down()
        
    def move_left(self):
        self.Grid.move_left()

    def move_right(self):
        self.Grid.move_right()

    def get_food_pos(self):
        return self.Grid.get_food_pos()
    
    def draw_2(self, canvas, squares):
        self.Grid.draw(canvas,squares)






def get_points(Ia):
    return Ia.get_points()

def order_IA(ia):
    ia.sort(key=get_points, reverse=True)
    return ia

def recombination_1(array_1, array_2, cut):
    a1=array_1.copy()
    a2=array_2.copy()
    for i in range(cut):
        a1[i]=array_2[i]
        a2[i]=array_1[i]
    result=[a1,a2]
    return result
    
def recombination_2(weights):
    result = []
    pos = randint(0, len(weights),len(weights[0]))
    k=0
    
    for i, x in enumerate(pos):
        #print(weights[x][i])
        result.append(weights[x][i])
        k+=1
        
    return result
    
def mutation(weights, mutation_prob=0.01):
    """generate a mutation with a probability of 1% and a mutation that is gaussian with mean 0 and sigma 1"""
    
    array=weights.copy()

    
    for i, x in enumerate(array):
        rand_float=random()
        if rand_float < mutation_prob:
            array[i]+=gauss(0,1)
    return array
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    