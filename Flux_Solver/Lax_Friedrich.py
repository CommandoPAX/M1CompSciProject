# Solves the Lax-Friedrich flux

import numpy as np
from Core.Config_Loader import Config_Loader
from Core.Error_Handler import LogError

def F12_Friedrich (U, X, dt):
    global n_cell
    R = np.zeros(n_cell,3)
    dx = X[1]-X[0]

    print(R.shape())

    for i in range(3):
        for j in range(n_cell) :
            R[i][j] = 0.5*(F(U[i][j])+F(U[i][j+1]))+0.5*dx/dt*(U[i][j]-U[i][j+1])
