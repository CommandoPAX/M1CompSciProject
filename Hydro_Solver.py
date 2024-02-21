# Main file to execute rest of the code

import numpy as np
import matplotlib.pyplot as plt
import os
from tkinter import*
from math import*
import sys
import json

from Core.Variables import *
from Core.Plot_Handler import *

with open("./Config/Default_Config.json", "r") as f :
    config = json.load(f)

if __name__ == "__main__" :

    # Conditions initiales

    #Théo : faudra l'implémenter avec une config modifiable, je m'en occuperai c'est pas très compliqué

    X = np.linspace(0,1,num=config["n_cell"])

    rho = np.ones(config["n_cell"])
    u=np.zeros(config["n_cell"])
    P = np.ones(config["n_cell"])
    rho[config["n_cell"]//2:] = 0.125
    P[config["n_cell"]//2:] = 0.1

    W = W_(rho, u, P)    

    Create_Plots(X,W)
