# Solves the Lax-Friedrich flux

import numpy as np
from Core.Config_Loader import Config_Loader
from Core.Error_Handler import LogError
from Core.Conservative_State_Solver import*

config = Config_Loader()

def F12_Friedrich (U, X, dt):

    global n_cell

    R = np.zeros((n_cell,3))
    dx = X[1]-X[0]

    print(U[0].shape)

    for i in range(n_cell):
        if i+1 <n_cell : R[i] = 0.5*(F_(U[i])+F_(U[i+1]))+0.5*dx/dt*(U[i]-U[i+1])

    return R