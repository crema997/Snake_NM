# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 10:14:34 2020

@author: User
"""
from IA_GPU import IA_GPU, play, get_points, order_IA, get_score, recombination, mutation
from numba import cuda
import numpy as np
from datetime import datetime
import math
from numba.cuda.random import create_xoroshiro128p_states, xoroshiro128p_uniform_float32, xoroshiro128p_normal_float32
import sys
import os
import copy
import tkinter as tk
from tkinter import Canvas
import time


def save_best(ia_best, path):
    best_str = "/best/"
    os.mkdir(path + best_str)
    for n, ia in enumerate(ia_best):
        np.savetxt(path + best_str + str(n)+'.txt', ia.get_weights())
        np.savetxt(path + best_str + str(n)+'_moves.txt', np.int8(ia.moves_done))
        np.savetxt(path + best_str + str(n)+'_food.txt', np.int8(ia.food_pos))
        #np.savetxt(path + best_str + str(n)+'_points.txt', np.int32(get_points(ia)))

        file_object = open(path + best_str + str(n)+'_points.txt', 'a')
        file_object.write(str(get_points(ia)))
        file_object.close()

def read_best(folder):
    count=0
    best_str = "/best/"
    ia_best=[]
    while True:
        if os.path.isfile(folder+ best_str + str (count) + '.txt'):
            weights = np.loadtxt(folder+ best_str + str (count) + '.txt', dtype=np.float32)
            ia=IA_GPU()
            ia.moves_done = np.loadtxt(folder+ best_str + str (count) + '_moves.txt', dtype=np.int8)
            ia.food_pos = np.loadtxt(folder+ best_str + str (count) + '_food.txt', dtype=np.int8)
            ia.grid.points = np.loadtxt(folder+ best_str + str (count) + '_points.txt', dtype=np.int32)
            ia.set_weights(weights)
            ia_best.append(ia)
        else: 
            break
        count +=1
    return ia_best

def save_status(ia, path):
    status_str = "/status/"
    os.mkdir(path + status_str)
    for n, i in enumerate(ia):
        np.savetxt(path + status_str + str(n)+'.txt', i.get_weights())
    
def load_status(folder):
    count=0
    status_str = "/status/"
    ia=[]
    while True:
        if os.path.isfile(folder+ status_str + str (count) + '.txt'):
            weights = np.loadtxt(folder+ status_str + str (count) + '.txt', dtype=np.float32)
            ia_temp=IA_GPU()
            ia_temp.set_weights(weights)
            ia.append(ia_temp)
        else: 
            break
        count +=1
    return ia

def save_all(best_ia, status):
    now = datetime.now()
    newDirName = now.strftime("%Y_%m_%d_%H_%M")
    os.mkdir(newDirName)
    
    file_object = open('history.txt', 'a')
    file_object.write(newDirName +'\n')
    file_object.close()
    
    save_best(best_ia, newDirName)
    save_status(status, newDirName)

def start_replay(ia):
    window=tk.Tk()
    window.geometry("839x839")
    window.title("prova")
    window.resizable(False,False)
    window.configure(background="black")
    
    c=Canvas(window,height=839,width=839,bg="black")
    c.pack()      
        
    squares =[[c.create_rectangle(0,0,20,20,fill="black")]*ia.grid.column for _ in [c.create_rectangle(0,0,20,20,fill="black")]*ia.grid.rows]

    for i, x in enumerate(squares):
        for j, y in enumerate(x):
            squares[i][j]=c.create_rectangle(0+21*i,0+21*j,20+21*i,20+21*j,fill="white")

    ia.grid.set_food_pos(ia.food_pos[0])
    ia.grid.draw(c, squares)

    print(ia.food_pos)    

    for i, x in enumerate(ia.moves_done):
        ia.grid.set_food_pos(ia.food_pos[i])
        
        time.sleep(0.1)
        print(ia.moves_done[i])
        
        if ia.moves_done[i] == 3: ia.Move_left()
        elif ia.moves_done[i] == 1: ia.Move_right()
        elif ia.moves_done[i] == 0: ia.Move_up()
        elif ia.moves_done[i] == 2: ia.Move_down()
    
        if ia.grid.status==False:
            window.destroy()
       
        else:
            ia.grid.set_food_pos(ia.food_pos[i+1])
            ia.grid.Update_grid()
            ia.grid.draw(c, squares)
            window.update_idletasks()
            window.update()
        
    window.mainloop()
    
def replay(): 
    file_object = open('history.txt', 'r')
    folder_ = file_object.readlines()
    for n,i in enumerate(folder_):
        print(str(n)+ ' ' + i.rstrip())
    num = input("Which save do you want to load?\n")
    folder=folder_[int(num)].rstrip()

    ia=read_best(folder)
    while True:
        print("you have " + str(len(ia)) + " ia.", end="")
        num = input("Which one do you want to see?\nWrite -1 to close\n")
        if int(num)==-1:
            break
        else:
            start_replay(ia[int(num)])

def restart(): 
    file_object = open('history.txt', 'r')
    folder = file_object.readlines()
    for n,i in enumerate(folder):
        print(str(n)+ ' ' + i.rstrip())
    num = input("Which save do you want to load?\n")

    all_best_ia=read_best(folder[int(num)].rstrip())
    ia=load_status(folder[int(num)].rstrip())   
    tot_ia=len(ia)
    weights_number=644
    generation = len(all_best_ia)+1
    boolean = True
    best_ia_number=100
    
    while (boolean):        
        print("Generation:", end=" ")
        print(generation)
        for i in range(tot_ia):
            play(ia[i])
            print(get_points(ia[i]),end=" ")
            
        order_IA(ia)
        
        best_ia=ia[:best_ia_number]        
        all_best_ia.append(copy.deepcopy(best_ia[0]))
        
        boolean=best_ia[0].get_points()<=200
        
        print("")
        print ("score",end=" ")
        print(get_score(best_ia[0]))
        print("moves_left",end=" ")
        print(best_ia[0].grid.moves_left)
        print ("points",end=" ")
        print(get_points(best_ia[0]))
        
        new_weights_gpu_mem =  cuda.device_array((tot_ia, 644))
        buff=[]
        for i in range(best_ia_number): 
            buff.append(best_ia[i].get_weights())
        
        old_weights=np.array(buff)
        old_weights_gpu_mem=cuda.to_device(old_weights)
        dt = datetime.now()
        
        #print(dt)
        rng_states = create_xoroshiro128p_states(1*tot_ia, seed=dt.microsecond)
        rng_states_2 = create_xoroshiro128p_states(644*tot_ia, seed=dt.microsecond)
        recombination[1,tot_ia](old_weights_gpu_mem, new_weights_gpu_mem, best_ia_number, tot_ia, 644, rng_states)
        #recombination_2[tot_ia,644](old_weights_gpu_mem, new_weights_gpu_mem, best_ia_number, tot_ia, 644, rng_states_2)
        
        #print(dt)
        dt = datetime.now()
        rng_states = create_xoroshiro128p_states(644*tot_ia, seed=dt.microsecond)
        mutation[tot_ia,644](new_weights_gpu_mem, tot_ia, 644, rng_states,0.1)
        
        new_weights=new_weights_gpu_mem.copy_to_host()
        
        for i in range(tot_ia):
            ia[i].set_weights(np.array(new_weights[i]))
        
        if not generation%100:
            print("\nsaving all")
            save_all(all_best_ia, ia)
         
        if not boolean:
            save_all(all_best_ia, ia)
            
        for i in range(tot_ia):
            ia[i].restart()
        
       
        generation+=1
    
def start():
    tot_ia=1000
    ia=[IA_GPU()]*tot_ia
    best_ia_number=100
    weights_number=644
    all_best_ia=[]
    for i in range(tot_ia):
        ia[i]=IA_GPU()
        ia[i].fill_layers()
    boolean = True
    generation=1
    while (boolean):        
        print("Generation:", end=" ")
        print(generation)
        for i in range(tot_ia):
            play(ia[i])
            print(get_points(ia[i]),end=" ")
            
        order_IA(ia)
        
        best_ia=ia[:best_ia_number]        
        all_best_ia.append(copy.deepcopy(best_ia[0]))
        
        boolean=best_ia[0].get_points()<=200
        
        print("")
        print ("score",end=" ")
        print(get_score(best_ia[0]))
        print("moves_left",end=" ")
        print(best_ia[0].grid.moves_left)
        print ("points",end=" ")
        print(get_points(best_ia[0]))
        
        new_weights_gpu_mem =  cuda.device_array((tot_ia, 644))
        buff=[]
        for i in range(best_ia_number): 
            buff.append(best_ia[i].get_weights())
        
        old_weights=np.array(buff)
        old_weights_gpu_mem=cuda.to_device(old_weights)
        dt = datetime.now()
        
        rng_states = create_xoroshiro128p_states(1*tot_ia, seed=dt.microsecond)
        rng_states_2 = create_xoroshiro128p_states(644*tot_ia, seed=dt.microsecond)
        recombination[1,tot_ia](old_weights_gpu_mem, new_weights_gpu_mem, best_ia_number, tot_ia, 644, rng_states)
        #recombination_2[tot_ia,644](old_weights_gpu_mem, new_weights_gpu_mem, best_ia_number, tot_ia, 644, rng_states_2)
        
        dt = datetime.now()
        rng_states = create_xoroshiro128p_states(644*tot_ia, seed=dt.microsecond)
        mutation[tot_ia,644](new_weights_gpu_mem, tot_ia, 644, rng_states,0.1)
        
        new_weights=new_weights_gpu_mem.copy_to_host()
        

        for i in range(tot_ia):
            ia[i].set_weights(np.array(new_weights[i]))
        
        if not generation%100:
            print("\nsaving all")
            save_all(all_best_ia, ia)
         
        if not boolean:
            save_all(all_best_ia, ia)    
         
        for i in range(tot_ia):
            ia[i].restart()
        
        generation+=1
    
#start()
#restart()
replay()