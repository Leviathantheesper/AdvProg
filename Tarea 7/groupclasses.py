# -*- coding: utf-8 -*-
"""
Created on Thu May  5 13:36:02 2022

@author: dcmol
"""
from math import ceil
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
    return Group(table)
def two_line(permutationmatrix):
    "Transforms a permutation matrix into the two line form of the permutation."
    size=len(permutationmatrix)
    iden=identitymatrix(size)
    twoline={}
    for i in range(size):
        result=permutationmatrix.index(iden[i])
        twoline[i+1]=result+1
    return twoline
def cycle_decomposition(twoline):
    "Returns the cycle decomposition of a permutation"
    base=list(twoline.keys())
    cycles=[]
    while base!=[]:
        key=base[0]
        base.remove(key)
        cycle=[key]
        temp=key
        while True:
            temp=twoline[temp]
            if temp in cycle:
                cycles.append(tuple(cycle))
                break
            cycle.append(temp)
            base.remove(temp)
        removetrivial=cycles.copy()
        for i in cycles:
            if len(i)==1:
                removetrivial.remove(i)
    return removetrivial
def transposition_decomposition(cycles):
    "Returns a transposition decomposition of a permutation"
    trans=[]
    for cycle in cycles:
        for i in range(len(cycle)-1):
            trans.append((cycle[0],cycle[len(cycle)-1-i]))
    return trans

def goodsubsets(basegroup,number):
    """Computes all the subsets with at most number elements of a given
    basegroup such that no element is in the generated subgroup of the other
    ones. It's essentially computing all the subgroups."""
    groupset=basegroup.base
    sub=[]
    blacklist=[]
    if number==1:
        for element in groupset:
            repeated=False
            for other in sub:
                if basegroup.gen({element})==basegroup.gen(other):
                    repeated=True
            if not repeated:
                sub.append({element})
                blacklist.append(basegroup.gen({element}))
        return sub,blacklist
    sub,blacklist=goodsubsets(basegroup,number-1)
    sub2=sub.copy()
    for smallsubset in sub2:
        subgroup=basegroup.gen(smallsubset)
        blacklist.append(subgroup)
        for element in groupset:
            if element not in subgroup:
                #print(element," no est?? en ",subgroup," que es generado por ",smallsubset)
                copy=smallsubset.copy()
                copy.add(element)
                gene=basegroup.gen(copy)
                if gene not in blacklist:
                    sub.append(copy)
                    blacklist.append(gene)
    return sub,blacklist
def subsets(baseset,number):
    """Computes all the subsets with at most number elements of a given baseset."""
    sub=[set()]
    sub4=[]
    if number==0:
        sub4=sub
    else:
        sub2=subsets(baseset,number-1)
        for smallsubset in sub2:
            for element in baseset:
                copy=smallsubset.copy()
                copy.add(element)
                sub.append(copy)
        sub3={frozenset(element) for element in sub}
        sub4=[set(element) for element in sub3]
    return sub4
def listofprimes(number):
    """Computes the first numberth primes."""
    listota=[]
    if number==1:
        listota=[2]
    elif number==2:
        listota=[2,3]
    elif number==3:
        listota=[2,3,5]
    else:
        listota=listofprimes(number-1)
        k=listota[len(listota)-1]
        for i in range(k+1,2*k-2):
            isp=True
            for prn in listota:
                if i%prn==0:
                    isp=False
                    break
            if isp:
                listota.append(i)
                break
    return listota
def lpleqthan(number):
    """Computes all the primes less or equal than number. The value 1.4*number
    is a bound for such a number.
    Source: math.stackexchange: Question ID 54312.
    """
    listota=listofprimes(ceil(1.4*number))
    primosmenores=listota.copy()
    for i in listota:
        if i>number:
            primosmenores.remove(i)
    return primosmenores
def primedecomposition(number):
    "Basic algorithm for prime decomposition of number."
    listota=lpleqthan(number)
    primedec=[]
    for prime in listota:
        expo=0
        k=number
        while k%prime==0:
            expo+=1
            k=k//prime
        if expo!=0:
            primedec.append((prime,expo))
    return primedec
