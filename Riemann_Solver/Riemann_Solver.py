# Riemann solver based on the fortran program in Toro 1999

from Core.Config_Loader import Config_Loader
from Riemann_Solver.subroutine import *
import numpy as np
    
def Riemann(t) : 
    
    config = Config_Loader()

    # Compute Gamma related constants
    G4 = 2/(config.DATA["gamma"]-1)

    # Compute sound speeds 

    CL = np.sqrt(config.DATA["gamma"]*config.DATA["P_inf"]/config.DATA["rho_inf"])
    CR = np.sqrt(config.DATA["gamma"]*config.DATA["P_sup"]/config.DATA["rho_sup"])

    # We test for the intial pressure conditions 

    TIMEOUT = t #seconds (maybe)
    DIAPH = 0.5 #Discontinuity position, considered at 0.5*L, unsure if this value is correct
    
    U = np.zeros((config.DATA["n_cell"],3))
    
    if (G4 *(CL+CR)) <= (config.DATA["u_sup"] - config.DATA["u_inf"]) :
        print("Vacuum is generated by data")
    else : 
        # Exact solution for presure and velocity in star region is found 
        PM = 0 
        UM = 0
        PM, UM = STARPU(PM, UM)
        dx = config.DATA["L"]/config.DATA["n_cell"]
        
        # Complete solution at time TIMEOUT is found
        for i in range(1, config.DATA["n_cell"]) : 
            XPOS = (float(i) - 0.5)*dx 
            S = (XPOS - DIAPH)/TIMEOUT 
            
            # Solution at point (X,T) = (XPOS - DIAPH, TIMEOUT) is found
            U[i, 0], U[i, 1], U[i, 2] = SAMPLE(PM, UM, S)
            
        return U
            