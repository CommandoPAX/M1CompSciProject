# Law-Wendroff

import numpy as np
from Core.Config_Loader import Config_Loader
from Core.Error_Handler import LogError
from Core.Conservative_State_Solver import*

config = Config_Loader()

def F12_Friedrich (U, dx, dt):
    
    n_cell = config.DATA["n_cell"]
    
    R1=np.zeros((3,n_cell))
    R2=np.zeros((3,n_cell))
    R=np.zeros((3,n_cell))
    
    
    for i in range(n_cell-1):
        if i==0:
            R1[:,i]=0.5*(U[:,i]+U[:,i+1]) - 0.5*(dt/dx)*(F_(U[:,i+1])-F_(U[:,i])) #R1[:,i]=U[:,i+1/2] at t'=t+1/2*dt
            R2[:,i]=0.5*(U[:,i]+U[:,i]) - 0.5*(dt/dx)*(F_(U[:,i])-F_(U[:,i])) #R2[:,i]=U[:,i-1/2] at t'=t+1/2*dt
        elif i==n_cell-1:
            R1[:,i]=0.5*(U[:,i]+U[:,i]) - 0.5*(dt/dx)*(F_(U[:,i])-F_(U[:,i])) #R1[:,i]=U[:,i+1/2] at t'=t+1/2*dt
            R2[:,i]=0.5*(U[:,i]+U[:,i-1]) - 0.5*(dt/dx)*(F_(U[:,i])-F_(U[:,i-1])) #R2[:,i]=U[:,i-1/2] at t'=t+1/2*dt
        else:    
            R1[:,i]=0.5*(U[:,i]+U[:,i+1]) - 0.5*(dt/dx)*(F_(U[:,i+1])-F_(U[:,i])) #R1[:,i]=U[:,i+1/2] at t'=t+1/2*dt
            R2[:,i]=0.5*(U[:,i]+U[:,i-1]) - 0.5*(dt/dx)*(F_(U[:,i])-F_(U[:,i-1])) #R2[:,i]=U[:,i-1/2] at t'=t+1/2*dt
        R[:,i]=U[:,i]-(dt/dx)*(F_(R1[:,i]-F_(R2[:,i]))) #R[:,i]=U[:,i] at t'=t+dt
        
    return R
        