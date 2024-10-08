import sys
import os
from PyQt5.QtWidgets import *
from FrontEnd.frontEndApi import FrontEndApi
from CentralFramework.centralFramework import Core
from CentralFramework import centralFramework


if __name__ == '__main__':
          
    api = FrontEndApi()
    # Keep these comments, you can comment and uncomment these to check the current
    # application flow
    
    #api.startProjectSelectionWindow()
    centralFramework.main() 
    #api.startMainWindow() # MAIN FLOW AT THE MOMENT, UNTIL CORE FULLY FIGURED OUT

    #keeping this line here is allowing it to start the event loop i think, without it something breaks i dont know why yet
    #something to do with multiple instances of event loop running 
    sys.exit(api.app.exec_())

    