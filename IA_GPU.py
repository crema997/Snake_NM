# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 10:36:19 2020

@author: User
"""

from __future__ import print_function, absolute_import
from grid import grid
from numba import cuda
from numba.cuda.random import create_xoroshiro128p_states, xoroshiro128p_uniform_float32, xoroshiro128p_normal_float32
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
def recombination(inp_weights, out_weights, n_inp_ia, tot_ia, n_weights, rng_states):#n_inp_ia: number of ia in input, tot_ia: total number of ia to be generated, n_weights: total number of weighta for ia
    
    pos = cuda.grid(1)
    if pos < tot_ia:
        ia_1 = int(xoroshiro128p_uniform_float32(rng_states, cuda.grid(1)) * n_inp_ia)
        ia_2 = int(xoroshiro128p_uniform_float32(rng_states, cuda.grid(1)) * n_inp_ia)
        cut = int(xoroshiro128p_uniform_float32(rng_states, cuda.grid(1)) * n_weights)
        for i in range(n_weights):
            if i < cut:
                out_weights[pos][i]=inp_weights[ia_1][i]
            else:
                out_weights[pos][i]=inp_weights[ia_2][i]

@cuda.jit #n block = tot_ia, threads per block = n_weights
def recombination_2(inp_weights, out_weights, n_inp_ia, tot_ia, n_weights, rng_states):
    # Thread id in a 1D block
    tx = cuda.threadIdx.x
    # Block id in a 1D grid
    ty = cuda.blockIdx.x
    if ty<tot_ia and tx<n_weights:
        ia_rng = int(xoroshiro128p_uniform_float32(rng_states, cuda.grid(1)) * n_inp_ia)
        out_weights[ty][tx] = inp_weights[ia_rng][tx]


@cuda.jit
def mutation(inp_weights, n_ia, n_weights, rng_states, prob=0.1):
    # Thread id in a 1D block
    tx = cuda.threadIdx.x
    # Block id in a 1D grid
    ty = cuda.blockIdx.x
    if ty<n_ia and tx<n_weights:
        a=xoroshiro128p_uniform_float32(rng_states, cuda.grid(1))
        if a<prob:
            inp_weights[ty][tx]+=(xoroshiro128p_normal_float32(rng_states, cuda.grid(1)))/5.



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
            ]*16)
        self.weights_layer_4=np.array([
                [0.]*(16+1)
            ]*4)
        self.moves_done=[]
        self.food_pos=[]
        
    def fill_layers(self):
        blocks=1
        
        threads_per_block=19
        dt = datetime.now()
        rng_states = create_xoroshiro128p_states(threads_per_block * blocks, seed=dt.microsecond)
        for i, x in enumerate(self.weights_layer_2):
            fill_random[1,threads_per_block](self.weights_layer_2[i], 19, rng_states)
            
        threads_per_block=17
        dt = datetime.now()
        rng_states = create_xoroshiro128p_states(threads_per_block * blocks, seed=dt.microsecond)
        for i, x in enumerate(self.weights_layer_3):
            fill_random[1,threads_per_block](self.weights_layer_3[i], 17, rng_states)
           
        threads_per_block=17
        dt = datetime.now()
        rng_states = create_xoroshiro128p_states(threads_per_block * blocks, seed=dt.microsecond)
        for i, x in enumerate(self.weights_layer_4):
            fill_random[1,threads_per_block](self.weights_layer_4[i], 17, rng_states)


    def get_weights(self):
        w_layer2=np.reshape(self.weights_layer_2,(304))
        w_layer3=np.reshape(self.weights_layer_3,(272))
        w_layer4=np.reshape(self.weights_layer_4,(68))
        return np.concatenate((w_layer2,w_layer3,w_layer4),axis=None)
    
    def set_weights(self, weights):
        w_layer2=np.array(weights[:304])
        self.weights_layer_2=np.reshape(w_layer2,(16,19))
        
        w_layer3=np.array(weights[304:304+272])
        self.weights_layer_3=np.reshape(w_layer3,(16,17))
        
        w_layer4=np.array(weights[304+272:])
        self.weights_layer_4=np.reshape(w_layer4,(4,17))
      

    def predict(self, input_arr):  
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
        for i in range(16):
            C[i][0]=expit(C[i][0])
        
        arr=np.append(C,[[1.]],0)
        A_global_mem = cuda.to_device(self.weights_layer_3)
        B_global_mem = cuda.to_device(arr)    
        C_global_mem = cuda.device_array((16, 1))
        blockspergrid_x = int(math.ceil(self.weights_layer_3.shape[0] / threadsperblock[0]))
        blockspergrid_y = int(math.ceil(arr.shape[1] / threadsperblock[1]))
        blockspergrid = (blockspergrid_x, blockspergrid_y)
        matmul[blockspergrid, threadsperblock](A_global_mem, B_global_mem, C_global_mem) #calculated values of third layer
   
        C = C_global_mem.copy_to_host()
        for i in range(8):
            C[i][0]=expit(C[i][0])
        
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
        C=np.reshape(C,(4))
        
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
                distance_wall = i
                boolean=False
            else:
                if self.grid.grid [pos[0]] [pos[1]] == 1:
                    if (not body_found):
                        distance_body = i 
                        body_found=True
            i+=1
        return [1/distance_body, 1/distance_wall]

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

    def restart(self):
        self.grid.restart()
        self.moves_done=[]
        self.food_pos=[]
     
    #set of functions used only for replay (no random generationf of food)
    def Move_up(self):
        self.grid.Move_up()
      
    def Move_down(self):
        self.grid.Move_down()
        
    def Move_left(self):
        self.grid.Move_left()

    def Move_right(self):
        self.grid.Move_right()    
    

def get_points(Ia):
    return Ia.get_points()    
    
def get_score_2(ia):
    points=ia.grid.points
    moves_done=200+points*100-ia.grid.moves_left
    return (2**points)*moves_done*moves_done

def get_score_3(ia):
    points=ia.grid.points
    moves_done=200+points*100-ia.grid.moves_left
    return points+0.001*moves_done

def get_score(ia):
    points=ia.grid.points
    moves_done=200+points*100-ia.grid.moves_left

    if (points < 10):
      fitness = moves_done * moves_done * pow(2, points)
    else:
      fitness =  moves_done * moves_done
      fitness *= pow(2, 10)
      fitness *= points
    
    return fitness

def order_IA(ia):
    ia.sort(key=get_score, reverse=True)
    return ia

def play(ia):
    #0=up, 1=right, 2=down, 3=left

    while ia.grid.status:
        ia.food_pos.append(ia.get_food_pos())
        distances = ia.calculate_distances()
        distances = np.reshape(distances, (18,1))
        result = ia.predict(distances)
        
        if result[0][0]==0:
            ia.move_up()
            ia.moves_done.append(0)
        elif result[0][0]==1:
            ia.move_right()
            ia.moves_done.append(1)
        elif result[0][0]==2:
            ia.move_down()
            ia.moves_done.append(2)
        elif result[0][0]==3:
            ia.move_left()
            ia.moves_done.append(3)