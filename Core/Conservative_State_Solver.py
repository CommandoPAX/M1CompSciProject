# Handles the resolution of the conservative flux for each cell

import numpy as np
from Core.Error_Handler import LogError
from Core.Config_Loader import *
from Core.Physics import *

def F_(U : np.array):
    """ 
    Computes the flux function as defined on page 1 of the subject
    """
    config = Config_Loader()
    gamma = config.DATA["gamma"]
    try : 
        return np.array([U[0], 0.5*(3-gamma)*U[1]**2/U[0]+(gamma-1)*U[2], U[1]/U[0]*U[2]-0.5*(gamma-1)*U[1]**3/U[0]**2])
    except Exception as e :
            LogError("F_", e)
            print(e)
            
def U_next(U : np.array, FluxIntercell : np.array, dx : float) : 
    return np.array(U + (delta_t(U[:, 1], a_(U[:, 2], U[:, 0]))/dx)*(FluxIntercell(i-1/2) + FluxIntercell(i+1/2)))