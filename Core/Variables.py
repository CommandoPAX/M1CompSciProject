# All main variables

import numpy as np
import json 

with open("./Config/Default_Config.json", "r") as f :
    config = json.load(f)

def P_(rho, K) :
    global gamma
    return K * np.pow(rho,gamma)

def a_ (P, rho):
    global gamma
    return np.sqrt(gamma*P/rho)

def U_(rho, u, P):
    global gamma
    return np.array([rho, rho*u, 0.5*rho*u**2+P/(gamma-1)])

def W_(rho, u, P):
    return np.array([rho, u, P])