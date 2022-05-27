# -*- coding: utf-8 -*-
"""
Created on Thu May 26 21:09:53 2022

@author: dcmol
"""

import pickle
f=open("result.txt","wb")
dct={"name":"Ravi", "age":23, "Gender":"M","marks":75}
pickle.dump(dct,f)
f.close()

#to read
import pickle
f=open("result.txt","rb")
d=pickle.load(f)
print (d)
f.close()