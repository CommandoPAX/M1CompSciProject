# Main file to execute rest of the code

import numpy as np
from Core.Variables import *
from Core.Plot_Handler import *
from Core.Config_Loader import Config_Loader

config = Config_Loader()

if __name__ == "__main__" :

    # We generate the space in which we'll work and we intialize all useful variables as 0 over this space

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
    
    # Plots the initial conditions only for now

    W = W_(rho, u, P)    
    Create_Plots(X,W)
