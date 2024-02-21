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

def P(rho, K) :
    global gamma
    return K * np.pow(rho,gamma)

def a (P, rho):
    global gamma
    return np.sqrt(gamma*P/rho)

def U(rho, u, P):
    global gamma
    return np.array([rho, rho*u, 0.5*rho*u**2+P/(gamma-1)])

def F(U_):
    global gamma
    return np.array([U_[0], 0.5*(3-gamma)*U_[1]**2/U[0]+(gamma-1)*U_[2], U_[1]/U_[0]*U_[2]-0.5*(gamma-1)*U_[1]**3/U_[0]**2])

if __name__ == "__main__" :

    # Conditions initiales

    X = np.linspace(0,1,num=n_cell)

    rho = np.ones(n_cell)
    u=np.zeros(n_cell)
    P = np.ones(n_cell)

    rho[n_cell//2:] = 0.125
    P[n_cell//2:] = 0.1

