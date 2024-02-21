# Handles changing the config without having to modify each file by hand

import json

# Version basique, faudra l'améliorer

class Config_Loader() :
    def __init__(self) : 
        self.Config_Name = "Sod_Problem"
        with open(f"./Config/{self.Config_Name}.json", "r") as f :
            self.DATA = json.load(f)