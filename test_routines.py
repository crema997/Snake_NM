# -*- coding: utf-8 -*-
"""
Created on Sat May 30 15:46:58 2020

@author: User
"""
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten
from random import seed
from IA import IA
from IA import order_IA
from IA import recombination_1
from IA import recombination_2
from IA import mutation

def test_get_and_set_weights():
    Ia=IA()
    Ia2=IA()
    a=Ia.get_weights_as_nparray()
    c=Ia2.get_weights_as_nparray()
    
    a_equals_c=((a==c).all())
    print ("a equals c? Expected: False Obtained:", end=" ")
    print (a_equals_c)
    #print (c)
    #print ("\n\n\n\n\n")
    Ia2.set_weights_as_nparray(a)
    b=Ia2.get_weights_as_nparray()
    
    a_equals_b=((b==a).all())
    print ("a equals b? Expected: True Obtained:", end=" ")
    print (a_equals_b)
    #print (a)
    #print ("\n\n\n\n\n")
    #print (b)

#test_get_and_set_weights()
    
def get_points(Ia):
    return Ia.get_points()

def test_ordering():
    ia=[IA()]*3
    
    for i, x in enumerate(ia):
        ia[i]=IA()
    
    
    ia[0].set_points(5)
    ia[1].set_points(3)
    ia[2].set_points(7)
    
    print("prima di riordinare, ordine aspettato: 5 3 7")
    for x in ia:
        print(x.get_points())
    
    order_IA(ia)
    
    print("dopo aver ordinato,  ordine aspettato: 7 5 3 ")
    for x in ia:
        print(x.get_points())
        
#test_ordering()
#test recombination_1
def test_reco_1():
    a=[0,1,2,3,4,5,6,7,8,9]
    b=[9,8,7,6,5,4,3,2,1,0]
    cut=3
    c=recombination_1(a,b,cut)
    result_1=[9,8,7,3,4,5,6,7,8,9]
    result_2=[0,1,2,6,5,4,3,2,1,0]
    for x in c:
        for y in x:
            print(y, end=" ")
        print("\n")
        
        
    c0_1=(c[0]==result_1)
    c1_2=(c[1]==result_2)
    print ("c[0] equals result 1? expected: True obtained",end=" ")
    print(c0_1)
    print ("c[1] equals result 2? expected: True obtained",end=" ")
    print(c1_2)    

test_reco_1()

#test recombination_2
def test_reco_2():
    a=[0,1,2,3,4,5,6,7,8,9]
    b=[9,8,7,6,5,4,3,2,1,0]
    arr=[a,b]    
    c=recombination_2(arr)
    for i in c:
        print(i)
  
def test_mutation():
    a=[0.,1.,2.,3.,4.,5.,6.,7.,8.,9.]
    b=mutation(a, mutation_prob=0.1)
    print(a)
    print(b)

def test_distances():
    seed()
    ia=IA()
    print(ia.calculate_distances())
    ia.draw()
#%%
#spazio di prova per test routine

from numpy.random import randint

def test_genetic_algo():
    ia1=IA()
    ia2=IA()
    
    w1=ia1.get_weights_as_nparray()
    w2=ia2.get_weights_as_nparray()
    
    cut =randint(0, w1.size, 1)
    print(w1.size)
    print(w2.size)
    
    buff=recombination_1(w1, w2, cut[0])
    print(len(buff[0]))
    
    buff=mutation(buff[0])

    print(len(buff))
    
    ia3=IA()
    ia3.set_weights_as_nparray(buff)
    
test_genetic_algo()
#%%
#test non importanti

def test ():
    Ia=IA()
    
    a=Ia.get_weights_as_nparray()
    print (a.size)

    #print(Ia.model.get_weights())
  
    for i,  layer in enumerate(Ia.model.layers):
        weights = layer.get_weights()
        print("layer", end=" ")
        print(i)
        print (weights)
        
    tf.keras.utils.plot_model(Ia.model, to_file="modello.png")

























