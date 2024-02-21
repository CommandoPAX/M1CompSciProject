# Don't know any good title

import numpy as np
from Core.Config_Loader import Config_Loader

config = Config_Loader()
gamma = config.DATA["gamma"]

def P_(rho : np.array, K : float) :
    """ 
    Computes the pressure using the polytropic equation of state with explonent gamma
    """
    global gamma
    return K * np.pow(rho,gamma)

def a_(P : np.array, rho : np.array):
    """ 
    Computes the speed of sound as defined on page 1 of the subject
    """
    global gamma
    return np.sqrt(gamma*P/rho)

def U_(rho : np.array, u : np.array, P : np.array):
    """ 
    Computes the array of conserved quantities as defined on page 1 of the subject
    """
    global gamma
    return np.array([rho, rho*u, 0.5*rho*u**2+P/(gamma-1)])

def W_(rho : np.array, u : np.array, P : np.array):
    """ 
    Returns an array of the primitive quantities
    """
    return np.array([rho, u, P])

def delta_t(u : np.array, a : np.array, dx : float) :
    """
    Computes the next timestep used for the calculations, using the following arguments :
    - u is an array of the velocity for each cell
    - a is an array of the sound speed for each cell 
    - dx is the distance between two cells
    """
    config = Config_Loader()
    S_max= np.max(np.absolute(u) + a)
    return (config.DATA["C"] * dx)/(S_max) # Returns the time step value to be used by Conservative_State_Solver.py

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