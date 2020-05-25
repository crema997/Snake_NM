# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#import tkinter as tk
from grid import grid
from snake import snake
import tkinter as tk
from tkinter import Canvas

#griglia 40*40
#lunghezza iniziale serpente 4
#posizione iniziale serpente 20,20

griglia=grid(_rows=40, _column=40)
snake=snake()
        
window=tk.Tk()
window.geometry("839x839")
window.title("prova")
window.resizable(False,False)
window.configure(background="black")

c=Canvas(window,height=839,width=839,bg="black")
c.pack()      
        
squares =[[c.create_rectangle(0,0,20,20,fill="white")]*griglia.column for _ in [c.create_rectangle(0,0,20,20,fill="white")]*griglia.rows]

for i, x in enumerate(squares):
    for j, y in enumerate(x):
        squares[i][j]=c.create_rectangle(0+21*i,0+21*j,20+21*i,20+21*j,fill="black")
        
    
 


griglia.import_snake(Snake=snake)
griglia.draw(c, squares)

def keypress(event,snake, griglia, c ,squares):
    
    if event.char == "a": snake.move_left()
    elif event.char == "d": snake.move_right()
    elif event.char == "w": snake.move_up()
    elif event.char == "s": snake.move_down()
    
    griglia.import_snake(Snake=snake)   
    griglia.draw(c, squares)

window.bind("<Key>", lambda event: keypress(event, snake, griglia, c, squares))
           
if __name__=="__main__":
    window.mainloop()

#print("senza nulla\n")
#griglia.Print()
#print("\n\n\n")

#griglia.import_snake(Snake=snake)

#print("con serpente\n")
#griglia.Print()
#print("\n\n\n")



#snake.move_left()
#snake.move_left()
#snake.move_left()
#snake.move_left()
#snake.move_down()
#griglia.import_snake(Snake=snake)

#print("con serpente mosso\n")
#griglia.Print()
#print("\n\n\n")

















