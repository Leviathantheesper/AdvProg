# -*- coding: utf-8 -*-
"""
Created on Thu May  5 13:36:02 2022

@author: dcmol
"""
from math import ceil
def subsets(A,n):
    sub=[set()]
    if n==0:
        return sub
    elif n>0:
        sub2=subsets(A,n-1)
        for S in sub2:
            for a in A:
                Q=S.copy()
                Q.add(a)
                sub.append(Q)
        sub3={frozenset(a) for a in sub}
        sub4=[set(a) for a in sub3]
        return sub4
def listofprimes(n):
    l=[2]
    if n==1:
        return [2]
    elif n==2:
        return [2,3]
    elif n==3:
        return [2,3,5]
    else:
        l=listofprimes(n-1)
        k=l[len(l)-1]
        for i in range(k+1,2*k-2):
            isp=True
            for a in l:
                if i%a==0:
                    isp=False
                    break
            if isp:
                l.append(i)
                break
        return l
def lpleqthan(n):
    l=listofprimes(ceil(1.4*n))
    s=l.copy()
    for i in l:
        if i>n:
            s.remove(i)
    return s
def primedecomposition(n):
    l=lpleqthan(n)
    d=[]
    for p in l:
        e=0
        k=n
        while k%p==0:
            e+=1
            k=k//p
        if e!=0:
            d.append((p,e))
    return(d)
def Newmanbound(n):
    l=[a[1]+1 for a in primedecomposition(n)]
    s=sum(l)
    return s
class Group:
    def __init__(self,table,s=0):
        #s!=0 to skip checks. Use if you already know the table defines a group.
        base=set(table.values())
        I=''    
        Inversos=[]
        if s==0:            
            Clo=True
            cart=[(a,b) for a in base for b in base]
            for c in cart:
                if table[c] not in base:
                    Clo=False
                    print("Warning, not closed.")
                    break
            Ass=True
            for i in base:
                for j in base:
                    for k in base:
                        a=table[(table[(i,j)],k)]                   
                        b=table[(i,table[(j,k)])]
                        if a!=b:
                            Ass=False
                            break
                    if not Ass:
                        break
                if not Ass:
                    print("Warning, not associative")
                    break     
            Id=True
            Ids=[]
            for i in base:
                Isid=True
                for j in base:
                    if table[(j,i)]!=j:
                        Isid=False
                        break
                if Isid:
                    Ids.append(i)            
            if len(Ids)==1:
                Id=True
                I=Ids[0]
            else:
                Id=False
                print("Warning, not identity")
            Inv=True
            for i in base:
                Hasinverse=False
                for j in base:
                    if table[(i,j)]==I:
                        Hasinverse=True
                        Inversos.append((i,j))
                        break
                if not Hasinverse:
                    Inv=False
                    print("Warning, not inverses")
                    break
        if s!=0:
            Clo=True
            Ass=True
            Id=True
            Inv=True
            cart={(a,b) for a in base for b in base}
            for c in cart:
                if table[c]==c[1]:
                    I=c[0]
            for c in cart:
                if table[c]==I:
                    Inversos.append(c)                    
        self.inverses=set(Inversos)
        self.base=base
        self.table=table
        self.iden=I
        if Clo and Ass and Id and Inv:
            self.isgroup=True
        else:
            print("Warning: Not a group")
            self.isgroup=False
    def subgroup(self,A):
        if A.issubset(self.base):
            subtable={}
            cart=[(a,b) for a in A for b in A]
            IsS=True
            for c in cart:
                if self.table[c] not in A:
                    IsS=False
                    return IsS
                else:
                    subtable[c]=self.table[c]
            return Group(subtable,1)
        else:
          return False
    def __str__(self):
        return str(self.table)
    def __eq__(self,other):
        if self.base==other.base and self.table==other.table:
            return True
        else:
            return False
    def __add__(self,other):
        T1=self.table
        T2=other.table
        S1=self.base
        S2=other.base
        S3={(a,b) for a in S1 for b in S2}
        char={(a,b) for a in S3 for b in S3}
        sumtable={}
        for c in char:
            q=c[0]
            r=c[1]
            sumtable[c]=(T1[(q[0],r[0])],T2[(q[1],r[1])])
        return Group(sumtable)
    def inverse(self,a):
        if a not in self.base:
            return "No"
        else:
            for c in self.inverses:
                if a in c:
                    if a==c[0]:
                        return c[1]
                    else:
                        return c[0]
    def subgroups(self):
        b=Newmanbound(len(self.base))
        subbase=set()
        P=subsets(self.base,b)
        for S in P:
            H=self.gen(S)
            subbase.add(frozenset(H))
        subgrouplist=[self.subgroup(H) for H in subbase]            
        return subgrouplist
    def gen(self,S):
        if S==set():
            return {self.iden}
        A={groupelement(self,a) for a in S}
        H=set()
        queue=[groupelement(self,self.iden)]
        while queue!=[]:
            for x in queue:
                queue.remove(x)
                if x.name in H:
                    continue
                else:
                    H.add(x.name)
                for a in A:
                    t=x+a
                    queue.append(t)
        return H
    def normalsubgroups(self):
        subgrouplist=self.subgroups()
        Gable=self.table
        Norm=[]
        for H in subgrouplist:
            Isnormal=True
            for i in self.base:
                for j in H.base:
                    conj=Gable[(Gable[(i,j)],self.inverse(i))]
                    if conj not in H.base:
                        Isnormal=False
                        break
                if not Isnormal:
                    break
            if Isnormal:
                Norm.append(H)    
        return Norm
    def isitabelian(self):
        Ab=True
        char=[(a,b) for a in self.base for b in self.base]
        for c in char:
            if self.table[c] != self.table[(c[1],c[0])]:
                Ab=False
                break
        return Ab
    def maximalsubgroups(self):
        subgrouplist=self.subgroups()
        Max=[]
        for H in subgrouplist:
            ismaximal=True
            if len(H.base)==len(self.base):
                ismaximal=False
            for K in subgrouplist:
                if len(K.base)!= len(self.base) and (H.base).issubset(K.base) and not H==K:
                    ismaximal=False
                    break
            if ismaximal:
                Max.append(H)
        return Max
    def isitnilpotent(self):
        Max=self.maximalsubgroups()
        Norm=self.normalsubgroups()
        Int=[]
        for H in Max:
            for K in Norm:
                if H==K and H not in Int:
                    Int.append(H)                    
        return len(Max)==len(Int)                                       
class groupelement:
    def __init__(self,group,tag):
        self.name=tag
        self.G=group
    def __add__(self,other):
        return groupelement(self.G,self.G.table[(self.name,other.name)])
    def __str__(self):
        return str(self.name)
    def __sub__(self,other):
        return groupelement(self.G,self.G.table[(self.name,self.G.inverse(other.name))])
    def order(self):
        counter=1
        a=self
        while a.name != self.G.iden:
            a+=self
            counter+=1
        return counter
        