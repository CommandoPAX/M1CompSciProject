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
from Riemann_Solver.Riemann_Solver import*
from Flux_Solver.Lax_Friedrich import*
from Core.Conservative_State_Solver import*

#import matplotlib.pyplot as plt


class Application (Tk):
    def __init__ (self):
        Tk.__init__(self)
        
        self.fig = Figure(figsize=(5,5), dpi=100)

        X = np.linspace(0,1)

        self.t = Label(self,text="t = 0",font="Arial 20",pady = 10)
        self.t.grid(row=0,column=1)

        self.frame_graphes = Frame(self, borderwidth =2,padx = 10, pady = 10)
        self.frame_graphes.grid(row = 1, column =1,rowspan=100)

        self.axes_rho = self.fig.add_subplot(221)
        self.axes_rho.set_xlabel("X [m]")
        self.axes_rho.set_ylabel("rho")
        self.plot_rho, = self.axes_rho.plot([0,0],label="density")
        self.axes_rho.legend()

        # Velocity
        self.axes_u = self.fig.add_subplot(222)
        self.axes_u.set_xlabel("X [m]")
        self.axes_u.set_ylabel("u [m/s]")
        self.plot_u, = self.axes_u.plot([0,0],label="velocity")
        self.axes_u.legend()
        
        # Pressure
        self.axes_P = self.fig.add_subplot(223)
        self.axes_P.set_xlabel("X [m]")
        self.axes_P.set_ylabel("P")
        self.plot_P, = self.axes_P.plot([0,0],label="Pression")
        self.axes_P.legend()
        
        # Internal Energy
        self.axes_U = self.fig.add_subplot(224)
        self.axes_U.set_xlabel("X [m]")
        self.axes_U.set_ylabel("U_int")
        self.plot_U, = self.axes_U.plot([0,0],label="Energie interne")
        self.axes_U.legend()

        self.canvas = FigureCanvasTkAgg(self.fig, self.frame_graphes)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        toolbar = NavigationToolbar2Tk(self.canvas, self.frame_graphes)
        toolbar.update()
        self.canvas._tkcanvas.pack()

        self.n = 0

        Button(self,text="Lancer la simulation",command=self.lancer).grid(row = 10, column =2)
        Button(self,text="Stop",command=self.Stop).grid(row = 11, column =2)
        Button(self,text="T = 0",command=self.T0).grid(row = 12, column =2)

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

        self.Frame_animation = LabelFrame(self,text="Animation")
        self.Frame_animation.grid(row =3,column=2,pady=20,padx=10)

        self.graphes = BooleanVar() # Ne fonctionne pas pour l'instant

        Checkbutton(self.Frame_animation, text="Afficher les graphiques",onvalue=True,offvalue=False,variable=self.graphes,command=self.Afficher_graphes).grid(row=1,column=0,pady=5,padx=5,columnspan=2)
        self.graphes.set(True)

        Label(self.Frame_animation,text = "Plot toutes les ").grid(row=2,column = 0,padx =0 )
        self.step = Spinbox(self.Frame_animation,from_=1,to=1e10,width=6)
        self.step.grid(row=2,column=1)
        Label(self.Frame_animation,text = "itérations").grid(row=2,column = 2,padx =0,pady=10 )


    def plot(self):

        self.U_int = 2*self.P/self.rho

        self.plot_rho.set_data(self.X,self.rho)
        self.plot_u.set_data(self.X,self.u)
        self.plot_P.set_data(self.X,self.P)
        self.plot_U.set_data(self.X,self.U_int)


        if self.rho.any !=0 :
            dy = np.max(self.rho)-np.min(self.rho)
            self.axes_rho.set_ylim(np.min(self.rho)-dy/10,np.max(self.rho)+dy/10)


        if self.u.any() != 0 :
            dy = np.max(self.u)-np.min(self.u)
            self.axes_u.set_ylim(np.min(self.u)-dy/10,np.max(self.u)+dy/10)

        dy = np.max(self.P)-np.min(self.P)

        self.axes_P.set_ylim(np.min(self.P)-dy/10,np.max(self.P)+dy/10)

        dy = np.max(self.U_int)- np.min(self.U_int)
        try :
            self.axes_U.set_ylim(np.min(self.U_int)-dy/10,np.max(self.U_int)+dy/10)
        except :
            pass

        #self.plot_U.set_data(X,self.U_int)

    def lancer(self):
        self.stop = False
        self.Simulation()

    def Simulation(self):
        flux =self.flux.get()
        self.n +=1 
        
        dx = self.X[1]-self.X[0]
        
        if flux != "Riemann" :
            self.T += delta_t(self.U[:, 1], a_(self.U[:, 2], self.U[:, 0]),dx)
            self.U = U_next(self.U,dx,flux)
            Res = U_a_la_moins_un(self.U)
        else :
            self.T += 0.001
            Res = Riemann(self.T)

        if self.graphes.get() :
            if self.n % int(self.step.get()) == 0 :  # Ne plot pas à chaque étape pour accélérer les calculs

                self.rho = Res[:,0]
                self.u = Res[:,1]
                self.P = Res[:,2]

                self.plot()
                self.canvas.draw()
                self.t.configure(text="t = "+str(self.T)+" s")


            if self.T < 0.25 and not self.stop :
                self.after(1,self.Simulation)
            else :
                self.canvas.draw()
                self.t.configure(text="t = "+str(self.T)+" s")  
        else :     
            if self.T < 0.25 and not self.stop :
                self.Simulation()
            else :
                showinfo("Fin","Fin")
                
                self.rho = Res[:,0]
                self.u = Res[:,1]
                self.P = Res[:,2]

                self.plot()
                self.canvas.draw()
                self.t.configure(text="t = "+str(self.T)+" s")

     

    def Afficher_graphes(self):
        self.axes_rho.set_visible(self.graphes.get())
        self.axes_u.set_visible(self.graphes.get())
        self.axes_P.set_visible(self.graphes.get())
        self.axes_U.set_visible(self.graphes.get())

        self.canvas.draw()

    def Stop(self):
        self.stop = True

    def T0(self):
        self.ouvrir_conf(self.nom_fichier)

    def ouvrir_conf (self, fichier = ""):
        if fichier == "" : fichier = askopenfilename (filetypes=[('Fichiers .json','.json'),('Tous les fichiers','.*')],initialdir="./Config")
        nom_fichier = fichier.split("/")
        self.nom_fichier = nom_fichier[len(nom_fichier)-1]
        self.T = 0
        self.t.configure(text="t = 0")
        self.nom_CI.configure(text=self.nom_fichier)

        self.config = Config_Loader(self.nom_fichier[:-5])

        self.n_cell = self.config.DATA["n_cell"]

        self.rho = np.zeros(self.n_cell)
        self.u = np.zeros(self.n_cell)
        self.P = np.zeros(self.n_cell)

        self.rho[:self.n_cell//2] = self.config.DATA["rho_inf"]
        self.u[:self.n_cell//2] = self.config.DATA["u_inf"]
        self.P[:self.n_cell//2] = self.config.DATA["P_inf"]
            
        self.rho[self.n_cell//2:] = self.config.DATA["rho_sup"]
        self.u[self.n_cell//2:] = self.config.DATA["u_sup"]
        self.P[self.n_cell//2:] = self.config.DATA["P_sup"]    

        self.n = 0    

        self.X = np.linspace(0,1,num=self.n_cell)
        self.U = U_(self.rho,self.u,self.P)

        self.plot()
        self.canvas.draw()

if __name__ == "__main__" :
    fen = Application()
    fen.ouvrir_conf("./Config/Sod_Problem.json")

    fen.mainloop()
    fen.quit()
