from math import*
import numpy as np

class Riemann ():
    def __init__ (self, n_cell, l, disc, gamma, timeout, rho_inf, rho_sup, P_inf,P_sup, v_inf, v_sup):
        self.n_cell == n_cell
        self.l = l
        self.disc = disc
        self.gamma = gamma
        self.timeout = timeout
        self.rho_inf = rho_inf
        self.rho_sup = rho_sup
        self.P_inf = P_inf
        self.P_sup = P_sup

        self.G1 = (gamma-1)/(2*gamma)
        self.G2 = (gamma+1)/(2*gamma)
        self.G3 = 2*gamma/(gamma-1)
        self.G4 = 2/(gamma-1)
        self.G5 = 2/(gamma+1)
        self.G6 = (gamma-1)/(gamma+1)
        self.G7 = (gamma-1)/2
        self.G8 = gamma-1

        self.CL = sqrt(self.gamma*self.P_inf/self.rho_inf)
        self.CR = sqrt(self.gamma*self.P_sup/self.rho_sup)

        if self.G4*(self.CL+self.CR) <= self.v_sup-self.v_inf :
            return "Vacuum generated by data"

    def Starpu (self, P, U, MPA):
        pass

    def Guessp (self):
        self.QUSER = 2

        self.CUP = 0.25*(self.DL+self.DR)*(self.CL+self.CR)
        self.PPV = max(0, 0.5*(self.PL+self.PR)+0.5*(self.UL-self.UR)*self.CUP)
        self.PMIN = min(self.P_inf, self.P_sup)
        self.PMAX = max(self.P_inf, self.P_sup)
        self.QMAX = self.PMAX / self.PMIN

        if self.QMAX <= self.QUSER and self.PMIN <= self.PPV and self.PPV <= self.PMAX :
            self.PM = self.PPV
        else :
            if self.PPV < self.PMIN :
                self.PQ = (self.PL/self.PR)**self.G1
                self.UM = (self.PQ*self.UL/self.CL + self.UR/self.CR + self.G4*(slf.PQ-1))/(self.PQ/self.CL+1./self.CR)
                self.PTL = 1+self.G7*(self.UL - self.UM)
