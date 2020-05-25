# -*- coding: utf-8 -*-
"""
Created on Sat May 23 11:16:50 2020

@author: User
"""


import tkinter as tk
from tkinter import Canvas

window=tk.Tk()
window.geometry("839x839")
window.title("prova")
window.resizable(False,False)
window.configure(background="black")

c=Canvas(window,height=839,width=839,bg="black")
c.pack()

#canvas.create_rectangle(x1, y1, x2, y2, **kwargs), 
#with (x1,y1) the coordinates of the top left corner and (x2, y2) those of the bottom right corner


#r1=c.create_rectangle(0,0,20,20,fill="red")
#r2=c.create_rectangle(0,0,40,20,fill="blue")
#r3=c.create_rectangle(0,0,20,40,fill="yellow")
#r4=c.create_rectangle(0,60,20,20,fill="green")
#r5=c.create_rectangle(60,0,20,20,fill="white")

squares =[[c.create_rectangle(0,0,20,20,fill="white")]*40 for _ in [c.create_rectangle(0,0,20,20,fill="white")]*40]

for i, x in enumerate(squares):
    for j, y in enumerate(x):
        squares[i][j]=c.create_rectangle(0+21*i,0+21*j,20+21*i,20+21*j,fill="black")



c.itemconfig(squares[0][20],fill="white")










def keypress(event):
	x, y = 0, 0
	if event.char == "a": x = -10 
	elif event.char == "d": x = 10
	elif event.char == "w": y = -10
	elif event.char == "s": y = 10
	#c.move(squares[0][0], x, y)

window.bind("<Key>", keypress)

#first_button=tk.Button(text="Saluta!")
#first_button.grid(row=0,column=0)

if __name__=="__main__":
    window.mainloop()