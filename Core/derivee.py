import numpy as np

def derivee (f, x : np.array):
    global n_cell

    y = f(x)
    dx = x[1]-x[0]
    yp = np.zeros(n_cell)
    for i in range(len(x)):
        if i >=1 and i+1 < len(x) : yp [i] = (y[i-1]+y[i+1])/(2*dx)

        # Transmissive boundary condition

        if i == 0 :
            yp[i] = (y[0]+y[1])/(2*dx)
        if i+1 == len(x) : 
            yp[i] = (y[i-1]+y[i])/(2*dx)

    return yp