# Handles fixing the time step for each generation

import numpy as np
from Core.Config_Loader import *
from Core.Variables import *


def delta_t(u : np.array, a : np.array, dx : float) :
    # u is an array of the velocity for each cell
    # a is an array of the sound speed for each cell 
    # dx is the distance between two cells
    
    config = Config_Loader()
    S_max= np.max(np.absolute(u) + a)
    return (config.DATA["C"] * dx)/(S_max)