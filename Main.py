import os
import eel
from Engine.Features import *
from Engine.Command import *

def Start():

    eel.init("Www")
    
    PlayAssistSound()

    os.system('start msedge.exe --app="http://localhost:8000/index.html"')

    eel.start('index.html',mode=None,host='localhost',block=True)