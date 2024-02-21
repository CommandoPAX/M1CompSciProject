# Handles computing derivative

import numpy as np
from Core.Config_Loader import Config_Loader

def derivee (f : function, x : np.array):
    """ 
    Computes a simple derivative using transmissive boundary conditions
    """
    config = Config_Loader()
    y = f(x)
    dx = x[1]-x[0]
    yp = np.zeros(config.DATA["n_cell"])
    for i in range(len(x)):
        if i >=1 and i+1 < len(x) : 
            yp[i] = (y[i-1]+y[i+1])/(2*dx)

        # Transmissive boundary condition

        if i == 0 :
            yp[i] = (y[0]+y[1])/(2*dx)
        if i+1 == len(x) : 
            yp[i] = (y[i-1]+y[i])/(2*dx)

    return yp