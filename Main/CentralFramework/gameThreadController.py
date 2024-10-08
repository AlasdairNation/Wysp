import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from CentralFramework.threadController import ThreadController
# Runs the game thread
# To do:
# - exception handling
# - plugin error reception
class gameThreadController(ThreadController):
    lastArgs = ""
    
    def __init__(self,gameHandlerAPI):
        super().__init__(gameHandlerAPI)
    
    # Returns list of currently accessible game plugins
    def getGames(self): 
        return self.api.getGames(dir = "")
    
    # Sets current game
    def setGame(self,GameInfoClass):
        if (self.isRunning()):
            self.stop()
        return self.api.setGame(GameInfoClass)
        
    # Plays the game using inputted args
    def play(self,args):
        if (self.isRunning()):
            self.stop()
        self.lastArgs = args
        self.startThread(self.api.run,args)
    
    # Closes the game
    def stop(self):
        if (self.isRunning()):
            self.killThread()
    
    # Restarts the game using old args
    # Used to have "args" as an input. If you're restarting you're just gonna use the last used args.
    def restart(self):
        self.stop()
        self.play(self.lastArgs)