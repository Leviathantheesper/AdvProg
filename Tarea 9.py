# -*- coding: utf-8 -*-
"""
Created on Sun May 22 05:55:52 2022

@author: dcmol
"""

import re
import os

def filenames():
    names=[]
    files=[file for file in os.listdir() if os.path.isfile(file)]
    #print(files)
    for file in files:
        namematch=re.search("^.*\.", file)
        print(type(namematch))
        if type(namematch)==type(None):
            names.append(file)
        else:
            name=namematch.group(0)[:-1]
            names.append(name)
    print(names)
    return names


filenames()
