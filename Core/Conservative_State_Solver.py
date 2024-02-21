# Handles the resolution of the conservative flux for each cell

import numpy as np

def F_(U : np.array, gamma : float):
    return np.array([U[0], 0.5*(3-gamma)*U[1]**2/U[0]+(gamma-1)*U[2], U[1]/U[0]*U[2]-0.5*(gamma-1)*U[1]**3/U[0]**2])