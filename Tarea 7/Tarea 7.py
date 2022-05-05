# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 03:06:30 2022

@author: dcmol
"""
import groupclasses
def permutations(list):
    if len(list)<=1:
        return [list]
    if len(list)>1:       
        perm=[]
        for i in list:
            listi=list.copy()
            listi.remove(i)
            permi=permutations(listi)
            for p in permi:
                p.append(i)
                perm.append(p)
        return(perm)
def identitymatrix(n):
    A=[]
    r=[]
    for i in range(n-1):
        r.append(0)
    for i in range(n):
        s=r.copy()
        s.insert(i,1)
        A.append(s)
    return A
def sqmatrixproduct(A,B,n):
    C=identitymatrix(n)
    for i in range(n):
        for j in range(n):
            l=[]
            for k in range(n):
                Cijk=A[i][k]*B[k][j]
                l.append(Cijk)
            C[i][j]=sum(l)            
    return C
def PermutationGroup(n):
    I=identitymatrix(n)
    base1=permutations(I)
    base=range(len(base1))
    table={}
    char=[(a,b) for a in base for b in base]
    for c in char:
        prod=sqmatrixproduct(base1[c[0]],base1[c[1]],n)
        pr=base1.index(prod)
        table[c]=pr
    return(groupclasses.Group(table))
def tablezn(n):
    basetemp=range(n)
    base=[str(a) for a in basetemp]
    cart=[(a,b) for a in base for b in base]
    table={}
    for c in cart:
        d=(int(c[0])+int(c[1]))%n
        table[c]=str(d)
    return table
def tabledn(n):
    Rot=groupclasses.Group(tablezn(n))
    Ref=groupclasses.Group(tablezn(2))
    Rottable=Rot.table
    Reftable=Ref.table
    Dihbase={(a,b) for a in Rot.base for b in Ref.base}
    Dihtable={}
    cart={(a,b) for a in Dihbase for b in Dihbase}
    for c in cart:
        le=c[0]
        ri=c[1]
        if le[1]=='0':
            Dihtable[c]=(Rottable[(le[0],ri[0])],Reftable[(le[1],ri[1])])
        if le[1]=='1':
            Dihtable[c]=(Rottable[(le[0],Rot.inverse(ri[0]))],Reftable[(le[1],ri[1])])
    return Dihtable
#t=tabledn(6)
#G=groupclasses.Group(t)    
#G=Group(t)+Group(tablezn(2))
G=PermutationGroup(4)
print(len(G.subgroups()))
print(len(G.normalsubgroups()))
print(len(G.maximalsubgroups()))
print("Is G Nilpotent? ", G.isitnilpotent())
print("Is G Abelian? ", G.isitabelian())
print(G.base)
print(G.table)
print(G.iden)
print(G.inverses)
Op=[groupclasses.groupelement(G,a) for a in G.base]
for a in Op:
    print(a.order())
