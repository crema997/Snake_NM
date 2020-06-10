# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 10:14:34 2020

@author: User
"""
import numpy as np
from IA import IA

def main():
    moves_done=[] #0=up, 1=right, 2=down, 3=left
    food_pos=[]
    ia=IA()
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
       
    print(moves_done)
    print(food_pos)
main()   
    
#%%   
import numpy as np  
  
# initilizing list 
lst = [1, 7, 0, 6, 2, 5, 6] 
  
# converting list to array 
arr = np.array(lst) 
  
# displaying list 
print ("List: ", lst) 
  
# displaying array 
print ("Array: ", arr)  
    
    
#%%    
def funza():    
    #while ia.Grid.status:
    a=0
    
