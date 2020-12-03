from numba import jit
from sympy.functions.combinatorial.factorials import binomial
from mpmath import hyp2f1, power, fsum, fprod, isnan

@jit
def Ptrue(Qp, I, R, S, Q, b, replacement = True): 
    """
    Returns the probability of testing with replacement,
    in which tested individuals can be retested on the same day.
    
    Args
    ----
    Qp (int): number of positive tests.
    I (int): number of infecteds.
    R (int): number of recovered.
    S (int): number of suceptibles.
    Q (int): number of tests.
    b (float): biased-testing factor.
    replacement (boolean): testing with/without replacement.
    
    """
        
    if replacement:
        f = b * ( I + R ) / ( b * ( I + R ) + S/b )
        
        Ptrue = binomial(Q, Qp) * power(f,Qp) * power(1-f,Q-Qp)
        
    else:
        product_1 = [ 1/( b * ( I + R ) + S/b - n) for n in range(Q) ]
        product_2 = [ b * ( I + R ) - k for k in range(Qp) ]
        product_3 = [ S/b - l for l in range(Q-Qp) ]
        
        Ptrue = binomial(Q, Qp) * fprod(product_1) * fprod(product_2) * fprod(product_3)
    
    return Ptrue

@jit
def Perr(Qtildep, Q, Qp, FNR, FPR): 
    """
    Returns observed error-prone probability distribution.
    
    Args
    ----
    Qtildep (int): number of positive tests.
    Qp (int): number of positive tests.
    Q (int): number of tests.
    FNR (float): false-negative fraction.
    FPR (float): false-positive fraction.
    
    """
    
    Qm = Q - Qp
    
    Perr = power(FNR, Qp) * power(1 - FPR, Qm - Qtildep ) * power(FPR, Qtildep) \
           * binomial( Qm, Qtildep ) * hyp2f1( -Qp, -Qtildep, Qm + 1 - Qtildep, \
           (FNR-1)*(FPR-1)/(FNR*FPR) )
        
    if isnan(Perr):
        Perr = 0
        
    return Perr

@jit
def Ptot(Qtildep, I, S, R, Q, b, FNR, FPR, replacement = True):
    """
    Returns observed error-prone probability distribution.
    
    Args
    ----
    Qtildep (int): number of positive tests.    
    Qp (int): number of positive tests.
    FNR (float): false-negative fraction.
    FPR (float): false-positive fraction.
    replacement (boolean): testing with/without replacement.
    
    """
    
    Ptot = [ Perr(Qtildep, Q, Qp, FNR, FPR) * 
           Ptrue(Qp, I, R, S, Q, b, replacement) for Qp in range(Q+1) ]
               
    Ptot = fsum(Ptot)
    
    Ptot = float(Ptot)
    
    print( "(Qtildep/Q,Ptot)=(%f,%f)"%(Qtildep/Q,Ptot) ) 
    return Ptot