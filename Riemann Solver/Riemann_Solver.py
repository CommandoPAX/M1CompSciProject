# Riemann solver based on the fortran program in Toro 1999

from Core.Config_Loader import Config_Loader
import numpy as np

config = Config_Loader()

# Compute Gamma related constants
G1 = (config.DATA["gamma"]-1)/(2*config.DATA["gamma"])
G2 = (config.DATA["gamma"]+1)/(2*config.DATA["gamma"])
G3 = 2*config.DATA["gamma"]/(config.DATA["gamma"]-1)
G4 = 2/(config.DATA["gamma"]-1)
G5 = 2/(config.DATA["gamma"]+1)
G6 = (config.DATA["gamma"]-1)/(config.DATA["gamma"]+1)
G7 = (config.DATA["gamma"]-1)/2
G8 = config.DATA["gamma"]-1

# Compute sound speeds 

CL = np.sqrt(config.DATA["gamma"]*config.DATA["P_inf"]/config.DATA["rho_inf"])
CR = np.sqrt(config.DATA["gamma"]*config.DATA["P_sup"]/config.DATA["rho_sup"])

def SAMPLE(PM, UM, S) : 
    global G1, G2, G3, G4, G5, G6, G7, G8, CL, CR
    
    if S <= UM :
        # Sampling point lies to the left of the contact discontinuity
        if PM <= config.DATA["P_inf"] : 
            # Left rarefaction
            SHL = config.DATA["u_inf"] - CL 
            if S <= SHL :
                D_out = config.DATA["rho_inf"]
                U_out = config.DATA["u_inf"]
                P_out = config.DATA["P_inf"]
            else : 
                CML = CL * (PM / config.DATA["P_inf"])**G1 
                STL = UM - CML
                if S >= STL : 
                    # Sampled point is star left state
                    D_out = config.DATA["rho_inf"] * (PM / config.DATA["P_inf"])**(1.0/config.DATA["gamma"])
                    U_out = UM 
                    P_out = PM 
                else : 
                    # Sampled point is inside left fan
                    U_out = G5 * (CL + G7*config.DATA["u_inf"] + S)
                    C = G5*(CL + G7*(config.DATA["u_inf"] - S))
                    D = config.DATA["rho_inf"]*(C/CL)**G4 
                    P = config.DATA["P_inf"]*(C/CL)**G3 
        else : 
            # Left shock
            PML = PM/config.DATA["P_inf"]
            SL = config.DATA["u_inf"] - CL*np.sqrt(G2*PML + G1)
            if S <= SL : 
                # Sampled point is left data state
                D_out = config.DATA["rho_inf"]
                U_out = config.DATA["u_inf"]
                P = config.DATA["P_inf"]
            else : 
                # Sampled point is star left state
                D_out = config.DATA["rho_inf"]*(PML + G6)/(PML*G6 + 1.0)
                U_out = UM 
                P_out = PM 
    else : 
        # Sampling point lies to the right of the contact discontinuity
        if PM >= config.DATA["P_sup"] : 
            # Right shock 
            PMR = PM/config.DATA["P_sup"]
            SR = config.DATA["u_sup"] + CR * np.sqrt(G2*PMR + G1)
            if S >= SR : 
                #Sampled point is right data state 
                D_out = config.DATA["rho_sup"]
                U_out = config.DATA["u_sup"]
                P_out = config.DATA["P_sup"]
            else : 
                # Sampled point is star right state
                D_out = config.DATA["rho_sup"]*(PMR + G6)/(PMR*G6 + 1.0)
                U_out = UM 
                P_out = PM 
        else :
            # Right rarefaction 
            SHR = config.DATA["u_sup"] + CR 
            if S >= SHR : 
                # Sampled point is right data state 
                D_out = config.DATA["rho_sup"]
                U_out = config.DATA["u_sup"]
                P_out = config.DATA["P_sup"]
            else : 
                CMR = CR*(PM/config.DATA["P_sup"])**G1 
                STR = UM + CMR 
                if S <= STR : 
                    # Sampled point is star right state 
                    D_out = config.DATA["rho_sup"]*(PM/config.DATA["P_sup"])**(1.0/config.DATA["gamma"])
                    U_out = UM 
                    P_out = PM 
                else : 
                    #Sampled point is inside left fan 
                    U_out = G5 * (-CR + G7*config.DATA["u_sup"] + S) 
                    C = G5 * (CR - G7 * (config.DATA["u_sup"] -S))
                    D_out = config.DATA["rho_sup"] * (C/CR)**G4 
                    P_out = config.DATA["P_sup"] * (C/CR)**G3 
                    
    return D_out, U_out, P_out 

def PREFUN(F, FD, P, DK, PK, CK) : 
    global G1, G2, G3, G4, G5, G6, G7, G8, CL, CR 
    
    if P <= PK : 
        # Rarefaction wave 
        PRAT = P/PK 
        F = G4*CK*(PRAT**G1 - 1.0)
        FD (1.0/(DK*CK))*PRAT**(-G2) 
    else :
        # Shock wave 
        AK = G5/DK 
        BK = G6*PK 
        QRT = np.sqrt(AK/(BK + P))
        F = (P - PK) * QRT 
        FD (1 - 0.5 * (P - PK)/(BK + P))*QRT 
    return F, FD, P, DK, PK, CK

def GUESSP(PM) : 
    # W.I.P. page 171
    pass
        
def STARPU(P, U, MPA) : 
    dx = config.DATA["L"]/config.DATA["n_cell"]
    #Pold = GUESSP(PSTART)
    UDIFF = config.DATA["u_sup"] - config.DATA["u_inf"]
    
if __name__ == "__main__" :

    # We test for the intial pressure conditions 

    if (G4 *(CL+CR)) <= (config.DATA["u_sup"] - config.DATA["u_inf"]) :
        print("Vacuum is generated by data")