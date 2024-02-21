#Handler responsible for logging errors
import datetime
import os

#Should only work on Linux based system for now
    
def LogError(CogFunct : str, Error : Exception) : #Function that will handle logging all errors
    try :
        filename = str(datetime.date.today()) + ".log"
        ErrMsg = str(datetime.datetime.now()) + " " + f"{CogFunct} : " + str(Error) + '\n'
        f = open("./Logs/" + filename, "a+")
        f.write(ErrMsg)
        f.close()
    except Exception as e :
        os.system(f"mkdir ./Logs")
        filename = str(datetime.date.today()) + ".log"
        ErrMsg = str(datetime.datetime.now()) + " " + f"{CogFunct} : " + str(Error) + '\n'
        f = open("./Logs/" + filename, "a+")
        f.write(ErrMsg)
        f.close()