def newmanbound(number):
    """This is a weak version of the Newman bound for the quantity of generators
    of a group of size number.
    Source: Bounds for the Number of Generators of a Finite Group
    Author: Morris Newman
    Published on 1967
    In the bound that article there is a series of numbers denoted by f_i
    which correspond to the exponent in the size of a maximal cyclic subgroup
    of a Sylow p-subgroup of the group.
    If we ignore those numbers we get a slightly worse bound, that still works
    well for our case."""
    listota=[prc[1] for prc in primedecomposition(number)]
    bigsum=sum(listota)
    return bigsum
def testassociativity(table,base):
    """Verifies Associativity of a given operation table with base_set base."""
    ass=True
    for i in base:
        for j in base:
            for k in base:
                leftele=table[(table[(i,j)],k)]
                rightele=table[(i,table[(j,k)])]
                if leftele!=rightele:
                    ass=False
                    break
            if not ass:
                break
        if not ass:
            print("Warning, not associative")
            break
    return ass
def testclosure(table,base):
    """Verifies Closure of a given operation table with base_set base."""
    clo=True
    cart=[(leftele,rightele) for leftele in base for rightele in base]
    for pair in cart:
        if table[pair] not in base:
            clo=False
            print("Warning, not closed.")
            break
    return clo
def testid(table,base):
    """Verifies if there is an identity element of a given operation table
    with base_set base."""
    ids=[]
    for i in base:
        isid=True
        for j in base:
            if table[(j,i)]!=j:
                isid=False
                break
        if isid:
            ids.append(i)
    if len(ids)!=0:
        return ids
    print("Warning, not identity")
    return False
def getinverses(table,base,identity):
    """Verifies if all elements of a given operation table with base_set base
    with an identity have an inverse."""
    inverses=[]
    for i in base:
        hasinverse=False
        for j in base:
            if table[(i,j)]==identity:
                hasinverse=True
                inverses.append((i,j))
                break
        if not hasinverse:
            print("Warning, not inverses")
            return False
    return inverses
