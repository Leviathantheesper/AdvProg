# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 03:06:30 2022

@author: dcmol
"""
import groupclasses
def permutations(mylist):
    """Computes all the permutation of an ordered set mylist."""
    if len(mylist)<=1:
        return [mylist]
    if len(mylist)>1:
        perm=[]
        for i in mylist:
            listi=mylist.copy()
            listi.remove(i)
            permlist=permutations(listi)
            for permutation in permlist:
                permutation.append(i)
                perm.append(permutation)
        return perm
    return "Wrong type"
def identitymatrix(size):
    """Computes the sizexsize identity matrix."""
    idmatrix=[]
    zerovector=[]
    for i in range(size-1):
        zerovector.append(0)
    for i in range(size):
        row=zerovector.copy()
        row.insert(i,1)
        idmatrix.append(row)
    return idmatrix
def sqmatrixproduct(leftmatrix,rightmatrix,size):
    """Computes the matrix product of the square matrices leftmatrix and
    rightmatrix of the same size."""
    matprod=identitymatrix(size)
    for i in range(size):
        for j in range(size):
            localproducts=[]
            for k in range(size):
                productijk=leftmatrix[i][k]*rightmatrix[k][j]
                localproducts.append(productijk)
            matprod[i][j]=sum(localproducts)
    return matprod
def permutationgroup(size):
    """Computes the permutation group S_size, as the group of all the permutation
    matrices, i.e. the result of permutating the rows of the identity matrix.
    Then it removes the identity as matrices and leaves it just with the
    table."""
    iden=identitymatrix(size)
    base1=permutations(iden)
    base=range(len(base1))
    table={}
    cart=[(a,b) for a in base for b in base]
    for pair in cart:
        prod=sqmatrixproduct(base1[pair[0]],base1[pair[1]],size)
        prod_index=base1.index(prod)
        table[pair]=prod_index
    return groupclasses.Group(table)
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
G=permutationgroup(5)
#G=groupclasses.Group(t)
#sets,blacklist=groupclasses.goodsubsets(G, 4)
#print(sets)
#print(len(sets))
#print(len(groupclasses.subsets(G.base, 4)))
#G=Group(t)+Group(tablezn(2))
#G=permutationgroup(3)
print("Number of Subgroups: ",len(G.subgroups()))
print("Number of Normal Subgroups: ",len(G.normalsubgroups()))
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
