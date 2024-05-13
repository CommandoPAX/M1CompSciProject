import numpy as np
from Core.Physics import *
from Core.Plot_Handler import *
from Core.Config_Loader import Config_Loader
from Flux_Solver.Lax_Friedrich import*
from Core.Conservative_State_Solver import*
from Core.Riemann_Solver import *



n_cell = 50
dx = 1/n_cell

rho = np.ones((n_cell,n_cell))
ux = np.zeros((n_cell,n_cell))
uy = np.zeros((n_cell,n_cell))
P = np.ones((n_cell,n_cell))

P[10:30,10:30] = 10

T = 0

for j in range(100):
    if j%10 == 0 :
        plt.imshow(P,vmin=1,vmax=10,cmap="hot")
        plt.title("P [Pa], t = "+str(j))
        plt.colorbar()
        plt.savefig(str(j)+".png")
        plt.clf()
    for i in range(n_cell):
        rho_i = rho[:,i]
        u_i = ux[:,i]
        P_i = P[:,i]

        U_i = U_(rho_i,u_i,P_i)

        U_i = U_next(U_i,dx,"LF")

        Res = U_a_la_moins_un(U_i)
        rho[:,i] = Res[:,0]
        ux[:,i] = Res[:,1]
        P[:,i] = Res[:,2]

        rho_i = rho[i,:]
        u_i = uy[i,:]
        P_i = P[i,:]

        U_i = U_(rho_i,u_i,P_i)

        U_i = U_next(U_i,dx,"LF")

        Res = U_a_la_moins_un(U_i)
        rho[i,:] = Res[:,0]
        ux[i,:] = Res[:,1]
        P[i,:] = Res[:,2]
            

