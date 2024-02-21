# Solves the Lax-Friedrich flux

import numpy as np
from Core.Config_Loader import Config_Loader
from Core.Physics import*

def F12_Friedrich (U : np.array, X : np.array, dt : float, signe : str ="+"):
    
    config = Config_Loader()
    n_cell = config.DATA["n_cell"]
    
    R = np.zeros((n_cell,3))
    dx = X[1]-X[0]


    if signe == "+":
        for i in range(n_cell):
            if i+1 != n_cell : R[i] = 0.5*(F_(U[i])+F_(U[i+1]))+0.5*dx/dt*(U[i]-U[i+1])
            if i+1 == n_cell : R[i] = 0.5*(F_(U[i])+F_(U[i]))+0.5*dx/dt*(U[i]-U[i])
    if signe == "-":
        for i in range(n_cell):
            if i != 0 : R[i] = 0.5*(F_(U[i-1])+F_(U[i]))+0.5*dx/dt*(U[i-1]-U[i])
            if i== 0 : R[i] = 0.5*(F_(U[i-1])+F_(U[i-1]))+0.5*dx/dt*(U[i-1]-U[i-1])

    else :
        raise ZeroDivisionError("tout est faux aaaaaaaaaaaaaah")

    return R