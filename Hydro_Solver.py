# Main file to execute rest of the code

import numpy as np
from Core.Physics import *
from Core.Plot_Handler import *
from Core.Config_Loader import Config_Loader
from Flux_Solver.Lax_Friedrich import*

def NewConfig ():
    Create_New_Config = input("Do you wish to create a new config file (y/n) ? ")
    
    if Create_New_Config == "y" or Create_New_Config == "Y" : #Currently doesn't work, didn't have time to finish before having to leave
        Gamma = float(input("Gamma ? "))
        L = float(input("L ? "))
        n_cell = int(input("n_cell ? "))
        C = float(input("C ? "))
        # rho = list(input())
        # u = 
        # P = 
        #config.generate_new_config(gamma, L, n_cell, C, rho, u, P, "New_Config")


if __name__ == "__main__" :

    # We generate the space in which we'll work and we intialize all useful variables as 0 over this space
    config = Config_Loader()
    n_cell = config.DATA["n_cell"]

    X = np.linspace(0,1,num=config.DATA["n_cell"])
    
    rho = np.zeros(config.DATA["n_cell"])
    u = np.zeros(config.DATA["n_cell"])
    P = np.zeros(config.DATA["n_cell"])

    # Load all initial conditions
    # To change initial conditions, change config name in Core/Config_Loader.py

    rho[:config.DATA["n_cell"]//2] = config.DATA["rho_inf"]
    u[:config.DATA["n_cell"]//2] = config.DATA["u_inf"]
    P[:config.DATA["n_cell"]//2] = config.DATA["P_inf"]
        
    rho[config.DATA["n_cell"]//2:] = config.DATA["rho_sup"]
    u[config.DATA["n_cell"]//2:] = config.DATA["u_sup"]
    P[config.DATA["n_cell"]//2:] = config.DATA["P_sup"]        
    
    U = U_(rho,u,P)
    print(U.shape)
    F12_Friedrich(U,X,0.01)

    
    # Plots the initial conditions only for now

    W = W_(rho, u, P)    
    Create_Plots(X,W)
