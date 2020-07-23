# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 16:03:13 2020

@author: User
"""
from main import save_best, read_best, save_status, load_status
import os
import datetime
from IA_GPU import IA_GPU


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

def test_read_best():
    ia_best=read_best('2020_07_23_16_08')   
    print(ia_best[0].get_weights())

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


def test_load_status():
    ia=load_status('2020_07_23_16_10')   
    print(ia[0].get_weights())

#test_save_best()
#test_read_best()
#test_save_status()
#test_load_status()