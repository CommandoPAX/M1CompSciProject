# Handles creating every plot

import matplotlib.pyplot as plt 

def Create_Plots(X, W, output = "GRAPHIQUE"):

    fig = plt.figure()

    axes = fig.add_subplot(221)
    axes.set_xlabel("X [m]")
    axes.set_ylabel("rho")

    axes.plot(X, W[0], label = "Density")
    axes.legend()

    axes = fig.add_subplot(222)
    axes.set_xlabel("X [m]")
    axes.set_ylabel("u [m/s]")

    axes.plot(X, W[1], label="velocity")
    axes.legend()


    axes = fig.add_subplot(223)
    axes.set_xlabel("X [m]")
    axes.set_ylabel("P")

    axes.plot(X, W[2], label="Pressure")
    axes.legend()

    axes = fig.add_subplot(224)
    axes.set_xlabel("X [m]")
    axes.set_ylabel("U2")

    U = U(W[0],W[1],W[2])

    axes.plot(X,U[2], label="Internal energy")
    axes.legend()
    plt.savefig("Graphes/"+output)

    plt.show()