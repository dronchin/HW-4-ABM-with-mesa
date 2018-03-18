#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 21:18:36 2018

@author: fyt
"""

import random as r
legal_x=[0,10]
legal_y=[0,10]

class MSU:
    def __init__(self):
        #initial power
        self.power=100
        #initial random position
        self.x=r.randint(legal_x[0],legal_x[1])
        self.y=r.randint(legal_y[0],legal_y[1])

    def move(self):
        #move to new position (x, y)
        new_x=self.x+r.choice([-1,1,-1,1])
        new_y=self.y+r.choice([-1,1,-2,-2])
        #check whether the new position over x-axis
        if new_x<legal_x[0]:
            self.x=legal_x[0]-(new_x-legal_x[0])
        elif new_x>legal_x[1]:
            self.x=legal_x[1]-(new_x-legal_x[1])
        else:
            self.x=new_x
        #check whether the new position over y-axis
        if new_y<legal_y[0]:
            self.y=legal_y[0]-(new_y-legal_y[0])
        elif new_y>legal_y[1]:
            self.y=legal_y[1]-(new_y-legal_y[1])
        else:
            self.y=new_y
        #power used
        self.power-=1
        #return position
        return (self.x,self.y)
    def eat(self):
        self.power+=20
        if self.power>100:
            self.power=100
class UoM:
    def __init__(self):
        self.x=r.randint(legal_x[0],legal_x[1])
        self.y=r.randint(legal_y[0],legal_y[1])
    def move(self):
         #move to new position (x, y)
        new_x=self.x+r.choice([-1,1,-2,2])
        new_y=self.y+r.choice([-1,1,-2,2])
        #check whether the new position over x-axis
        if new_x<legal_x[0]:
            self.x=legal_x[0]-(new_x-legal_x[0])
        elif new_x>legal_x[1]:
            self.x=legal_x[1]-(new_x-legal_x[1])
        else:
            self.x=new_x
        #check whether the new position over y-axis
        if new_y<legal_y[0]:
            self.y=legal_y[0]-(new_y-legal_y[0])
        elif new_y>legal_y[1]:
            self.y=legal_y[1]-(new_y-legal_y[1])
        else:
            self.y=new_y
        #return position
        return (self.x,self.y)
msu=MSU()
uom=[]
for i in range(10):
    new_uom=UoM()
    uom.append(new_uom)
while True:
    if not len(uom):
        print('All UoM were eated by MSU!')
        break
    if not msu.power:
        print('MSU has no power, died!')
        break
    pos=msu.move()
    for each_uom in uom[:]:
        if each_uom.move()==pos:
            #Uom was eated
            msu.eat()
            uom.remove(each_uom)
            print('A UoM was eated by MSU!')