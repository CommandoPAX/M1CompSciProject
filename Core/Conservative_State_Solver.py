# Handles the resolution of the conservative flux for each cell

import numpy as np
from Core.Error_Handler import LogError
from Core.Config_Loader import*
from Core.Physics import *
from Flux_Solver.Lax_Friedrich import*

def F_(U : np.array):
    """ 
    Computes the flux function as defined on page 1 of the subject
    """
    config = Config_Loader()
    gamma = config.DATA["gamma"]
    
    return np.array([U[0], 0.5*(3-gamma)*U[1]**2/U[0]+(gamma-1)*U[2], U[1]/U[0]*U[2]-0.5*(gamma-1)*U[1]**3/U[0]**2])

            
def U_next(U : np.array, FluxIntercell : np.array, X) : 
    """
    Uses the state of the physical system at a time t to calculate the state at the time t + delta_t
    U = array([rho_i, u_i, P_i]) where i is the cell index
    With this convention, U[:, 0] is every density, U[:, 1] every speed, U[:, 2] every pressure
    """
    i = 0 #Placeholder while waiting for the intercell flux function
    return np.array(U + (delta_t(U[:, 1], a_(U[:, 2], U[:, 0]))/dx)*(F12_Friedrich(U,X,dt,signe="-") - F12_Friedrich(U,X,dt,signe="+")))