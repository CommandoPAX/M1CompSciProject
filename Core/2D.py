import numpy as np
from Core.Physics import *
from Core.Plot_Handler import *
from Core.Config_Loader import Config_Loader
from Flux_Solver.Lax_Friedrich import*
from Core.Conservative_State_Solver import*
from Core.Riemann_Solver import *

n_cell = 25

rho = np.ones((n_cell,n_cell))
ux = np.zeros((n_cell,n_cell))
uy = np.zeros((n_cell,n_cell))
P = np.ones((n_cell,n_cell))

P[10,10] = 10

plt.imshow(P)