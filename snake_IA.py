# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#griglia 40*40
#lunghezza iniziale serpente 4
#posizione iniziale serpente 20,20

class grid:
    def __init__(self):
        a=0
    
    
    Grid = [[0]*20 for _ in [0]*20]
    
    def Print(self):
       for x in self.Grid:
           for y in x:
               print (y, end=" ")
           print("\n")

    def import_snake(self, Snake):
        
        for i, x in enumerate(self.Grid):
            for j, y in enumerate(x):
                if y==1:
                    self.Grid[i][j]=0
                    
        for x in Snake.position:
            self.Grid[x[0]][x[1]]=1
        
        
        
        
class snake:
    def __init__(self, Lenght=4):    
        self.lenght=Lenght
        self.position=[[10,10]]
        for i in range(0,Lenght-1):
            self.position.append([9-i,10])
   
    def move_down(self):
        
        prev_position=(self.position[0]).copy()
        
        i=0
        for x in self.position:
            if i==0:
                self.position[i][0]+=1
            else:
                buff=self.position[i]
                self.position[i]=prev_position
                prev_position=buff
            i+=1
            
            
    def move_up(self):
        
        prev_position=(self.position[0]).copy()
        
        i=0
        for x in self.position:
            if i==0:
                self.position[i][0]-=1
            else:
                buff=self.position[i]
                self.position[i]=prev_position
                prev_position=buff
            i+=1
   

    def move_right(self):
        
        prev_position=(self.position[0]).copy()
        
        i=0
        for x in self.position:
            if i==0:
                self.position[i][1]+=1
            else:
                buff=self.position[i]
                self.position[i]=prev_position
                prev_position=buff
            i+=1
    
    def move_left(self):
        
        prev_position=(self.position[0]).copy()
        
        i=0
        for x in self.position:
            if i==0:
                self.position[i][1]-=1
            else:
                buff=self.position[i]
                self.position[i]=prev_position
                prev_position=buff
            i+=1
    
    
    
griglia=grid()
snake=snake()

print("senza nulla\n")
griglia.Print()
print("\n\n\n")

griglia.import_snake(Snake=snake)

print("con serpente\n")
griglia.Print()
print("\n\n\n")



snake.move_left()
snake.move_left()
snake.move_left()
snake.move_left()
snake.move_down()
griglia.import_snake(Snake=snake)

print("con serpente mosso\n")
griglia.Print()
print("\n\n\n")

















