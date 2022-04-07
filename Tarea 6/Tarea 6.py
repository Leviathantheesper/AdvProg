# -*- coding: utf-8 -*-
class NononoEnterosporfavor(Exception):
    """No, no, no!!! Integers Only, Please"""
    pass
class Attemptoverflow(Exception):
    """This is such a looooooooong Collatz sequence.
    
    Attributes:
        ene -- Last number in the sequence until error occured.
        message -- explanation of the error
    """
    pass
    def __init__(self, ene, message="This is such a long Collatz sequence, please stop and continue from "):
        self.ene = ene
        self.message = message+str(ene)
        super().__init__(self.message)
class Broken(Exception):
    """NOPE"""
    pass

def C(n):
    """Este método aplica la función de Collatz a un entero. Si la entrada no es un entero falla"""
    try:
        if type(n) != type(1):
            raise NononoEnterosporfavor
        elif n%2==0:
            return n//2
        else:
            return 3*n+1
    except NononoEnterosporfavor:
        print("No, no, no!!! Integers Only, Please")
        n=-404
        return n
        
def Collatz(n):
    print("Inicio")
    t=0
    while n>1:
        print(n)
        n=C(n)
        t+=1
        if t>100:
            raise Attemptoverflow(n)
    if n==-404:
        s="You broke it. Congratulations."
        return(s)
        print(s)
        raise Broken(1)
    if n==1:
        return True
    else:
        return False
print(Collatz(27))