# Hydrodynamics : Shock Tube and Riemann Solvers

## Installation and configuration

To run this program, simply launch the file Hydrod_Solver.py which will generate the graphs in the directory graphs.

## Function and Class list : 

### *class* Config_Loader_py *()*

This class is used to load the json config files for the different problems we will study.
To change the config, one must change the Config_Name attribute in the python code.
It only has a single function : 

#### *function* generate_new_config *(self, gamma : float, L : float, n_cell : int, C : float, rho_inf : float, rho_sup : float, u_inf : float, u_sup :float, P_inf : float, P_sup : float, output_name : str)*

This function is called in main to generate a new json file containing the new problem's config.

### *function* P_ *(rho : numpy.array, k : float)*

### *function* a_ *(P : numpy.array, rho : numpy.array)*

### *function* U_ *(rho : numpy.array, u : numpy.array, P : numpy.array)*

### *function* W_ *(rho : numpy.array, u : numpy.array, P : numpy.array)*

### *function* delta_t *(u : numpy.array, a : numpy.array, dx : float)*

### *function* derivee *(f : function, x : numpy.array)*