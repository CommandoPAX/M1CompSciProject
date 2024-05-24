import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def charger (fichier):


    data = pd.read_csv(fichier,skiprows=3,index_col="n_cell",delimiter=" ")

    split = fichier.split("/")
    label = split[len(split)-1]

    flux = label.split("_")[-2]
    t = label.split("_")[-1][:-4]

    #label = flux+", t = "+str(round(float(t),3))+" s"

    P = data["P"].to_numpy()
    u = data["u"].to_numpy()
    rho = data["rho"].to_numpy()

    return rho, u , P

LF = charger("./output/Sod_Problem/Sod_Problem_LF_500cells.txt")
LW = charger("./output/Sod_Problem/Sod_Problem_LW_0.25046.txt")
Riemann = charger("./output/Sod_Problem/Sod_Problem_Riemann_0.25.txt")

X = np.linspace(0,1,len(LF[0]))

args = [r"Density ratio for 500 cells",r"Velocity ratio for 50 cells",r"Pressure ratio for 50 cells"]
unites = [r"rho [$kg/m^3$]",r"u [$m/s$]",r"P [$Pa$]"]
for i in range(3):

    axes = plt.gca()

    plt.title(args[i])

    plt.plot(X,Riemann[i]/Riemann[i],label="Riemann")
    plt.plot(X,LF[i]/Riemann[i],label = "Lax-Friedrich")
    plt.plot(X,LW[i]/Riemann[i],label = "Lax-Wendroff")

    axes.set_xlabel("X [m]")


    plt.legend()

    plt.show()

"""for i in range(3):

    plt.title(args[i][:-6])
    axes = plt.gca()
    axes.set_xlabel("X [m]")
    axes.set_ylabel(unites[i])

    plt.plot(X,Riemann[i],label="Riemann")
    plt.plot(X,LF[i],label = "Lax-Friedrich")
    plt.plot(X,LW[i],label = "Lax-Wendroff")

    plt.legend()

    plt.show()"""