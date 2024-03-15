# Law-Wendroff

import numpy as np
from Core.Physics import *

def F12_Wendroff (U : np.array, dx, dt : float, signe : str="+"):
    
    
    n_cell = len(U[:,0])

    R = np.zeros((n_cell,3))

    if signe == "+":
        for i in range(n_cell):
            if i+1 != n_cell : R[i] = F_(0.5*(U[i+1]+U[i])-0.5*dt/dx*(F_(U[i+1])-F_(U[i])))
            if i+1 == n_cell : R[i] = F_(0.5*(U[i]+U[i])-0.5*dt/dx*(F_(U[i])-F_(U[i])))
    elif signe == "-":
        for i in range(n_cell):
            if i!=0 : R[i] = F_(0.5*(U[i-1]+U[i])-0.5*dt/dx*(F_(U[i])-F_(U[i-1])))
            if i==0 : R[i] = F_(0.5*(U[i]+U[i])-0.5*dt/dx*(F_(U[i])-F_(U[i])))

    return R