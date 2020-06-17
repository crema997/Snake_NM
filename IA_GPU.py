# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 10:36:19 2020

@author: User
"""

from __future__ import print_function, absolute_import
from grid import grid
from numba import cuda
from numba.cuda.random import create_xoroshiro128p_states, xoroshiro128p_uniform_float32
import numpy as np
from datetime import datetime
import math
from scipy.special import expit

@cuda.jit 
def fill_random(arr, size, rng_states):
    pos = cuda.grid(1)
    if pos < size:
       arr[pos]=xoroshiro128p_uniform_float32(rng_states, cuda.grid(1))*2.-1.

@cuda.jit
def scalar(vector,matrix,result,size):
    pos = cuda.grid(1)
    if pos<size:
        result[pos]=(matrix[pos]*vector).sum()

@cuda.jit
def matmul(A, B, C):
    """Perform matrix multiplication of C = A * B
    """
    row, col = cuda.grid(2)
    if row < C.shape[0] and col < C.shape[1]:
        tmp = 0.
        for k in range(A.shape[1]):
            tmp += A[row, k] * B[k, col]
        C[row, col] = tmp

@cuda.jit
def recombination(inp_weights, out_weights, inp_ia, tot_ia, n_weights, rng_states):#inp_ia: number of ia in input, tot_ia: total number of ia to be generated, n_weights: total number of weighta for ia
    pos = cuda.grid(1)
    if pos < tot_ia:
        ia_1= int(xoroshiro128p_uniform_float32(rng_states, cuda.grid(1)) * inp_ia)
        ia_2= int(xoroshiro128p_uniform_float32(rng_states, cuda.grid(1)) * inp_ia)
        cut= int(xoroshiro128p_uniform_float32(rng_states, cuda.grid(1)) * n_weights)
        for i in range(n_weights):
            if i < cut:
                out_weights[pos][i]=inp_weights[ia_1][i]
            else:
                out_weights[pos][i]=inp_weights[ia_2][i]

@cuda.jit
def mutation(inp_weights, n_ia, n_weights, rng_states, prob=0.1):
    # Thread id in a 1D block
    tx = cuda.threadIdx.x
    # Block id in a 1D grid
    ty = cuda.blockIdx.x
    if ty<n_ia and tx<n_weights:
        a=xoroshiro128p_uniform_float32(rng_states, cuda.grid(1))
        #print(a)
        if a<prob:
            inp_weights[ty][tx]+=(xoroshiro128p_uniform_float32(rng_states, cuda.grid(1))*2-1)
    



class IA_GPU:
    def __init__(self, nodes_in_layer=[18,16,8,4]):
        self.grid=grid()
        self.layers=4
        self.nodes_in_layer=nodes_in_layer
        self.weights_layer_2=np.array([
                [0.]*(18+1)
            ]*16)
        self.weights_layer_3=np.array([
                [0.]*(16+1)
            ]*8)
        self.weights_layer_4=np.array([
                [0.]*(8+1)
            ]*4)
        
    def fill_layers(self):
        blocks=1
        
        threads_per_block=19
        dt = datetime.now()
        #print (dt)
        rng_states = create_xoroshiro128p_states(threads_per_block * blocks, seed=dt.microsecond)
        for i, x in enumerate(self.weights_layer_2):
            fill_random[1,threads_per_block](self.weights_layer_2[i], 19, rng_states)
            
        threads_per_block=17
        dt = datetime.now()
        rng_states = create_xoroshiro128p_states(threads_per_block * blocks, seed=dt.microsecond)
        for i, x in enumerate(self.weights_layer_3):
            fill_random[1,threads_per_block](self.weights_layer_3[i], 17, rng_states)
           
        threads_per_block=9
        dt = datetime.now()
        rng_states = create_xoroshiro128p_states(threads_per_block * blocks, seed=dt.microsecond)
        for i, x in enumerate(self.weights_layer_4):
            fill_random[1,threads_per_block](self.weights_layer_4[i], 9, rng_states)


    def get_weights(self):
        w_layer2=np.reshape(self.weights_layer_2,(304))
        #print(w_layer2)
        w_layer3=np.reshape(self.weights_layer_3,(136))
        #print(w_layer3)
        w_layer4=np.reshape(self.weights_layer_4,(36))
        #print(w_layer4)
        return np.concatenate((w_layer2,w_layer3,w_layer4),axis=None)
    
    def set_weights(self, weights):#weights must be a 1D np array
        w_layer2=np.array(weights[:304])
        self.weights_layer_2=np.reshape(w_layer2,(16,19))
        
        w_layer3=np.array(weights[304:304+136])
        self.weights_layer_3=np.reshape(w_layer3,(8,17))
        
        w_layer4=np.array(weights[304+136:])
        self.weights_layer_4=np.reshape(w_layer4,(4,9))
       
    def predict_2(self, input_arr):
        layer_2=np.array([0.]*16)
        scalar[1,16](np.append(input_arr,[1]), self.weights_layer_2,layer_2, 16)
        
        layer_3=np.array([0.]*8)
        scalar[1,8](np.append(layer_2,[1]), self.weights_layer_3,layer_3, 8)
        
        layer_4=np.array([0.]*4)
        scalar[1,16](np.append(layer_3,[1]), self.weights_layer_3,layer_4, 4)

        return np.where(layer_4 == np.amax(layer_4))

    def predict(self, input_arr):  #TODO, no sigmoid function
        #print(input_arr)
        arr=np.append(input_arr,[[1.]],0)
        A_global_mem = cuda.to_device(self.weights_layer_2)
        B_global_mem = cuda.to_device(arr)
        C_global_mem = cuda.device_array((16, 1))
        threadsperblock = (16, 16)
        blockspergrid_x = int(math.ceil(self.weights_layer_2.shape[0] / threadsperblock[0]))
        blockspergrid_y = int(math.ceil(arr.shape[1] / threadsperblock[1]))
        blockspergrid = (blockspergrid_x, blockspergrid_y)
        # Start the kernel 
        matmul[blockspergrid, threadsperblock](A_global_mem, B_global_mem, C_global_mem) #calculated values of second layer
        C = C_global_mem.copy_to_host()
        #print(C)
        #print("")
        #for i in range(16):
        #    C[i][0]=expit(C[i][0])
        #print(C)
        
        arr=np.append(C,[[1.]],0)
        A_global_mem = cuda.to_device(self.weights_layer_3)
        B_global_mem = cuda.to_device(arr)    
        C_global_mem = cuda.device_array((8, 1))
        blockspergrid_x = int(math.ceil(self.weights_layer_3.shape[0] / threadsperblock[0]))
        blockspergrid_y = int(math.ceil(arr.shape[1] / threadsperblock[1]))
        blockspergrid = (blockspergrid_x, blockspergrid_y)
        matmul[blockspergrid, threadsperblock](A_global_mem, B_global_mem, C_global_mem) #calculated values of third layer
   
        C = C_global_mem.copy_to_host()
        #print(C)
        #print("")
        #for i in range(8):
        #    C[i][0]=expit(C[i][0])
        #print(C)
        
        arr=np.append(C,[[1.]],0)
        A_global_mem = cuda.to_device(self.weights_layer_4)
        B_global_mem = cuda.to_device(arr)
        C_global_mem = cuda.device_array((4, 1))
        blockspergrid_x = int(math.ceil(self.weights_layer_3.shape[0] / threadsperblock[0]))
        blockspergrid_y = int(math.ceil(arr.shape[1] / threadsperblock[1]))
        blockspergrid = (blockspergrid_x, blockspergrid_y)
        matmul[blockspergrid, threadsperblock](A_global_mem, B_global_mem, C_global_mem) #calculated values of the last layer
    
        # Copy the result back to the host
        C = C_global_mem.copy_to_host()
        #print (C)
        C=np.reshape(C,(4))
        #print (C)
        
        return np.where(C == np.amax(C))

    def check_direction(self, versor): 
        boolean = True
        body_found= False
        i=1
        distance_body=50
        distance_wall=50
        while boolean:
            pos=[x + i*y for x, y in zip(self.grid.snake.position[0], versor)]
            if pos[0]<0 or pos[0]>39 or pos[1]<0 or pos[1]>39:
                distance_wall = i-1
                boolean=False
            else:
                if self.grid.grid [pos[0]] [pos[1]] == 1:
                    if (not body_found):
                        distance_body = i 
                        body_found=True
            i+=1
        return [distance_body, distance_wall]

    def calculate_distances(self):
        """calculate the distance(in x and y) between the head of the snake an the food. 
           Also looks in 8 directions to check if there is a part of the body of the snake or a wall"""
        self.grid.update_grid()
        distances=[]
        x_dist=self.grid.food.x-self.grid.snake.position[0][0]
        y_dist=self.grid.food.y-self.grid.snake.position[0][1]
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
        
        distances_np=np.array([distances])
        return distances_np
    
    def move_up(self):
        self.grid.move_up()
      
    def move_down(self):
        self.grid.move_down()
        
    def move_left(self):
        self.grid.move_left()

    def move_right(self):
        self.grid.move_right()

    def get_points(self):
        return self.grid.get_points()

    def get_food_pos(self):
        return self.grid.get_food_pos()
    
    
def get_points(Ia):
    return Ia.get_points()

def order_IA(ia):
    ia.sort(key=get_points, reverse=True)
    return ia

def play(ia, moves_done, food_pos):
    #0=up, 1=right, 2=down, 3=left

    while ia.grid.status:
        food_pos.append(ia.get_food_pos())
        distances = ia.calculate_distances()
        distances = np.reshape(distances, (18,1))
        result = ia.predict(distances)
        
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
    tot_ia=1000
    food_pos=[[]]*tot_ia
    moves_done=[[]]*tot_ia
    ia=[IA_GPU()]*tot_ia
    for i in range(tot_ia):
        ia[i].fill_layers()
    boolean = True
    generation=1
    while (boolean):
        print("Generation:", end=" ")
        print(generation)
        for i, x in enumerate(ia):
            play(ia[i],moves_done[i],food_pos[i])
            #print(get_points(ia[i]),end=" ")
        
        order_IA(ia)
        
        best_ia=ia[:10]
        boolean=best_ia[0].get_points()<=30
        print("")
        print ("points",end=" ")
        print(best_ia[0].get_points())
        new_weights_gpu_mem =  cuda.device_array((tot_ia, 476))
        buff=[]
        for i in range(tot_ia): 
            buff.append(ia[i].get_weights())
        old_weights=np.array(buff)
        old_weights_gpu_mem=cuda.to_device(old_weights)
        dt = datetime.now()
        rng_states = create_xoroshiro128p_states(1*tot_ia, seed=dt.microsecond)
        recombination[1,tot_ia](old_weights_gpu_mem, new_weights_gpu_mem, 10, tot_ia, 476, rng_states)
        rng_states = create_xoroshiro128p_states(476*tot_ia, seed=dt.microsecond)
        mutation[tot_ia,476](new_weights_gpu_mem, tot_ia, 476, rng_states,0.1)
        
        new_weights=new_weights_gpu_mem.copy_to_host()
        for i in range(tot_ia):
            ia[i].set_weights(new_weights[i])
        generation+=1
#main()




def main_2():
    tot_ia=1000
    food_pos=[[]]*tot_ia
    moves_done=[[]]*tot_ia
    ia=[IA_GPU]*tot_ia
    for i in range(tot_ia):
        ia[i]=IA_GPU()
        ia[i].fill_layers()
    boolean = True
    generation=1

    print("Generation:", end=" ")
    print(generation)
    for i in range(tot_ia):
        play(ia[i],moves_done[i],food_pos[i])
        print(get_points(ia[i]),end=" ")
        
    order_IA(ia)
        
    best_ia=ia[:10]
    boolean=best_ia[0].get_points()<=30
    print("")
    print ("points",end=" ")
    print(best_ia[0].get_points())
    new_weights_gpu_mem =  cuda.device_array((tot_ia, 476))
    buff=[]
    for i in range(tot_ia): 
        buff.append(ia[i].get_weights())
    old_weights=np.array(buff)
    old_weights_gpu_mem=cuda.to_device(old_weights)
    dt = datetime.now()
    rng_states = create_xoroshiro128p_states(1*tot_ia, seed=dt.microsecond)
    recombination[1,tot_ia](old_weights_gpu_mem, new_weights_gpu_mem, 10, tot_ia, 476, rng_states)
    rng_states = create_xoroshiro128p_states(476*tot_ia, seed=dt.microsecond)
    mutation[tot_ia,476](new_weights_gpu_mem, tot_ia, 476, rng_states,0.1)
        
    new_weights=new_weights_gpu_mem.copy_to_host()
    for i in range(tot_ia):
        ia[i].set_weights(new_weights[i])
    generation+=1
    
    #print(moves_done)

main_2()
















