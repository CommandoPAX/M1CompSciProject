# Handles changing the config without having to modify each file by hand

import json

with open("./Config/Default_Config.json", "r") as f :
    config = json.load(f)