# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 15:01:10 2020

@author: User
"""
from IA_GPU import IA_GPU, mutation, recombination, recombination_2
from datetime import datetime
import sys
import os
import numpy as np
from numba import cuda
from numba.cuda.random import create_xoroshiro128p_states

def test_predict():
    ia=IA_GPU()
    ia.fill_layers()
    arr=ia.weights_layer_2
    inp_arr=np.array([[1.]]*18)
    inp_arr2=np.array([[1.]]*19)
    out_arr=np.array([[0.]*19])
    move=ia.predict(inp_arr)
    print(move[0])

def test_mutation():
    a=np.array([[0.,0.,0.,0.,0.],[0.,0.,0.,0.,0.]])
    A_global_mem = cuda.to_device(a)
    dt = datetime.now()
    rng_states = create_xoroshiro128p_states(10, seed=dt.microsecond)
    mutation[2,5](A_global_mem,2,3,rng_states,0.3)
    A=A_global_mem.copy_to_host()
    print(A)
    
def test_recombination():
    dt = datetime.now()
    tot_ia=5
    rng_states = create_xoroshiro128p_states(1*tot_ia, seed=dt.microsecond)
    inp_weights_local=np.array([[1.,2.,3.,4.,5.,6.,7.,8.,9.],[9.,8.,7.,6.,5.,4.,3.,2.,1.]])
    inp_weights= cuda.to_device(inp_weights_local)
    out_weights = cuda.device_array((tot_ia, 9))
    recombination[1,tot_ia](inp_weights, out_weights, 2, tot_ia, 9, rng_states)
    C = out_weights.copy_to_host()
    print(C)

def test_recombination_2():
    dt = datetime.now()
    tot_ia=5
    rng_states = create_xoroshiro128p_states(644*tot_ia, seed=dt.microsecond)
    inp_weights_local=np.array([[1.,2.,3.,4.,5.,6.,7.,8.,9.],[9.,8.,7.,6.,5.,4.,3.,2.,1.]])
    inp_weights= cuda.to_device(inp_weights_local)
    out_weights = cuda.device_array((tot_ia, 9))
    recombination_2[tot_ia,9](inp_weights, out_weights, 2, tot_ia, 9, rng_states)
    C = out_weights.copy_to_host()
    print(C)
  
#test_predict()
#test_mutation()
#test_recombination()
#test_recombination_2()