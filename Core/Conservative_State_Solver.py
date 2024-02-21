# Handles the resolution of the conservative flux for each cell

import numpy as np
from Core.Config_Loader import*
from Core.Physics import *
from Flux_Solver.Lax_Friedrich import *
from Flux_Solver.Lax_Wendroff import * 
from Flux_Solver.Godunov import *

def U_next(U : np.array, dx, intercell : str = "LF") : 
    """
    Uses the state of the physical system at a time t to calculate the state at the time t + delta_t
    U = array([rho_i, u_i, P_i]) where i is the cell index
    With this convention, U[:, 0] is every density, U[:, 1] every speed, U[:, 2] every pressure
    """
    dt = delta_t(U[:, 1], a_(U[:, 2], U[:, 0]),dx)
    if intercell == "LF" :
        return np.array(U + (dt/dx)*(F12_Friedrich(U,dx,dt,signe="-") - F12_Friedrich(U,dx,dt,signe="+")))
    if intercell == "LW" :
        return np.array(U + (dt/dx)*(F12_Wendroff(U,dx,dt) - F12_Wendroff(U,dx,dt)))
    if intercell == "Go" : 
        return "Not Yet Implemented"