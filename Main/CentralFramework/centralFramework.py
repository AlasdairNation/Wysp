# Ewans fix for python not recognizing the parent package
# Praise be the Messiah
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from FrontEnd.frontEndApi import FrontEndApi
from GameHandler.gameHandlerAPI import gameHandlerAPI
from ProjectHandler.projectHandler import ProjectHandlerAPI
from CentralFramework.gameThreadController import gameThreadController
from CentralFramework.guiThreadController import guiThreadController
from CentralFramework.projectThreadController import ProjectThreadController

class Core:
    # APIs init external for testability
    def __init__(self,gameMaster,guiMaster,projectMaster):
        self.gameMaster = gameMaster
        self.guiMaster = guiMaster
        self.projectMaster = projectMaster
        self.running = True

    # boot sequence of program.
    def run(self):
        self.chooseProject()

    # Opens the boot screen, allowing the user to choose a project / game
    # TO DO: error checking (try catch etc), and interpretting messages from APIs that indicate error
    def chooseProject(self):
        # Acquire resource
        projectList = self.projectMaster.getProjects()
        # Project selection
        self.guiMaster.projectSelectionScreen(projectList, self._returnChooseProject,self.projectMaster.deleteProject)

    def _returnChooseProject(self,chosenProject):
        if (chosenProject == None): # End Program Flag
            print("chosen project is none")
            self.endProgram()
        else:
            if (chosenProject == 0): # New Project Flag
                self.chooseGame()
            else: # Load Project
                self.projectMaster.setProject(chosenProject)
                self.startEditor()

    def chooseGame(self):
        gameList = self.gameMaster.getGames()
        projectList = self.projectMaster.getProjects()
        self.guiMaster.gameSelectionScreen(gameList, projectList, self._returnChooseGame)

    def _returnChooseGame(self,chosenGame, projectName = None):
        if (chosenGame == None):
            self.endProgram()
        elif(chosenGame == 0):
            self.chooseProject()
        else:
            self.projectMaster.newGameProject(chosenGame, projectName)
            self.startEditor()

    # Opens the editor
    def startEditor(self):
        try:
            self.projectMaster.startThread()
            self.guiMaster.codeScreen(self.gameMaster,self.projectMaster,self._returnStartEditor)
        except Exception as e:
            print("Fatal Error: ",e)
            self.endProgram()
    
    def _returnStartEditor(self, exitProgram):
        self.projectMaster.closeThread()
        print("exitProgram is ", exitProgram)
        if (exitProgram):
            self.endProgram()
        else:
            self.chooseProject()
        
    # Closes all threads, ends the program
    def endProgram(self):
        print("Closing program...")
        if (self.gameMaster!= None):
            self.gameMaster.closeThread()
        if (self.projectMaster != None):
            self.projectMaster.closeThread()
        if (self.guiMaster != None):
            self.guiMaster.closeThread()
        self.running = False
    
def main():
    fAPI = FrontEndApi()
    gAPI = gameHandlerAPI()  
    pAPI = ProjectHandlerAPI()

    guiMaster = guiThreadController(fAPI)
    gameMaster = gameThreadController(gAPI)
    projectMaster = ProjectThreadController(pAPI) 

    coreProgram = Core(gameMaster,guiMaster,projectMaster)
    try:
        coreProgram.run()
    except Exception as e:
        print("Fatal error: ",e,"\n")
        if ((coreProgram != None)and(coreProgram.running)):
            coreProgram.endProgram()   
 
if __name__ == '__main__':
    main()