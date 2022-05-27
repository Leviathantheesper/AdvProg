# -*- coding: utf-8 -*-
"""
Created on Thu May 26 21:09:53 2022

@author: dcmol
"""

#to read
import pickle
f=open("result.txt","rb")
d=pickle.load(f)
print (d)
f.close()