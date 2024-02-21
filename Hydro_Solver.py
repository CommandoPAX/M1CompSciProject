# Main file to execute rest of the code

import numpy as np
from tkinter import*
from math import*

from Core.Variables import *
from Core.Plot_Handler import *
from Core.Config_Loader import Config_Loader

config = Config_Loader()

if __name__ == "__main__" :

    # Conditions initiales

    #Théo : faudra l'implémenter avec une config modifiable, je m'en occuperai c'est pas très compliqué

    X = np.linspace(0,1,num=config["n_cell"])

    rho = np.ones(config.DATA["n_cell"])
    u=np.zeros(config.DATA["n_cell"])
    P = np.ones(config.DATA["n_cell"])
    rho[config.DATA["n_cell"]//2:] = 0.125
    P[config.DATA["n_cell"]//2:] = 0.1

    W = W_(rho, u, P)    

    Create_Plots(X,W)
