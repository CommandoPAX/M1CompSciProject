# Riemann solver based on the fortran program in Toro 1999

from Core.Config_Loader import Config_Loader
import numpy as np

class Riemann_Solver() : 
    def __init__(self, c_name) : 
        config = Config_Loader()

        # Compute Gamma related constants
        self.G1 = (config.DATA["gamma"]-1)/(2*config.DATA["gamma"])
        self.G2 = (config.DATA["gamma"]+1)/(2*config.DATA["gamma"])
        self.G3 = 2*config.DATA["gamma"]/(config.DATA["gamma"]-1)
        self.G4 = 2/(config.DATA["gamma"]-1)
        self.G5 = 2/(config.DATA["gamma"]+1)
        self.G6 = (config.DATA["gamma"]-1)/(config.DATA["gamma"]+1)
        self.G7 = (config.DATA["gamma"]-1)/2
        self.G8 = config.DATA["gamma"]-1

        # Compute sound speeds 
        self.CL = np.sqrt(config.DATA["gamma"]*config.DATA["P_inf"]/config.DATA["rho_inf"])
        self.CR = np.sqrt(config.DATA["gamma"]*config.DATA["P_sup"]/config.DATA["rho_sup"])
        
        # Useful values 
        self.DL = config.DATA["rho_inf"]
        self.DR = config.DATA["rho_sup"]
        self.PL = config.DATA["P_inf"]
        self.PR = config.DATA["P_sup"]
        self.UL = config.DATA["u_inf"]
        self.UR = config.DATA["u_sup"]
        self.G = config.DATA["gamma"]
        self.n = config.DATA["n_cell"]
        self.L = config.DATA["L"]

                
    def SAMPLE(self, PM, UM, S) : 
        
        if S <= UM :
            # Sampling point lies to the left of the contact discontinuity
            if PM <= self.PL : 
                # Left rarefaction
                SHL = self.UL - self.CL 
                if S <= SHL :
                    D_out = self.DL
                    U_out = self.UL
                    P_out = self.PL
                else : 
                    CML = self.CL * (PM / self.PL)**self.G1 
                    STL = UM - CML
                    if S >= STL : 
                        # Sampled point is star left state
                        D_out = self.DL * (PM / self.PL)**(1.0/self.G)
                        U_out = UM 
                        P_out = PM 
                    else : 
                        # Sampled point is inside left fan
                        U_out = self.G5 * (self.CL + self.G7*self.UL + S)
                        C = self.G5*(self.CL + self.G7*(self.UL - S))
                        D_out = self.DL*(C/self.CL)**self.G4 
                        P_out = self.PL*(C/self.CL)**self.G3 
            else : 
                # Left shock
                PML = PM/self.PL
                SL = self.UL - self.CL*np.sqrt(self.G2*PML + self.G1)
                if S <= SL : 
                    # Sampled point is left data state
                    D_out = self.DL
                    U_out = self.UL
                    P_out = self.PL
                else : 
                    # Sampled point is star left state
                    D_out = self.DL*(PML + self.G6)/(PML*self.G6 + 1.0)
                    U_out = UM 
                    P_out = PM 
        else : 
            # Sampling point lies to the right of the contact discontinuity
            if PM >= self.PR : 
                # Right shock 
                PMR = PM/self.PR
                SR = self.UR + self.CR * np.sqrt(self.G2*PMR + self.G1)
                if S >= SR : 
                    #Sampled point is right data state 
                    D_out = self.DR
                    U_out = self.UR
                    P_out = self.PR
                else : 
                    # Sampled point is star right state
                    D_out = self.DR*(PMR + self.G6)/(PMR*self.G6 + 1.0)
                    U_out = UM 
                    P_out = PM 
            else :
                # Right rarefaction 
                SHR = self.UR + self.CR 
                if S >= SHR : 
                    # Sampled point is right data state 
                    D_out = self.DR
                    U_out = self.UR
                    P_out = self.PR
                else : 
                    CMR = self.CR*(PM/self.PR)**self.G1 
                    STR = UM + CMR 
                    if S <= STR : 
                        # Sampled point is star right state 
                        D_out = self.DR*(PM/self.PR)**(1.0/self.G)
                        U_out = UM 
                        P_out = PM 
                    else : 
                        #Sampled point is inside left fan 
                        U_out = self.G5 * (-self.CR + self.G7*self.UR + S) 
                        C = self.G5 * (self.CR - self.G7 * (self.UR -S))
                        D_out = self.DR * (C/self.CR)**self.G4 
                        P_out = self.PR * (C/self.CR)**self.G3 
                        
        return D_out, U_out, P_out 


    def PREFUN(self, P, DK, PK, CK) : 
        
        if P <= PK : 
            # Rarefaction wave 
            PRAT = P/PK 
            F = self.G4*CK*(PRAT**self.G1 - 1.0)
            FD = (1.0/(DK*CK))*PRAT**(-self.G2) 
        else :
            # Shock wave 
            AK = self.G5/DK 
            BK = self.G6*PK 
            QRT = np.sqrt(AK/(BK + P))
            F = (P - PK) * QRT 
            FD = (1 - 0.5 * (P - PK)/(BK + P))*QRT 
        return F, FD, P, DK, PK, CK


    def GUESSP(self) : 
        QUSER = 2.0
        
        #Compute guess pressure from PVRS Riemann solver
        
        CUP = 0.25*(self.DL + self.DR) * (self.CL + self.CR)
        PPV = 0.5*(self.PL + self.PR) + 0.5 * (self.UL - self.UR)*CUP 
        PPV = max(0.0, PPV)
        PMIN = min(self.PL, self.PR)
        PMAX = max(self.PL, self.PR)
        QMAX = PMAX/PMIN 
        
        if QMAX <= QUSER and PMIN <= PPV and PPV <= PMAX : 
            # Select PVRS Riemann solver 
            PM = PPV 
        
        else : 
            if PPV < PMIN : 
                # Select Two-Rarefaction Riemann solver 
                PQ = (self.PL/self.PR)**self.G1 
                UM = (PQ*self.UL/self.CL + self.UR/self.CR + self.G4 * (PQ - 1.0))/(PQ/self.CL + 1.0/self.CR)
                PTL = 1.0 + self.G7 * (self.UL - UM)/self.CL 
                PTR = 1.0 + self.G7 * (UM - self.UR)/self.CR 
                PM = 0.5*(self.PL*PTL**self.G3 + self.PR*PTR**self.G3)
                
            else :  
                # Select Two-Shock Riemann solver with PVRS as estimate 
                GEL = np.sqrt((self.G5/self.DL)/(self.G6*self.PL + PPV))
                GER = np.sqrt((self.G5/self.DR)/(self.G6*self.PR + PPV))
                PM = (GEL*self.PL + GER*self.PR - (self.UR - self.UL) / (GEL+GER))
        return PM 
            
            
    def STARPU(self, P, U) : 
        # Values returned are wrong, never U's value
        NRITER = 20 # Not really sure but it's my best guess
        TOLPRE = 1.0E-6
        
        PSTART = self.GUESSP()
        POLD = PSTART
        UDIFF = self.UR - self.UL
        
        for i in range(1, NRITER) : 
            FL, FLD, POLD, self.DL, self.PL, self.CL = self.PREFUN(POLD, self.DL, self.PL, self.CL) # I have added self. on these lines
            FR, FRD, POLD, self.DR, self.PR, self.CR = self.PREFUN(POLD, self.DR, self.PR, self.CR) # But it might be a mistake
            P = POLD - ((FL + FR + UDIFF)/(FLD + FRD))

            CHANGE = 2.0 * abs((P-POLD)/(P+POLD))
            if CHANGE <= TOLPRE : 
                # Compute velocity in Star Region
                break
            if P < 0.0 : 
                P = TOLPRE 
            POLD = P
        
        U = 0.5*(self.UL + self.UR + FR - FL)

        return P, U #Will only return a non-0 value for U if CHANGE <= TOLPRE was validated once, currently it does not

    def Evol(self, t) :
        # We test for the intial pressure conditions 

        TIMEOUT = t #seconds (maybe)
        DIAPH = 0.5 #Discontinuity position, considered at 0.5*L, unsure if this value is correct
        
        U = np.zeros((self.n,3))
        
        if (self.G4 *(self.CL+self.CR)) <= (self.UR - self.UL) :
            print("Vacuum is generated by data")
        else : 
            # Exact solution for presure and velocity in star region is found 
            PM = 0 
            UM = 0
            PM, UM = self.STARPU(PM, UM)
            dx = self.L/self.n
            
            # Complete solution at time TIMEOUT is found
            for i in range(1, self.n) : 
                XPOS = (float(i) - 0.5)*dx 
                S = (XPOS - DIAPH)/TIMEOUT 
                
                # Solution at point (X,T) = (XPOS - DIAPH, TIMEOUT) is found
                U[i, 0], U[i, 1], U[i, 2] = self.SAMPLE(PM, UM, S)
                
            return U
