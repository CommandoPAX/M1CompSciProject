# Main file to execute rest of the code

import numpy as np
from tkinter import*
from math import*

from Core.Variables import *
from Core.Plot_Handler import *
from Core.Config_Loader import Config_Loader

config = Config_Loader()

if __name__ == "__main__" :

    X = np.linspace(0,1,num=config["n_cell"])
    
    rho = np.zeros(config.DATA["n_cell"])
    u = np.zeros(config.DATA["n_cell"])
    P = np.zeros(config.DATA["n_cell"])

    # Load all initial conditions
    rho[:config.DATA["n_cell"]//2] = config.DATA["rho_inf"]
    u[:config.DATA["n_cell"]//2] = config.DATA["u_inf"]
    P[:config.DATA["n_cell"]//2] = config.DATA["P_inf"]
    
    rho[config.DATA["n_cell"]//2:] = config.DATA["rho_sup"]
    u[config.DATA["n_cell"]//2:] = config.DATA["u_sup"]
    P[config.DATA["n_cell"]//2:] = config.DATA["P_sup"]

    W = W_(rho, u, P)    

    Create_Plots(X,W)
