# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 15:01:10 2020

@author: User
"""
from IA_GPU import IA_GPU 
from main import save_best, read_best, save_status, load_status
from datetime import datetime
import sys
import os

#test read/save best    
def test_save_best():
    now = datetime.datetime.now()
    newDirName = now.strftime("%Y_%m_%d_%H_%M")
    os.mkdir(newDirName)
    ia=[IA_GPU()]*10
    for i in range(10):
        ia[i]=IA_GPU()
        ia[i].fill_layers()
    save_best(ia, newDirName)

#test_save_best()

def test_read_best():
    ia_best=read_best('2020_07_08_16_02')   
    print(ia_best[0].get_weights())

#test_read_best()


#test read/save status    
def test_save_status():
    now = datetime.datetime.now()
    newDirName = now.strftime("%Y_%m_%d_%H_%M")
    os.mkdir(newDirName)
    ia=[IA_GPU()]*10
    for i in range(10):
        ia[i]=IA_GPU()
        ia[i].fill_layers()
    save_status(ia, newDirName)

#test_save_status()

def test_load_status():
    ia=load_status('2020_07_08_17_36')   
    print(ia[0].get_weights())

#test_load_status()