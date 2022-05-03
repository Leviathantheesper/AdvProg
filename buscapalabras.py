# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 18:50:54 2022

@author: dcmol
"""
import random
s=""
letras=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
for i in range(100000):
    a=random.choice(letras)
    s=s+a
d=open("espanol.txt")
palabras=[]
for i in range(174846):
    w=d.readline()
    w=w.strip()
    if i%1000==0:
        print(i)
    if w in s:
        palabras.append(w)
print(len(palabras))
print(palabras)