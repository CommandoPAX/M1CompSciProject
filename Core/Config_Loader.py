# Handles changing the config without having to modify each file by hand

import json
from Core.Error_Handler import LogError

class Config_Loader() :
    """ 
    Loads the config for a given problem to be used by other files
    """
    def __init__(self) : 
        try :
            self.Config_Name = "Sod_Problem"
            with open(f"./Config/{self.Config_Name}.json", "r", encoding="utf-8") as f :
                self.DATA = json.load(f)
        except Exception as e :
            LogError("Config_Loader.__init__", e)
            print(e)
            
    def generate_new_config(self, gamma : float, L : float, n_cell : int, C : float,
                            rho_inf : float, rho_sup : float, u_inf : float,
                            u_sup : float, P_inf : float, P_sup : float, output_name : str) :
        """ 
        Generates a new config from a given list of parameters and saves it
        """
        try :
            NewConfig = {}
            NewConfig["gamma"] = gamma
            NewConfig["L"] = L
            NewConfig["n_cell"] = n_cell 
            NewConfig["C"] = C 
            NewConfig["rho_inf"] = rho_inf 
            NewConfig["rho_sup"] = rho_sup 
            NewConfig["u_inf"] = u_inf 
            NewConfig["u_sup"] = u_sup 
            NewConfig["P_inf"] = P_inf
            NewConfig["P_sup"] = P_sup
            
            self.DATA = NewConfig
            
            with open(f"./Config/{output_name}.json", "w", encoding="utf-8") as outf :
                json.dump(self.DATA, outf, indent=4, separators=(", ", ": "), sort_keys=True, skipkeys=True, ensure_ascii=False)
                
            print(f"Configuration changed sucesfully to {output_name}")
        except Exception as e :
            LogError("Config_Loader.generate_new_config", e)
            print(e)