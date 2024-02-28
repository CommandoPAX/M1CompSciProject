# Main file to execute rest of the code

import numpy as np
from Core.Physics import *
from Core.Plot_Handler import *
from Core.Config_Loader import Config_Loader
from Flux_Solver.Lax_Friedrich import*
from Core.Conservative_State_Solver import*

def NewConfig ():
    Create_New_Config = input("Do you wish to create a new config file (y/n) ? ")
    
    if Create_New_Config == "y" or Create_New_Config == "Y" : #Currently doesn't work, didn't have time to finish before having to leave
        _Gamma = float(input("Gamma ? "))
        _L = float(input("L ? "))
        _n_cell = int(input("n_cell ? "))
        _C = float(input("C ? "))
        _rho_inf = float(input("rho_inf ? "))
        _rho_sup = float(input("rho_sup ? "))
        _u_inf = float(input("u_inf ? "))
        _u_sup = float(input("u_sup ? "))
        _P_inf = float(input("P_inf ? "))
        _P_sup = float(input("P_sup ? "))
        config.generate_new_config(_Gamma, _L, _n_cell, _C, _rho_inf, _rho_sup, _u_inf, _u_sup, _P_inf, _P_sup, "New_Config")


if __name__ == "__main__" :

    # We generate the space in which we'll work and we intialize all useful variables as 0 over this space
    config = Config_Loader()
    n_cell = config.DATA["n_cell"]

    X = np.linspace(0,1,num=n_cell)
    
    rho = np.zeros(n_cell)
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

    Resultat = U_a_la_moins_un(U)
  
    Create_Plots(X,Resultat)
