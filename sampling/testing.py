from numba import jit
from sympy.functions.combinatorial.factorials import binomial
from mpmath import hyp2f1, power, fsum, fprod, isnan, exp, sqrt, pi

# testing bias function
B = lambda b, f0: exp(b)/(1-f0+f0*exp(b))

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
        f0 = ( I + R ) / ( S + I + R )
        Ptrue = binomial(Q,Qp) * power(f0*exp(b),Qp) * power(1-f0,Q-Qp)
        Ptrue /= power(1+(exp(b)-1)*f0,Q)
        
    else:
        product = [ ( I + R - k )/( S - Q + Qp - k ) for k in range(Qp) ]
        
        Ptrue = binomial(Q, Qp) * fprod(product) * exp(Qp*b) * \
                1/hyp2f1( -I - R, -Q, S - Q + 1, exp(b) )

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

@jit
def Ptot_approximation(Qtildep, I, S, R, Q, b, FNR, FPR):
    """
    Returns observed error-prone probability distribution.
    
    Args
    ----
    Qtildep (int): number of positive tests.    
    Q (int): number of tests.
    I (int): number of infecteds.
    R (int): number of recovered.
    S (int): number of suceptibles.
    b (float): biased-testing factor.
    FNR (float): false-negative fraction.
    FPR (float): false-positive fraction.
    
    """
    
    P = lambda Qtildep, mu, sigma: exp(-(Qtildep-mu)**2/(2*sigma**2)) \
                                   /(sigma*sqrt(2*pi))
    
    
    f0 = ( I + R ) / ( S + I + R )
    f = f0 * B(b,f0)
    
    mu = Q * ( f * ( 1 - FNR ) + ( 1 - f ) * FPR )
    sigma = sqrt(mu * (1 -  ( f * ( 1 - FNR ) + ( 1 - f ) * FPR )))#sqrt( Q * ( 1 - f ) * FPR * ( 1 - FPR ) + \
            #Q * f * FNR * ( 1 - FNR ) + Q * f * ( 1 - f ) * ( 1 - FNR -FPR ) )
    
    return P(Qtildep, mu, sigma)
