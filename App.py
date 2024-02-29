from tkinter import*
import matplotlib
import numpy as np

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

#import matplotlib.pyplot as plt


class Application (Tk):
    def __init__ (self):
        Tk.__init__(self)
        self["bg"] = "white"
        
        self.fig = Figure(figsize=(5,5), dpi=100)

        X = np.linspace(0,5)
        rho = u = P = U_int = X
        
        self.axes_rho = self.fig.add_subplot(221)
        self.axes_rho.set_xlabel("X [m]")
        self.axes_rho.set_ylabel("rho")
        self.axes_rho.legend()

        # Velocity
        axes = self.fig.add_subplot(222)
        axes.set_xlabel("X [m]")
        axes.set_ylabel("u [m/s]")
        axes.plot(X, u, label="velocity")
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

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)

        self.n = 0

        self.bouton = Button(self,text="Je suis un BOUTON",command=self.plot)
        self.bouton.pack()

    def plot(self,event=None):
        X = np.linspace(0,5)
        #self.fig.clf()
        self.axes_rho.plot(X,self.n*X)
        self.canvas.draw()
        self.n+=1

if __name__ == "__main__" :
    fen = Application()
    fen.bind("<Return>",fen.plot)
    fen.mainloop()
    fen.quit()
