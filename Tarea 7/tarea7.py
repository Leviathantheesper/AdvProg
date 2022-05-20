# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 03:06:30 2022

@author: dcmol
"""
import groupclasses

def tablezn(size):
    """Computes the group of integers modulo size"""
    basetemp=range(size)
    base=[str(a) for a in basetemp]
    cart=[(a,b) for a in base for b in base]
    table={}
    for pair in cart:
        sumamodular=(int(pair[0])+int(pair[1]))%size
        table[pair]=str(sumamodular)
    return table
def tabledn(size):
    """Computes the dihedral group with 2xsize elements as the semidirect
    product f Z_size and Z_2."""
    rot=groupclasses.Group(tablezn(size))
    ref=groupclasses.Group(tablezn(2))
    rottable=rot.table
    reftable=ref.table
    dihbase={(a,b) for a in rot.base for b in ref.base}
    dihtable={}
    cart={(a,b) for a in dihbase for b in dihbase}
    for pair in cart:
        left=pair[0]
        right=pair[1]
        if left[1]=='0':
            dihtable[pair]=(rottable[(left[0],right[0])],reftable[(left[1],right[1])])
        if left[1]=='1':
            dihtable[pair]=(rottable[(left[0],rot.inverse(right[0]))],reftable[(left[1],right[1])])
    return dihtable
#t=tabledn(4)
G=groupclasses.PermutationGroup(5)
for i in G.base:
    print(i,G.twoline[i])
print(G.twoline[2],"o",G.twoline[3],"=",G.twoline[G.table[(2,3)]])
print(G.cycdec[2],"o",G.cycdec[3],"=",G.cycdec[G.table[(2,3)]])
#G=groupclasses.Group(t)
#sets,blacklist=groupclasses.goodsubsets(G, 4)
#print(sets)
#print(len(sets))
#print(len(groupclasses.subsets(G.base, 4)))
#G=Group(t)+Group(tablezn(2))
#G=permutationgroup(3)
print("Number of Subgroups: ",len(G.subgroups()))
print("Number of Normal Subgroups: ",len(G.normalsubgroups()))
print("Number of Sylow Subgroups: ",len(G.sylowsubgroups()))
print("Number of Maximal Subgroups: ",len(G.maximalsubgroups()))
print("Is G Nilpotent? ", G.isitnilpotent())
print("Is G Abelian? ", G.isitabelian())
print("Set of Elements: ", G.base)
print("Table of operations: ",G.table)
print("Identity: ", G.iden)
print("Inverses: ", G.inverses)
Op=[groupclasses.Groupelement(G,a) for a in G.base]
for a in Op:
    print("The order of",a.name," is ", a.order())
