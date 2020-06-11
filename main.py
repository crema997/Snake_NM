# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 10:14:34 2020

@author: User
"""
from numba import cuda
import numpy as np
import time
from IA import IA
from IA import order_IA 
from numpy.random import randint
from IA import recombination_1
from IA import mutation
from IA import get_points
import gc

def play(ia, moves_done, food_pos):
    #0=up, 1=right, 2=down, 3=left

    while ia.Grid.status:
        food_pos.append(ia.get_food_pos())
        distances = ia.calculate_distances()
        prediction=ia.predict(distances)
    
        result = np.where(prediction[0] == np.amax(prediction[0]))
        
        if result[0][0]==0:
            ia.move_up()
            moves_done.append(0)
        elif result[0][0]==1:
            ia.move_right()
            moves_done.append(1)
        elif result[0][0]==2:
            ia.move_down()
            moves_done.append(2)
        elif result[0][0]==3:
            ia.move_left()
            moves_done.append(3)
       
    

def main():
    ia_arr= []
    food_pos=[[]]*100
    moves_done=[[]]*100
    
    #print(food_pos)
    #print(moves_done)
    
    for i in range (100):
        ia_arr.append(IA())
        print(i)

    for i, x in enumerate(ia_arr):
        play(ia_arr[i],moves_done[i],food_pos[i])
        print(get_points(ia_arr[i]))
        
    order_IA(ia_arr)
    
    best_ia=ia_arr[:10]
    new_ia=[]
    for i in range(100):
        values = randint(0, 10, 2)
        cut =randint(0, best_ia[values[0]].get_weights_as_nparray().size, 1)
        
        w1=best_ia[values[0]].get_weights_as_nparray()
        w2=best_ia[values[1]].get_weights_as_nparray()
        
        
        
        buff=recombination_1(w1, w2, cut[0])
        buff=mutation(buff[0])
        new_ia.append(IA())
        new_ia[i].set_weights_as_nparray(buff)
        print(i)
        
        
def main2():
    ia_number=100
    ia_arr= []
    food_pos=[[]]*ia_number
    moves_done=[[]]*ia_number
    boolean=True
    for i in range (ia_number):
        ia_arr.append(IA())
        print(i)
    #print(food_pos)
    #print(moves_done)
    while(boolean):

        for i, x in enumerate(ia_arr):
            play(ia_arr[i],moves_done[i],food_pos[i])
            print(get_points(ia_arr[i]),end=" ")
        
        print("\n")   
        order_IA(ia_arr)
        
        best_ia=ia_arr[:10]
        boolean=best_ia[0].get_points()<=30
        print ("points",end=" ")
        print(best_ia[0].get_points())
        new_ia=[]
        for i in range(ia_number):
            values = randint(0, 10, 2)
            cut =randint(0, best_ia[values[0]].get_weights_as_nparray().size, 1)
            
            w1=best_ia[values[0]].get_weights_as_nparray()
            w2=best_ia[values[1]].get_weights_as_nparray()
            
            buff=recombination_1(w1, w2, cut[0])
            buff=mutation(buff[0])
            new_ia.append(IA())
            new_ia[i].set_weights_as_nparray(buff)
            print(i,end=" ")
        print("\n")  
        ia_arr=new_ia.copy()
        gc.collect()


main2()