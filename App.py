from tkinter import*
from tkinter.messagebox import*
from tkinter.filedialog import*

import matplotlib
import numpy as np

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from Core.Physics import *
from Core.Plot_Handler import *
from Core.Config_Loader import Config_Loader
from Flux_Solver.Lax_Friedrich import*
from Core.Conservative_State_Solver import*

#import matplotlib.pyplot as plt


class Application (Tk):
    def __init__ (self):
        Tk.__init__(self)
        
        self.fig = Figure(figsize=(5,5), dpi=100)

        X = np.linspace(0,5)
        rho = u = P = U_int = X

        self.t = Label(self,text="t = 0",font="Arial 20",pady = 10)
        self.t.grid(row=0,column=1)

        self.frame_graphes = Frame(self, borderwidth =2,padx = 10, pady = 10)
        self.frame_graphes.grid(row = 1, column =1,rowspan=100)

        self.axes_rho = self.fig.add_subplot(221)
        self.axes_rho.set_xlabel("X [m]")
        self.axes_rho.set_ylabel("rho")
        self.plot_rho, = self.axes_rho.plot(X,rho,label="density")
        self.axes_rho.legend()

        # Velocity
        axes = self.fig.add_subplot(222)
        axes.set_xlabel("X [m]")
        axes.set_ylabel("u [m/s]")
        self.plot_u, = axes.plot(X, u, label="velocity")
        axes.legend()
        
        # Pressure
        axes = self.fig.add_subplot(223)
        axes.set_xlabel("X [m]")
        axes.set_ylabel("P")
        axes.plot(X, P, label="Pressure")
        axes.legend()
        
        # Internal Energy
        axes = self.fig.add_subplot(224)
        axes.set_xlabel("X [m]")
        axes.set_ylabel("U_int")
        axes.plot(X,U_int, label="Internal energy")
        axes.legend()

        self.canvas = FigureCanvasTkAgg(self.fig, self.frame_graphes)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        toolbar = NavigationToolbar2Tk(self.canvas, self.frame_graphes)
        toolbar.update()
        self.canvas._tkcanvas.pack()

        self.n = 0

        self.bouton = Button(self,text="Je suis un BOUTON",command=self.plot)
        self.bouton.grid(row = 10, column =2)

        self.title("L'hydrodynamiquateur génial")

        self.flux = StringVar()
        self.flux.set("LF")

        self.Frame_flux = LabelFrame(self, text="Méthode de résolution")
        self.Frame_flux.grid(row=1,column = 2,padx= 20,pady =20)

        Radiobutton(self.Frame_flux,text="Lax Friedrich",value="LF",variable=self.flux).grid(row = 1, column = 1)
        Radiobutton(self.Frame_flux,text="Lax Wendroff",value="LW",variable=self.flux).grid(row = 2, column = 1)
        Radiobutton(self.Frame_flux,text="Riemann",value="Riemann",variable=self.flux).grid(row = 3, column = 1)

        self.Frame_config = LabelFrame(self,text="Conditions initiales")
        self.Frame_config.grid(column=2,row=2)
        self.nom_CI = Label(self.Frame_config,text="sod.conf")
        self.nom_CI.grid(row=1,padx=10,pady=10)
        Button(self.Frame_config,text="Ouvrir",command=self.ouvrir_conf).grid(row=2)

    def plot(self,event=None):
        X = np.linspace(0,5)
        self.plot_rho.set_ydata(X**self.n)
        self.canvas.draw()
        self.canvas.flush_events()
        self.n+=1

    def ouvrir_conf (self, fichier = ""):
        if fichier == "" : fichier = askopenfilename (filetypes=[('Fichiers .json','.json'),('Tous les fichiers','.*')],initialdir="./Config")
        nom_fichier = fichier.split("/")
        nom_fichier = nom_fichier[len(nom_fichier)-1]
        self.nom_CI.configure(text=nom_fichier)

        self.config = Config_Loader(nom_fichier[:-5])


if __name__ == "__main__" :
    fen = Application()
    fen.ouvrir_conf("./Config/Sod_Problem.json")

    fen.mainloop()
    fen.quit()
