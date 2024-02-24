# Handles creating every plot

import matplotlib.pyplot as plt 
from Core.Physics import *
from Core.Config_Loader import Config_Loader

config = Config_Loader()
gamma = config.DATA["gamma"]

def Create_Plots(X : np.array, W : np.array, output : str = "GRAPHIQUE"):
    """ 
    Creates and saves the plots
    Only works for the initial conditions in its current form
    All plots are in function of X[m]
    """
    
    global gamma

    fig = plt.figure()

    rho = W[:,0]
    u = W[:,1]
    P = W[:,2]
    U_int =  2*(P/rho)

    # Density
    axes = fig.add_subplot(221)
    axes.set_xlabel("X [m]")
    axes.set_ylabel("rho")
    axes.plot(X, rho, label = "Density")
    axes.legend()

    # Velocity
    axes = fig.add_subplot(222)
    axes.set_xlabel("X [m]")
    axes.set_ylabel("u [m/s]")
    axes.plot(X, u, label="velocity")
    axes.legend()
    
    # Pressure
    axes = fig.add_subplot(223)
    axes.set_xlabel("X [m]")
    axes.set_ylabel("P")
    axes.plot(X, P, label="Pressure")
    axes.legend()
    
    # Internal Energy
    axes = fig.add_subplot(224)
    axes.set_xlabel("X [m]")
    axes.set_ylabel("U_int")
    axes.plot(X,U_int, label="Internal energy")
    axes.legend()
    
    # Saves and shows the plots
    plt.savefig(f"Graphes/{output}")
    plt.show()