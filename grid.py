# -*- coding: utf-8 -*-
"""
Created on Mon May 25 15:13:57 2020

@author: User
"""

#import tkinter as tk
#0 vuota, 1 serpente, 2 cibo
class grid:
    def __init__(self, _rows=40, _column=40): 
        self.grid = [[0]*_column for _ in [0]*_rows]
        self.rows = _rows
        self.column = _column
        
    def Print(self):
       for x in self.grid:
           for y in x:
               print (y, end=" ")
           print("\n")


    def import_snake(self, Snake):
        
        for i, x in enumerate(self.grid):
            for j, y in enumerate(x):
                if y==1:
                    self.grid[i][j]=0
                    
        for x in Snake.position:
            self.grid[x[0]][x[1]]=1


    def draw (self, canvas, squares):
         for i, x in enumerate(self.grid):
            for j, y in enumerate(x):
                if "white"== canvas.itemcget(squares[j][i], "fill"):
                    canvas.itemconfig(squares[j][i],fill="black")
                if y==1:
                    canvas.itemconfig(squares[j][i],fill="white")