# Godunov flux solver

# Requirements : 
# - Should output something usable by Conservative_State_Solver

import numpy as np
from Core.Physics import*


def F12_Godunov (U : np.array, dx, dt : float, n : int, signe : str ="+"):
    
    n_cell = len(U[:,0])

    R = np.zeros((n_cell,3))

    if signe == "+":
        for i in range(n_cell):
            R[i] = (1/dt)*Integral(n*dt, (n+1)*dt, F_(U_RiemR(n))) #U_RiemR= Solution exact de Riemann au problème entre i et i+1
            #La formule est F(n*dt, entre cell i et i+1)= (1/dt)* Intégrale(n*dt -> (n+1)*dt, F_(U_Riemann(entre i et i+1, temps n*dt)))
    elif signe == "-":
        for i in range(n_cell):
            R[i] = (1/dt)*Integral(n*dt, (n+1)*dt, F_(U_RiemL(n))) #U_RiemR= Solution exact de Riemann au problème entre i-1 et i

    return R