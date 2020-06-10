# -*- coding: utf-8 -*-
"""
Created on Mon May 25 15:13:57 2020

@author: User
"""
from numpy.random import randint
from snake import snake
from food import food
#import tkinter as tk
#0 vuota, 1 serpente, 2 cibo

class grid(object):
    def __init__(self, _rows=40, _column=40,snake_len=4): 
        self.grid = [[0]*_column for _ in [0]*_rows]
        self.rows = _rows
        self.column = _column
        self.snake=snake(Lenght=snake_len)
        self.food=food(rows=self.rows, column=self.column)
        self.status=True
        self.points=0
        self.moves_left=200
        
    def Print(self):
       for x in self.grid:
           for y in x:
               print (y, end=" ")
           print("\n")


    def import_snake(self, Snake):
        self.snake=Snake
        for i, x in enumerate(self.grid):
            for j, y in enumerate(x):
                if y==1:
                    self.grid[j][i]=0
                    
        for x in Snake.position:
            self.grid[x[1]][x[0]]=1


    def draw (self, canvas, squares):
         for i, x in enumerate(self.grid):
            for j, y in enumerate(x):
                if "white"== canvas.itemcget(squares[i][j], "fill"):
                    canvas.itemconfig(squares[i][j],fill="black")
                if y==1:
                    canvas.itemconfig(squares[i][j],fill="white") 
                if y==2:
                    canvas.itemconfig(squares[i][j],fill="red")
                    
                    
    def import_food(self, food):
        if self.grid[food.y][food.x]==1:
            food.set_position(randint(0, self.column, 2))
            self.import_food(food)
        else:
            self.food=food
            self.grid[food.y][food.x]=2
    
    def update_grid (self):        
        for i, x in enumerate(self.grid):
            for j, y in enumerate(x):
                if y==1:
                    self.grid[i][j]=0
                    
        for x in self.snake.position:
            self.grid[x[1]][x[0]]=1            
            
        while self.grid[self.food.y][self.food.x]==1:
            self.food.set_position(randint(0, self.column, 2))
        
        self.grid[self.food.y][self.food.x]=2    
        
    def collision(self):
        if self.snake.position[0][0]<0 or self.snake.position[0][0]>=self.column-1 or self.snake.position[0][1]<0 or self.snake.position[0][1]>=self.rows-1:
            self.status=False
     
        for a in self.snake.position[1:]:
            if a==self.snake.position[0]:
                self.status=False    
            
    def eat(self):
        if self.food.x == self.snake.position[0][0] and self.food.y == self.snake.position[0][1]:
            self.snake.lenght+=1
            self.points+=1
            self.moves_left+=100
            self.snake.position.append(self.snake.last_pos)
            self.food.set_position(randint(0, self.column, 2))
            
    def move_up(self):#ok
        if self.moves_left<=0:
            self.status=False
        else:
            self.snake.move_up()
            self.moves_left-=1
            print(self.moves_left)
            self.collision()
            self.eat()
            self.update_grid()
                
    def move_down(self):#ok
        if self.moves_left<=0:
            self.status=False
        else:
            self.snake.move_down()
            self.moves_left-=1
            print(self.moves_left)
            self.collision()
            self.eat()
            self.update_grid()
                
    def move_left(self):
        if self.moves_left<=0:
            self.status=False
        else:
            self.snake.move_left()
            self.moves_left-=1
            print(self.moves_left)
            self.collision()
            self.eat()
            self.update_grid()
        
    def move_right(self):
        if self.moves_left<=0:
            self.status=False
        else:
            self.snake.move_right()
            self.moves_left-=1
            print(self.moves_left)
            self.collision()
            self.eat()
            self.update_grid()
              
    def get_points(self):
        return self.points            
            
    def set_points(self, points):
        self.points = points
            
    def get_food_pos(self):     
        return self.food.get_position()
            
            
            
            