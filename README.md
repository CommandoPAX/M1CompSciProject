# Hydrodynamics : Shock Tube and Riemann Solvers

## Installation and configuration

Librairies used : matplotlib, numpy, pandas, pillow

To install the requirements use : `pip install -r requirements.txt` (Python >= 3.9)

To run this program, simply launch the file App.py. 

The initial conditions should be stored in a json file in ./config.

## Utilisation

It is possible to reduce the frequency at which the graphes are updated on the animation to save calculation time.

To save the graphes, use the Button "save the figure" at the bottom left of the window.

The code also saves output file in a .txt file in ./output in the form of a pandas dataframe.
To open these files, Click Options -> Ouvrir une simulation and open the text file to plot it. It is possible to supperpose several graphes

Finally, to test 2D explosions, Options -> Explosions open a new window. Click on the canvas to add a surpressure

