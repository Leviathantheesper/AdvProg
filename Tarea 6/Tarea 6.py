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
    def __init__(self, message="You broke it. Congratulations"):
        self.message = message
        super().__init__(self.message)
class nonegativos(Exception):
    """Ejemmmm, nonnegative integers... please?"""
    pass
    def __init__(self, message="No negativos por favor."):
        self.message = message
        super().__init__(self.message)
def C(n):
    """Este método aplica la función de Collatz a un entero no negativo. Si la entrada no es un entero falla y regresa un error."""
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
    """Este método verifica la conjetura de Collatz para el entero n. 
    Si recibe -404 envía un error. Si el numero de iteraciones de C(n) 
    es superior a 100 interrumpe el método y envía un error con 
    el último valor de la secuencia."""
    t=0
    if n<0 and n!=-404:
        raise nonegativos()
        return -168
    while n>1:
        print(n)
        n=C(n)
        t+=1
        if t>100:
            raise Attemptoverflow(n)
    if n==-404:
        raise Broken()
    if n==1:
        print(n)
        return True
    else:
        print(n)
        return False
Collatz(160) #para funcionamiento normal
#Collatz(27) #para AttemptOverflow.
#Collatz(3.1) #para NononoEnteroseorfavor y Broken.
#Collatz(-2) #para nonegativos