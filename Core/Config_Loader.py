# Handles changing the config without having to modify each file by hand

import json

class Config_Loader() :
    """ 
    Loads the config for a given problem to be used by other files
    """
    def __init__(self) : 
        self.Config_Name = "Sod_Problem"
        with open(f"./Config/{self.Config_Name}.json", "r") as f :
            self.DATA = json.load(f)