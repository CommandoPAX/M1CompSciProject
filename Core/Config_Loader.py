# Handles changing the config without having to modify each file by hand

import json

class Config_Loader() :
    """ 
    Loads the config for a given problem to be used by other files
    """
    def __init__(self) : 
        self.Config_Name = "Sod_Problem"
        with open(f"./Config/{self.Config_Name}.json", "r", encoding="utf-8") as f :
            self.DATA = json.load(f)
            
    def generate_new_config(self, gamma : float, L : float, n_cell : int, C : float, rho : list, u : list, P : list, output_name : str) :
        """ 
        Generates a new config from a given list of parameters and saves it
        """
        NewConfig = {}
        NewConfig["gamma"] = gamma
        NewConfig["L"] = L
        NewConfig["n_cell"] = n_cell 
        NewConfig["C"] = C 
        NewConfig["rho_inf"] = rho[0]
        NewConfig["rho_sup"] = rho[1]
        NewConfig["u_inf"] = u[0]
        NewConfig["u_sup"] = u[1]
        NewConfig["P_inf"] = P[0]
        NewConfig["P_sup"] = P[1]
        
        self.DATA = NewConfig
        
        with open(f"./Config/{output_name}.json", "w", encoding="utf-8") as outf :
            json.dump(self.DATA, outf, indent=4, separators=(", ", ": "), sort_keys=True, skipkeys=True, ensure_ascii=False)
            
        print(f"Configuration changed sucesfully to {output_name}")