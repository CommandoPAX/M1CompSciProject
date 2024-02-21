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

This function computes the pressure using the polytropic equation of state with exponent gamma.

### *function* a_ *(P : numpy.array, rho : numpy.array)*

This function computes the speed of sound as defined on page 1 of the subject.

### *function* U_ *(rho : numpy.array, u : numpy.array, P : numpy.array)*

This function computes the array of conserved quantities as defined on page 1 of the subject.

### *function* W_ *(rho : numpy.array, u : numpy.array, P : numpy.array)*

This function returns an array of the primitive quantities.

### *function* delta_t *(u : numpy.array, a : numpy.array, dx : float)*

This function computes the next timestep used for the calculations.

### *function* derivee *(f : function, x : numpy.array)*

This function computes a simple derivative using transmissive boundary conditions
