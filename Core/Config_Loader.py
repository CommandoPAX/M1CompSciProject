# Handles changing the config without having to modify each file by hand

import json

# Version basique, faudra l'améliorer

class Config_Loader() :
    def __init__(self) : 
        with open("./Config/Default_Config.json", "r") as f :
            self.DATA = json.load(f)