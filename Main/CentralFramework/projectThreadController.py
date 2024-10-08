import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from CentralFramework.threadController import ThreadController
import queue
import threading
# Runs project thread (file editing etc)
# TO DO:
# Exception handling
# Notifying GUI of project handler responses
class ProjectThreadController(ThreadController):
    def __init__(self,projectHandlerAPI):
        self.commandList = queue.Queue()
        super().__init__(projectHandlerAPI)

    def startThread(self):
        method = self._commandLoop
        if (not self.commandList.empty()):
            self.commandList = queue.Queue()
        
        methodArgs = (self.commandList,self.api)
        return super().startThread(method, methodArgs)
        
    def closeThread(self):
        self.requestShutdown()
        return self.joinThread()
    
    # Returns list of available projects
    def getProjects(self):
        return self.api.getProjects('')
    
    def getCurrentProject(self):
        return self.api.getCurrentProject()
    
    # Sets current project
    def setProject(self,ProjectInfo):
        if (self.isRunning()):
            self.joinThread()
        return self.api.getProjectsInfo(ProjectInfo)
    
    def deleteProject(self,ProjectInfo):
        response = ""
        if (not self.isRunning()):
             response = self.api.deleteProject(ProjectInfo)
        else:
            response = "Error: Can't delete project while running code screen"
        return response
    
    # Sets current project by creating new project
    def newGameProject(self, GameInfo, ProjectName):
        return self.api.newGameProject(GameInfo,ProjectName)
    
    def bindMainWindow(self,mainWindow):
        self.api.bindMainWindow(mainWindow)
    
    # Opens a file for editing, boots the run loop
    def open(self,FilePath): #FilePath of type File Path
        print("projectThreadHandler.open() is currently not implemented")

    # Requests text update of current file
    def requestUpdate(self,NewText): #New Test of type String
        self._queueCommand(self.api.update,NewText)

    def requestCheck(self,args):
        self._queueCommand(self.api.check, args)
    
    # Requests save of current file
    def requestSave(self, listOfProjects):
        self._queueCommand(self.api.saveProject,listOfProjects)
    
    # Requests compilation of current file
    def requestCompile(self):
        self._queueCommand(self.api.compile, None)

    def requestRun(self, args):
        self._queueCommand(self.api.runProject,args)

    def requestShutdown(self):
        self._queueCommand(None, None) # Poisons consumer queue
    
    # Places command in a queue for _commandLoop to consume
    def _queueCommand(self, command, args):
        self.commandList.put([command,args])

    # Thread loop for the handler
    # Checks if it has any jobs, then waits for notification
    # For software engineers: This is a micro producer / consumer thread pattern
    def _commandLoop(self,args):
        self.commandList = args[0]
        self.api = args[1]
        while(not self.close.is_set()):
            command = self.commandList.get()
            try:
                if (command[0]==None): # Checks for shutdown command
                    self.close.set()
                else:
                    if (command[1]!= None): # If has args, run with args
                        command[0](command[1])
                    else: # If no args, run without
                        command[0]()
            except Exception as e:
                print("Command Error: ",e)
        return self.api