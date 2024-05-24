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
from Core.Riemann_Solver import*
from Flux_Solver.Lax_Friedrich import*
from Core.Conservative_State_Solver import*
import os
import pandas as pd

font = {'size'   : 16}

matplotlib.rc('font', **font)

class Application (Tk):
    def __init__ (self):
        Tk.__init__(self)
        
        self.fig = Figure(figsize=(12,8), dpi=100)

        X = np.linspace(0,1)

        self.t = Label(self,text="t = 0",font="Arial 20",pady = 10)
        self.t.grid(row=0,column=1)

        self.frame_graphes = Frame(self, borderwidth =2,padx = 10, pady = 20)
        self.frame_graphes.grid(row = 1, column =1,rowspan=100)

        self.axes_rho = self.fig.add_subplot(221)
        self.axes_rho.set_xlabel("X [m]")
        self.axes_rho.set_ylabel(r"rho [kg/$m^3$]")
        self.plot_rho, = self.axes_rho.plot([0,0],label="Density")
        self.axes_rho.legend()

        # Velocity
        self.axes_u = self.fig.add_subplot(222)
        self.axes_u.set_xlabel("X [m]")
        self.axes_u.set_ylabel("u [m/s]")
        self.plot_u, = self.axes_u.plot([0,0],label="Velocity")
        self.axes_u.legend()
        
        # Pressure
        self.axes_P = self.fig.add_subplot(223)
        self.axes_P.set_xlabel("X [m]")
        self.axes_P.set_ylabel("P [Pa]")
        self.plot_P, = self.axes_P.plot([0,0],label="Pressure")
        self.axes_P.legend()
        
        # Internal Energy
        self.axes_U = self.fig.add_subplot(224)
        self.axes_U.set_xlabel("X [m]")
        self.axes_U.set_ylabel("U_int [J]")
        self.plot_U, = self.axes_U.plot([0,0],label="Internal energy")
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
        #Radiobutton(self.Frame_flux,text="Godunov",value="Godunov",variable=self.flux).grid(row = 4, column = 1)    #Ne fonctionne pas pour l'instant

        self.Frame_config = LabelFrame(self,text="Conditions initiales")
        self.Frame_config.grid(column=2,row=2)
        self.nom_CI = Label(self.Frame_config,text="sod.conf")
        self.nom_CI.grid(row=1,padx=10,pady=10)
        Button(self.Frame_config,text="Ouvrir",command=self.ouvrir_conf).grid(row=2)

        self.Frame_animation = LabelFrame(self,text="Animation")
        self.Frame_animation.grid(row =3,column=2,pady=10,padx=10)

        self.graphes = BooleanVar() 

        #Checkbutton(self.Frame_animation, text="Afficher les graphiques",onvalue=True,offvalue=False,variable=self.graphes,command=self.Afficher_graphes).grid(row=1,column=0,pady=5,padx=5,columnspan=2)
        self.graphes.set(True)

        Label(self.Frame_animation,text = "Plot toutes les ").grid(row=2,column = 0,padx =0 )
        self.step = Spinbox(self.Frame_animation,from_=1,to=1e10,width=6)
        self.step.insert(END,"0")
        self.step.grid(row=2,column=1)
        Label(self.Frame_animation,text = "itérations").grid(row=2,column = 2,padx =0 )
        Label(self.Frame_animation,text="S'arrêter à t = ").grid(row=3,column=0,pady=10)
        self.t_stop = Entry(self.Frame_animation,width=7)
        self.t_stop.grid(row=3,column=1)
        Label(self.Frame_animation,text="s").grid(row=3,column=2)

        self.t_stop.insert(END, "0.25")


        self.Frame_output = LabelFrame(self,text="Output")

        Label(self.Frame_output, text="Nombre de fichiers de sorties : ").grid(row=0,column=0,padx =10,pady=10)
        self.N_sorties = Spinbox(self.Frame_output, from_= 1, to= 1e10,width = 7)
        self.N_sorties.grid(row=0,column=1,padx =10)

        self.Frame_output.grid(row =4,column=2,pady=10,padx=10)


        self.menubar = Menu(self)

        menu1 = Menu(self.menubar, tearoff=0)
        menu1.add_command(label="Ouvrir une simulation", command=self.Plotter)
        #menu1.add_command(label="Genere un fichier de config", command=self.generer_config)

        menu1.add_command(label="Explosions", command=self.explosions)


        menu1.add_separator()
        menu1.add_command(label="Quitter", command=self.destroy)
        self.menubar.add_cascade(label="Options", menu=menu1)

        menu2 = Menu(self.menubar, tearoff=0)
        menu2.add_command(label="Aide",command = self.aide)
        self.menubar.add_cascade(label="Aide", menu=menu2)

        self.config(menu=self.menubar)

    def aide(self):
        os.system("gedit README.md")

    def explosions(self):
        self.fen = Toplevel(self)
        
        self.fig_exp = Figure(figsize=(8,8), dpi=100)

        X = np.linspace(0,1)

        self.frame_graphes_exp = Frame(self.fen, borderwidth =2,padx = 10, pady = 20)
        self.frame_graphes_exp.grid(row = 1,rowspan = 3, column =1)

        self.axes_P_exp = self.fig_exp.add_subplot(title="P [Pa]")
        self.axes_P_exp.set_xlabel("Y [m]")
        self.axes_P_exp.set_ylabel("X [m]")

        self.canvas_exp = FigureCanvasTkAgg(self.fig_exp, self.frame_graphes_exp)
        self.canvas_exp.draw()
        self.canvas_exp.get_tk_widget().pack()   

        toolbar = NavigationToolbar2Tk(self.canvas_exp, self.frame_graphes_exp)
        toolbar.update()
        self.canvas_exp._tkcanvas.pack()

        Label (self.fen,text="Cliquez pour faire une explosion",font="Arial 20").grid(row=0,column=1)

        self.rho_exp = np.ones((50,50))
        self.ux_exp = np.zeros((50,50))
        self.uy_exp = np.zeros((50,50))
        self.P_exp = np.ones((50,50))

        plot_p = self.axes_P_exp.imshow(self.P_exp,vmin=1,vmax=10,cmap="hot")
        self.fig_exp.colorbar(plot_p)

        self.axes_P_exp.legend()
        self.flag = False

        Button(self.fen,text="Stop",command=self.stop_exp).grid(row=2,column=2,padx = 20)
        Button(self.fen,text="Reset",command=self.reset_exp).grid(row=3,column=2,padx = 20)


        self.canvas_exp.get_tk_widget().bind("<Button-1>",self.exploser)

        self.flux_exp = StringVar()
        self.flux_exp.set("LF")

        self.Frame_flux_exp = LabelFrame(self.fen, text="Méthode de résolution")
        self.Frame_flux_exp.grid(row=1,column = 2,padx= 20,pady =20)

        Radiobutton(self.Frame_flux_exp,text="Lax Friedrich",value="LF",variable=self.flux_exp).grid(row = 1, column = 1)
        Radiobutton(self.Frame_flux_exp,text="Lax Wendroff",value="LW",variable=self.flux_exp).grid(row = 2, column = 1)


    def stop_exp(self):
        self.flag = False

    def reset_exp(self):
        self.flag = False
        self.rho_exp = np.ones((50,50))
        self.ux_exp = np.zeros((50,50))
        self.uy_exp = np.zeros((50,50))
        self.P_exp = np.ones((50,50))

        self.axes_P_exp.imshow(self.P_exp,vmin=1,vmax=10,cmap="hot")
        self.canvas_exp.draw()
    def exploser(self,event):

        self.fen.update()
        Lx = int(self.canvas_exp.get_tk_widget()["width"])
        Ly = int(self.canvas_exp.get_tk_widget()["height"])

        y = int(event.x/Lx * 50) 
        x = int(event.y/Ly * 50) 

        xmin= max(0,x-10)
        xmax = min(49,x+10)
        ymin= max(0,y-10)
        ymax = min(49,y+10)

        self.step_exp = 0

        self.P_exp[xmin:xmax,ymin:ymax] +=9 
        #self.P_exp[ymin,ymax] +=9 

        if self.flag == False:
            self.flag = True
            self.animation_explosion()

    def animation_explosion(self):

        if self.step_exp % 10 == 0:
            self.axes_P_exp.imshow(self.P_exp,vmin=1,vmax=10,cmap="hot")
            self.canvas_exp.draw()
        #fen.after(10)

        self.step_exp +=1
        flux = self.flux_exp.get()

        for i in range(50):
            dx = 1/50

            rho_i = self.rho_exp[:,i]
            u_i = self.ux_exp[:,i]
            P_i = self.P_exp[:,i]

            U_i = U_(rho_i,u_i,P_i)

            U_i = U_next(U_i,dx,flux)

            Res = U_a_la_moins_un(U_i)
            self.rho_exp[:,i] = Res[:,0]
            self.ux_exp[:,i] = Res[:,1]
            self.P_exp[:,i] = Res[:,2]

            rho_i = self.rho_exp[i,:]
            u_i = self.uy_exp[i,:]
            P_i = self.P_exp[i,:]

            U_i = U_(rho_i,u_i,P_i)

            U_i = U_next(U_i,dx,flux)

            Res = U_a_la_moins_un(U_i)
            self.rho_exp[i,:] = Res[:,0]
            self.ux_exp[i,:] = Res[:,1]
            self.P_exp[i,:] = Res[:,2]


        if self.flag : self.fen.after(1,self.animation_explosion)

    def Plotter(self):

        self.fen_plot=Toplevel(self)

        self.fig_plot = Figure(figsize=(8,8), dpi=100)

        X = np.linspace(0,1)

        self.frame_graphes_plot = Frame(self.fen_plot, borderwidth =2,padx = 10, pady = 20)
        self.frame_graphes_plot.grid(row = 1, column =1)

        self.axes_rho_plot = self.fig_plot.add_subplot(221)
        self.axes_rho_plot.set_xlabel("X [m]")
        self.axes_rho_plot.set_ylabel("rho")


        # Velocity
        self.axes_u_plot = self.fig_plot.add_subplot(222)
        self.axes_u_plot.set_xlabel("X [m]")
        self.axes_u_plot.set_ylabel("u [m/s]")
        
        # Pressure
        self.axes_P_plot = self.fig_plot.add_subplot(223)
        self.axes_P_plot.set_xlabel("X [m]")
        self.axes_P_plot.set_ylabel("P")

        
        # Internal Energy
        self.axes_U_plot = self.fig_plot.add_subplot(224)
        self.axes_U_plot.set_xlabel("X [m]")
        self.axes_U_plot.set_ylabel("U_int")

        self.canvas_plot = FigureCanvasTkAgg(self.fig_plot, self.frame_graphes_plot)
        self.canvas_plot.draw()
        self.canvas_plot.get_tk_widget().pack()

        toolbar = NavigationToolbar2Tk(self.canvas_plot, self.frame_graphes_plot)
        toolbar.update()
        self.canvas_plot._tkcanvas.pack()

        Button(self.fen_plot,text = "Ouvrir", command = self.tracer).grid(row=1,column=2,padx = 20)

    def tracer(self):
        fichier = askopenfilename(filetypes=[('Fichiers textes','.txt')], initialdir="./output")
        if fichier :
            data = pd.read_csv(fichier,skiprows=3,index_col="n_cell",delimiter=" ")

            split = fichier.split("/")
            label = split[len(split)-1]

            flux = label.split("_")[-2]
            t = label.split("_")[-1][:-4]

            label = flux+", t = "+str(round(float(t),3))+" s"

            P = data["P"].to_numpy()
            u = data["u"].to_numpy()
            rho = data["rho"].to_numpy()

            X = np.linspace(0,1,num=len(P))

            U_int = 2*P/rho

            self.axes_rho_plot.plot(X,rho,label=label)
            self.axes_u_plot.plot(X,u,label=label)
            self.axes_P_plot.plot(X,P,label=label)
            self.axes_U_plot.plot(X,U_int,label=label)

            self.axes_rho_plot.legend()
            self.axes_u_plot.legend()
            self.axes_P_plot.legend()
            self.axes_U_plot.legend()

            self.canvas_plot.draw()

    def generer_config(self):
        pass

    def Conditions_bord (self):

        self.U_int[0]=self.U_int[1]
        self.P[0]=self.P[1]
        self.rho[0]=self.rho[1]
        self.u[0]=self.u[1]

        self.U_int[self.n_cell-1]=self.U_int[self.n_cell-2]
        self.P[self.n_cell-1]=self.P[self.n_cell-2]
        self.rho[self.n_cell-1]=self.rho[self.n_cell-2]
        self.u[self.n_cell-1]=self.u[self.n_cell-2]

    def plot(self):

        self.U_int = 2*self.P/self.rho

        self.Conditions_bord()

        self.plot_rho.set_data(self.X,self.rho)
        self.plot_u.set_data(self.X,self.u)
        self.plot_P.set_data(self.X,self.P)
        self.plot_U.set_data(self.X,self.U_int)

        self.maj_echelle(self.axes_u, self.u)
        self.maj_echelle(self.axes_P, self.P)
        self.maj_echelle(self.axes_rho, self.rho)
        self.maj_echelle(self.axes_U, self.U_int)

    def maj_echelle (self, axes, var) :
        if var.any() !=0 :
            dy = np.max(var) - np.min(var)
            if dy != 0 :
                axes.set_ylim(np.min(var) - dy/10, np.max(var)+dy/10)

    def lancer(self):
        self.stop = False
        self.plot_finis = 0
        try :
            self.tmax = float(self.t_stop.get())
        except:
            self.tmax = 0.25
            showwarning("Erreur", "Tmax doit être un float\nReglage à 0.25 s par défaut")
            self.t_stop.delete(ALL)
            self.t_stop.insert(END,"0.25")

        try:
            self.Nplot = int(self.N_sorties.get())
        except:
            self.Nplot = 1
            showwarning("Erreur", "Le nombre de sorties doit être entier\nReglage à 1 par défaut")
            self.t_stop.delete(ALL)
            self.t_stop.insert(END,"1")

        self.Simulation()

    def Simulation(self):
        flux =self.flux.get()
        self.n +=1 
        
        dx = self.X[1]-self.X[0]
        
        if flux in ("LF","LW"):
            self.T += delta_t(self.U[:, 1], a_(self.U[:, 2], self.U[:, 0]),dx)
            self.U = U_next(self.U,dx,flux)
            Res = U_a_la_moins_un(self.U)
        if flux == "Riemann" :
            self.T += 0.001
            Riemann_Sim = Riemann_Solver(self.nom_fichier[:-5])
            Res = Riemann_Sim.Evol(self.T)

        """if flux == "Godunov" :   
            dt = delta_t(self.U[:, 1], a_(self.U[:, 2], self.U[:, 0]),dx)
            self.T += dt

            F12 = np.zeros((self.n_cell,3))

            for i in range(0,len(self.u)-1):

                #print("\n\n x = "+str(i))

                u_i = self.u[i]
                u_f = self.u[i+1]

                p_i = self.P[i]
                p_f = self.P[i+1]

                r_i = self.rho[i]
                r_f = self.rho[i+1]

                Riemann_intermediaire = Riemann_Solver(self.nom_fichier[:-5],Is_Godunov=True, Densities=[r_i,r_f],Velocities=[u_i,u_f],Pressure=[p_i,p_f])
                Res_int = Riemann_intermediaire.Evol(dt)
                rho_int = Res_int[:,0]
                u_int = Res_int[:,1]
                P_int = Res_int[:,2]

                test = F_(np.array([np.mean(rho_int),np.mean(u_int),np.mean(P_int)]))

                F12[i][0]=test[0]
                F12[i][1]=test[1]
                F12[i][2]=test[2]

                #print("rho : "+str(rho_int))
                #print("u : "+str(u_int))
                #print("P : "+str(P_int))
            
            #F12 = F_(U_(F12[:,0],F12[:,1],F12[:,2]))

            self.U += 0.5*dx/dt * (F12-np.roll(F12,1))
            Res = U_a_la_moins_un(self.U)
            self.rho = Res[:,0]
            self.u = Res[:,1]
            self.P = Res[:,2]
            #self.U= U_(rho_int,u_int,P_int)
            #print(np.shape(self.U))
            #self.U = U_next(self.U,dx,"Godunov")"""

        self.Conditions_bord()

        if self.T >= self.tmax / self.Nplot  and self.Nplot  /(self.tmax/self.T) >= self.plot_finis +1:
            self.output()
            self.plot_finis +=1

        if self.graphes.get() :
            if self.n % int(self.step.get()) == 0 :  # Ne plot pas à chaque étape pour accélérer les calculs

                self.rho = Res[:,0]
                self.u = Res[:,1]
                self.P = Res[:,2]

                self.plot()
                self.canvas.draw()
                self.t.configure(text="t = "+str(round(self.T,5))+" s")


            if self.T < self.tmax and not self.stop :
                self.after(1,self.Simulation)
            else :
                self.canvas.draw()
                self.t.configure(text="t = "+str(round(self.T,5))+" s")  
        else :     
            if self.T < self.tmax and not self.stop :
                self.Simulation()
            else :
                showinfo("Fin","Fin")
                
                self.rho = Res[:,0]
                self.u = Res[:,1]
                self.P = Res[:,2]

                self.plot()
                self.canvas.draw()
                self.t.configure(text="t = "+str(round(self.T,5))+" s")


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

    def output (self) :
        os.system("mkdir ./output/"+self.nom_fichier[:-5])

        fichier = open("./output/"+self.nom_fichier[:-5]+"/"+self.nom_fichier[:-5]+"_"+str(self.flux.get())+"_"+str(round(self.T,5))+".txt","w")

        fichier.write("flux : "+str(self.flux.get())+"\n")
        fichier.write("Conditions initiales : "+str(self.nom_fichier)+"\n\n")
        fichier.write("n_cell rho u P\n")

        for i in range(self.n_cell):
            fichier.write(str(i) + " "+ str(self.rho[i])+" "+str(self.u[i])+" "+str(self.P[i])+"\n")

        fichier.close()

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
