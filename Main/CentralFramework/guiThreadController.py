import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from CentralFramework.threadController import ThreadController
# Runs the GUI thread
# TO DO:
# - Exception handling
# - link code screen up once the API is finished

class guiThreadController(ThreadController):
    def __init__(self,guiHandlerAPI):
        super().__init__(guiHandlerAPI)
    
    # loads the boot screen where the user can choose to pick a new project, or load an old one.
    # Blocks until gui returns result
    def newOrLoadScreen(self):
        self.api.newOrLoadWindow()
    
    # Loads the game selection screen 
    # Blocks until game selection is returned
    def gameSelectionScreen(self, Games, Projects, _returnMethod): #Game is of type List<GameInfoClass>
        self.api.startGameSelectionWindow(games = Games, projects = Projects, _returnMethod = _returnMethod)
            
    # Loads project selection screen
    # Blocks until project selection is returned
    def projectSelectionScreen(self,Projects,_returnChooseProject,_deleteMethod): #Projects if of type List<ProjectInfoClass>
        self.api.startProjectSelectionWindow(projects = Projects,_returnMethod = _returnChooseProject, _deleteMethod = _deleteMethod)

    
    # Boots the coding screen, giving the gui access to both game and project thread controller for direct interaction
    # Blocks until coding screen is exited
    def codeScreen(self,Game, Project,_returnMethod): # Game of type GameThreadController, Project of type ProjectThreadController
        self.api.startMainWindow(gameThread = Game, projectThread = Project,_returnMethod= _returnMethod) # self.api.startMainWindow(Game,Project)
   