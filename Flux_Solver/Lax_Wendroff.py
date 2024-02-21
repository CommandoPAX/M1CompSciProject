# Law-Wendroff

import numpy as np
from Core.Config_Loader import Config_Loader
from Core.Error_Handler import LogError
from Core.Conservative_State_Solver import*

config = Config_Loader()

def F12_Friedrich (U, dx, dt):
    
    n_cell = config.DATA["n_cell"]
    c=0.9
    R=np.zeros((3,n_cell))
    
    for i in range(n_cell):
        R[:,i]=0.5*(U[:,i]+U[:,i+1]) + 0.5*(dt/dx)*(F_[:,i]-F_[:,i+1]) #R[:,i]=U[:,i+1/2] at t'=t+1/2*dt
        