# Handles the resolution of the conservative flux for each cell

import numpy as np
from Core.Error_Handler import LogError

def F_(U : np.array, gamma : float):
    """ 
    Computes the flux function as defined on page 1 of the subject
    """
    try : 
        return np.array([U[0], 0.5*(3-gamma)*U[1]**2/U[0]+(gamma-1)*U[2], U[1]/U[0]*U[2]-0.5*(gamma-1)*U[1]**3/U[0]**2])
    except Exception as e :
            LogError("F_", e)
            print(e)