class Group:
    """
    The Group object implements a group in python.
    It has:
        base (the base set)
        table (the group table)
        identity (an identity element)
        inverses (a list of all pairs of inverses)
    """
    def __init__(self,table,s=0):
        #s!=0 to skip checks. Use if you already know the table defines a group.
        base=set(table.values())
        identity=''
        inverses=[]
        if s==0:
            clo=testclosure(table,base)
            ass=testassociativity(table,base)
            idd=testid(table,base)
            identity=idd[0]
            inverses=getinverses(table,base,identity)
            inv=bool(inverses)
        if s!=0:
            clo=True
            ass=True
            idd=True
            inv=True
            cart={(leftele,rightele) for leftele in base for rightele in base}
            for pair in cart:
                if table[pair]==pair[1]:
                    identity=pair[0]
            for pair in cart:
                if table[pair]==identity:
                    inverses.append(pair)
        self.inverses=set(inverses)
        self.base=base
        self.table=table
        self.iden=identity
        if clo and ass and idd and inv:
            self.isgroup=True
        else:
            print("Warning: Not a group")
            self.isgroup=False
    def subgroup(self,sub_set):
        """Checks if sub_set is a subgroup of self.
        We assume all groups are finite, so we only need to make the subtable
        and test closure."""
        if sub_set.issubset(self.base):
            subtable={}
            cart=[(leftele,rightele) for leftele in sub_set for rightele in sub_set]
            issub=True
            for pair in cart:
                if self.table[pair] not in sub_set:
                    issub=False
                    return issub
                subtable[pair]=self.table[pair]
            return Group(subtable,1)
        return False
    def __str__(self):
        """For __str__ it's the best to have the command return the group table"""
        return str(self.table)
    def __eq__(self,other):
        """Two groups self and other are equal if have the same base set and the same table."""
        return self.base==other.base and self.table==other.table
    def __add__(self,other):
        """Implementation of direct product of self and other."""
        table_1=self.table
        table_2=other.table
        first_base=self.base
        second_base=other.base
        direct_base={(leftele,rightele) for leftele in first_base for rightele in second_base}
        cart={(leftele,rightele) for leftele in direct_base for rightele in direct_base}
        sumtable={}
        for pair in cart:
            left=pair[0]
            right=pair[1]
            sumtable[pair]=(table_1[(left[0],right[0])],table_2[(left[1],right[1])])
        return Group(sumtable)
    def inverse(self,ele):
        """Computes the inverse of an element. Not very efficient.
        But not very expensive either."""
        if ele not in self.base:
            return False
        for pair in self.inverses:
            if ele in pair:
                if ele==pair[0]:
                    return pair[1]
                return pair[0]
        return False
    def gen(self,sub_set):
        "Computes the subgroup generated by a sub_set of elements of self."
        if sub_set==set():
            return {self.iden}
        group_elements={Groupelement(self,ele) for ele in sub_set}
        gen_sugbroup=set()
        queue=[Groupelement(self,self.iden)]
        while queue!=[]:
            for queued in queue:
                queue.remove(queued)
                if queued.name in gen_sugbroup:
                    continue
                gen_sugbroup.add(queued.name)
                for ele in group_elements:
                    plus=queued+ele
                    queue.append(plus)
        return gen_sugbroup
    def subgroups(self):
        """Computes all the subgroups of self. This kind of method requires
        a lot of optimization. The naive algorithm is to compute all the
        subsets and check whether each one of them is a subgroup.
        In the case of a group with 24 elements this is not good. A group with
        24 elements has 16777216 subsets. In this method we implement the
        Newman bound to limit the number of generators, and we generate all
        the subgroups with up to that number of generators.
        In a group of 24 elements this means we need to compute up all the
        nonempty subsets with up to 6 elements, which is 190050 subsets.
        Still not the best, but way better than the naive way. """
        bound=newmanbound(len(self.base))
        gens=goodsubsets(self, bound)[0]
        subgrouplist=[self.subgroup(self.gen(gs)) for gs in gens]
        #Following is deprecated
        #subbase=set()
        #sub_sets=subsets(self.base,bound)
        #for sub_set in sub_sets:
        #    gen_sugbroup=self.gen(sub_set)
        #    subbase.add(frozenset(gen_sugbroup))
        #subgrouplist=[self.subgroup(gen_sugbroup) for gen_sugbroup in subbase]
        return subgrouplist
    def normalsubgroups(self):
        """Computes the normal subgroups of self"""
        subgrouplist=self.subgroups()
        table=self.table
        norm=[]
        for sub_group in subgrouplist:
            isnormal=True
            for i in self.base:
                for j in sub_group.base:
                    conj=table[(table[(i,j)],self.inverse(i))]
                    if conj not in sub_group.base:
                        isnormal=False
                        break
                if not isnormal:
                    break
            if isnormal:
                norm.append(sub_group)
        return norm
    def isitabelian(self):
        """Checks if group is abelian"""
        abel=True
        cart=[(leftele,rightele) for leftele in self.base for rightele in self.base]
        for pair in cart:
            if self.table[pair] != self.table[(pair[1],pair[0])]:
                abel=False
                break
        return abel
    def sylowsubgroups(self):
        """Computes the Sylow Subgroups of self"""
        sylow=[]
        number=len(self.base)
        primedec=primedecomposition(number)
        primecomponents=[primexp[0]**primexp[1] for primexp in primedec]
        for sub_group in self.subgroups():
            if len(sub_group.base) in primecomponents:
                sylow.append(sub_group)
        return sylow
    def maximalsubgroups(self):
        """Computes the maximal subgroups of self"""
        subgrouplist=self.subgroups()
        maxi=[]
        for sub_group in subgrouplist:
            ismaximal=True
            if len(sub_group.base)==len(self.base):
                ismaximal=False
            for sub_group_2 in subgrouplist:
                bool_1=len(sub_group_2.base)!= len(self.base)
                bool_2=(sub_group.base).issubset(sub_group_2.base)
                bool_3=not sub_group==sub_group_2
                if bool_1 and bool_2 and bool_3:
                    ismaximal=False
                    break
            if ismaximal:
                maxi.append(sub_group)
        return maxi
    def isitnilpotent(self):
        """Verifies if self is nilpotent, by checking if all the maximal
        subgroups are normal.
        It's the easiest characterization to implement that I know of.
        Altenratively, if we make a method to compute the Sylow subgroups
        we can do the same, since a group is nilpotent iff all the Sylow
        subgroups are normal."""
        sylow=self.sylowsubgroups()
        norm=self.normalsubgroups()
        intersection=[]
        for sub_group in sylow:
            for sub_group_2 in norm:
                if sub_group==sub_group_2 and sub_group not in intersection:
                    intersection.append(sub_group)
        return len(sylow)==len(intersection)
