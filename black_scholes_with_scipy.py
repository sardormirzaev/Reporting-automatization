# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 13:39:39 2019

@author: Bernd Lewerenz
"""

# Implements lognormal BS on top of scipy/norm

# Prints as Example  Delta and Vega for Inflation Options (EUHICP)

from scipy.stats import norm
import numpy as np

N=10000 # Nominal for Basis Points
#I_i = 91.46 # EU-HICP unser Linker initial
I_i = 105.4 # EU-HICP - heute (BaseIndex)
#I_e = I_i * 1.2
#I_e = 106.4 #EU-HICP 1 year
#I_e = 422.07 # UK-RPI 10 Years
I_e = 116.08 # EU-HICPXT Forward for 10 years
sigma = 0.02 # I-Vol für ein Jahr EUHICP
expiryTime = 10


# This is from Hull 7th Edition page 350 Formula 16.10

def lognormal_black(Fwd,X,sigma,T,DF=1.0 , cp=1):
    d1 = (np.log(Fwd/X) + np.square(sigma) * T * 0.5)/(sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return (cp * DF * ( Fwd * norm.cdf(cp * d1) - X * norm.cdf(cp * d2)))

# Example Deflation Protection that is a zero Strike zc Put Option on the index
value_base = N * lognormal_black(I_e,I_i,sigma,expiryTime,cp=-1) / I_i
value_up = N * lognormal_black(I_e*1.01,I_i,sigma,expiryTime,cp=-1) / I_i
value_vol_up = N * lognormal_black(I_e,I_i,sigma * 1.01,expiryTime,cp=-1) / I_i

print("\nGreeks and Value of Inflation Option (Deflation Protection) \nbased on scipy/norm")
print("All Values in Basis Points\n\n")
print("delta: ", value_up - value_base,"\tVega: ", value_vol_up - value_base,
      "\t Price: ", value_base)