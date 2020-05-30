# -*- coding: utf-8 -*-
"""
Created on Sat May 30 15:46:58 2020

@author: User
"""


from IA import IA

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
 
  



  
test_get_and_set_weights()