class PermutationGroup(Group):
    """Permutation groups deserve to have their own class."""
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-locals
    # This is reasonable for such a big class.
    # pylint: disable=super-init-not-called
    # PermutationGroup is a Group, but the initialization is way different.
    def __init__(self,size):
        iden=identitymatrix(size)
        base1=permutations(iden)
        base=range(len(base1))
        table={}
        cart=[(a,b) for a in base for b in base]
        for pair in cart:
            prod=sqmatrixproduct(base1[pair[0]],base1[pair[1]],size)
            prod_index=base1.index(prod)
            table[pair]=prod_index
        thegroup=Group(table)
        self.base=thegroup.base
        self.table=table
        self.inverses=thegroup.inverses
        self.iden=thegroup.iden
        self.matrices={}
        self.number=size
        for ele in base:
            self.matrices[ele]=base1[ele]
        self.twoline={}
        for ele in base:
            self.twoline[ele]=two_line(self.matrices[ele])
        self.cycdec={}
        for ele in base:
            cycles=cycle_decomposition(self.twoline[ele])
            self.cycdec[ele]=cycles
        self.transdec={}
        for ele in base:
            cycles=cycle_decomposition(self.twoline[ele])
            trans=transposition_decomposition(cycles)
            self.transdec[ele]=trans
    def isitabelian(self):
        """Checks if group is abelian"""
        if self.number==2:
            return True
        return False
    def isitnilpotent(self):
        """Verifies if self is nilpotent, by checking if all the maximal
        subgroups are normal.
        It's the easiest characterization to implement that I know of.
        Altenratively, if we make a method to compute the Sylow subgroups
        we can do the same, since a group is nilpotent iff all the Sylow
        subgroups are normal."""
        if self.number==2:
            return True
        return False
class Groupelement:
    """A group element consists of the name it has in the group, and the
    information of the group table."""
    def __init__(self,group,tag):
        self.name=tag
        self.group=group
    def __add__(self,other):
        """We can add elements in a group by using the information on the table."""
        return Groupelement(self.group,self.group.table[(self.name,other.name)])
    def __str__(self):
        """They return their name when printed."""
        return str(self.name)
    def __sub__(self,other):
        """They can be inverted."""
        return Groupelement(self.group,self.group.table[(self.name,self.group.inverse(other.name))])
    def order(self):
        """The order can easily be calculated."""
        counter=1
        ele=self
        while ele.name != self.group.iden:
            ele+=self
            counter+=1
        return counter
class Permutation(Groupelement):
    # pylint: disable=super-init-not-called
    """Permutations are elements of a PermutationGroup that behave
    as functions."""
    def __init__(self,permgroup,index):
        self.name=index
        self.group=permgroup
        self.twoline=permgroup.twoline[index]
        self.matrix=permgroup.matrices[index]
        self.cycles=permgroup.cycdec[index]
        self.trans=permgroup.transdec[index]
    def __call__(self,element):
        if element in list(self.name.keys()):
            return self.name[element]
        return "Wrong"
    def __str__(self):
        return str(self.twoline)
    def __repr__(self):
        return str(self.cycles)
    def __mul__(self,other):
        return Permutation(self.group,(self+other).name)
