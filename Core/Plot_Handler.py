# Handles creating every plot

import matplotlib.pyplot as plt 
from Core.Physics import *

def Create_Plots(X : np.array, W : np.array, output : str = "GRAPHIQUE"):
    """ 
    Creates and saves the plots
    Only works for the initial conditions in its current form
    All plots are in function of X[m]
    """
    
    fig = plt.figure()

    # Density
    try :
        axes = fig.add_subplot(221)
        axes.set_xlabel("X [m]")
        axes.set_ylabel("rho")
        axes.plot(X, W[0], label = "Density")
        axes.legend()
    except Exception as e :
            LogError("Create_Plots - Density", e)
            print(e)
            pass

    # Velocity
    try :
        axes = fig.add_subplot(222)
        axes.set_xlabel("X [m]")
        axes.set_ylabel("u [m/s]")
        axes.plot(X, W[1], label="velocity")
        axes.legend()
    except Exception as e :
            LogError("Create_Plots - Velocity", e)
            print(e)
            pass

    # Pressure
    try :
        axes = fig.add_subplot(223)
        axes.set_xlabel("X [m]")
        axes.set_ylabel("P")
        axes.plot(X, W[2], label="Pressure")
        axes.legend()
    except Exception as e :
            LogError("Create_Plots - Pressure", e)
            print(e)
            pass

    # Internal Energy
    try :
        axes = fig.add_subplot(224)
        axes.set_xlabel("X [m]")
        axes.set_ylabel("U2")
        U = U_(W[0],W[1],W[2])
        axes.plot(X,U[2], label="Internal energy")
        axes.legend()
    except Exception as e :
            LogError("Create_Plots - Internal Energy", e)
            print(e)
            pass
    
    # Saves and shows the plots
    plt.savefig(f"Graphes/{output}")
    plt.show()