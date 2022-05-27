# -*- coding: utf-8 -*-
"""
Created on Thu May 26 20:53:36 2022

@author: dcmol
"""
import pickle
f=open('texto.txt','r')
g=open('result.txt','wb')
content = f.read()
dumping=pickle.dumps(content)
print('Pickled: ', dumping)
print("Unpickled: ",pickle.loads(dumping))
pickle.dump(content,g)
f.close()
g.close()
h=open('result.txt','r')
gibberish=h.read()
print("If you don't open as binary you get: ",gibberish)
h.close()
i=open("result.txt","rb")
d=pickle.load(i)
print ("Unpickled file: ",d)
i.close()