# All main variables

import numpy as np
from Core.Config_Loader import Config_Loader

config = Config_Loader()
gamma= config.DATA["gamma"]

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