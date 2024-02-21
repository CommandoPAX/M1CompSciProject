# Solves the Lax-Friedrich flux

import numpy as np
from Core.Config_Loader import Config_Loader
from Core.Error_Handler import LogError
from Core.Conservative_State_Solver import*

config = Config_Loader()

def F12_Friedrich (U, X, dt):

    n_cell = config.DATA["n_cell"]

    R = np.zeros((3,n_cell))
    dx = X[1]-X[0]

    print(R[0].shape)

    for i in range(3):
        for j in range(n_cell) :
            R[i][j] = 0.5*(F_(U[i][j])+F_(U[i][j+1]))+0.5*dx/dt*(U[i][j]-U[i][j+1])
