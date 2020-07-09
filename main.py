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
#import datetime
import sys
import os



def save_best(ia_best, path):
    best_str = "/best/"
    os.mkdir(path + best_str)
    for n, i in enumerate(ia_best):
        np.savetxt(path + best_str + str(n)+'.txt', i.get_weights())
    
def read_best(folder):
    count=0
    best_str = "/best/"
    ia_best=[]
    while True:
        if os.path.isfile(folder+ best_str + str (count) + '.txt'):
            weights = np.loadtxt(folder+ best_str + str (count) + '.txt', dtype=np.float32)
            ia=IA_GPU()
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
    save_best(best_ia, newDirName)
    save_status(status, newDirName)





















def main():
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
        all_best_ia.append(best_ia[0])        
        if generation%5:
            print("\nsaving all")
            save_all(all_best_ia, ia)
        
        boolean=best_ia[0].get_points()<=10
        
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
        
        #print(new_weights)
        #prova=new_weights[0]
        #print("")
        #print(prova)
        for i in range(tot_ia):
            ia[i].set_weights(np.array(new_weights[i]))
            ia[i].restart()
        generation+=1
        #boolean=False
        
    print (all_best_ia)
main()