# Main file to execute rest of the code

import numpy as np
import matplotlib.pyplot as plt
import os
from tkinter import*
from math import*
import sys

gamma = 1.4
L = 1 #longueur du tube en mètres
n_cell = 10000

def derivee (f, x):
    global n_cell

    y = f(x)
    dx = x[1]-x[0]
    yp = np.zeros(n_cell)
    for i in range(len(x)):
        if i >=1 and i+1 < len(x) : yp [i] = (y[i-1]+y[i+1])/(2*dx)

        # Transmissive boundary condition

        if i == 0 : yp[i] : yp [i] = (y[0]+y[1])/(2*dx)
        if i+1 == len(x) : yp [i] = (y[i-1]+y[i])/(2*dx)

    return yp

def P_(rho, K) :
    global gamma
    return K * np.pow(rho,gamma)

def a_ (P, rho):
    global gamma
    return np.sqrt(gamma*P/rho)

def U_(rho, u, P):
    global gamma
    return np.array([rho, rho*u, 0.5*rho*u**2+P/(gamma-1)])

def F_(U):
    global gamma
    return np.array([U[0], 0.5*(3-gamma)*U[1]**2/U[0]+(gamma-1)*U[2], U[1]/U[0]*U[2]-0.5*(gamma-1)*U[1]**3/U[0]**2])

def W_(rho, u, P):
    return np.array([rho, u, P])

def graphes (X, W, output = "GRAPHIQUE"):

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

    U = U_(W[0],W[1],W[2])

    axes.plot(X,U[2], label="Internal energy")
    axes.legend()
    plt.savefig("Graphes/"+output)

    plt.show()

if __name__ == "__main__" :

    # Conditions initiales

    X = np.linspace(0,1,num=n_cell)

    rho = np.ones(n_cell)
    u=np.zeros(n_cell)
    P = np.ones(n_cell)

    rho[n_cell//2:] = 0.125
    P[n_cell//2:] = 0.1

    W = W_ (rho, u, P)    

    graphes(X,W)
