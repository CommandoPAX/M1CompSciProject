# Main file to execute rest of the code

import numpy as np
from Core.Physics import *
from Core.Plot_Handler import *
from Core.Config_Loader import Config_Loader
from Flux_Solver.Lax_Friedrich import*
from Core.Conservative_State_Solver import*
from Riemann_Solver.Riemann_Solver import Riemann


if __name__ == "__main__" :

    # We generate the space in which we'll work and we intialize all useful variables as 0 over this space
    config = Config_Loader()
    n_cell = config.DATA["n_cell"]

    X = np.linspace(0,1,num=n_cell)
    
    """rho = np.zeros(n_cell)
    u = np.zeros(n_cell)
    P = np.zeros(n_cell)

    # Load all initial conditions
    # To change initial conditions, change config name in Core/Config_Loader.py

    rho[:n_cell//2] = config.DATA["rho_inf"]
    u[:n_cell//2] = config.DATA["u_inf"]
    P[:n_cell//2] = config.DATA["P_inf"]
        
    rho[n_cell//2:] = config.DATA["rho_sup"]
    u[n_cell//2:] = config.DATA["u_sup"]
    P[n_cell//2:] = config.DATA["P_sup"]        
    
    Ttot = 0

    U = U_(rho,u,P)
    dx = X[1]-X[0]

    while 1 :
        Ttot += delta_t(U[:, 1], a_(U[:, 2], U[:, 0]),dx)
        #print(Ttot)
        U = U_next(U,dx,"LW")
        if Ttot > 0.25 : break
        
    # TEST

    Resultat = U_a_la_moins_un(U)"""
    
    Resultat = Riemann(0.001)
    Create_Plots(X,Resultat)
    
