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

from IA import IA
from IA import order_IA

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

    
def get_point(Ia):
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
  

  

#%%
def get_point(Ia):
    return Ia.get_points()

ia=[IA()]*3

Ia1=IA()
Ia2=IA()
Ia3=IA()

Ia1.set_points(5)
Ia2.set_points(3)
Ia3.set_points(7)

ia[0]=Ia1
ia[1]=Ia2
ia[2]=Ia3

for x in ia:
    print(x.get_points())

ia.sort(key=get_point)

for x in ia:
    print(x.get_points())
#%%


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

























