import sys 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qsci import *
from PyQt5.QtGui import *
from CentralFramework.gameThreadController import gameThreadController
from CentralFramework.projectThreadController import ProjectThreadController

class FrontEndApi:
    def __init__(self):
        self.app = QApplication.instance() or QApplication([])
        self.mainWindow = None
        self.gameWindow = None
        self.projectWindow = None
        self.currentWindow = None
        self.gameThread : gameThreadController = None
        self.projectThread : ProjectThreadController = None
        
    #Note: local import to avoid circular import
    #Run event loop to prevent freezing in terminal on launch 
    def startMainWindow(self, projectThread=None, gameThread=None, _returnMethod = None):
        from FrontEnd.windows.mainWindow import MainWindow
        if self.currentWindow:
            self.currentWindow.close()

        if projectThread:
            self.projectThread : ProjectThreadController = projectThread
        if gameThread:
            self.gameThread : gameThreadController = gameThread

        self.MainWindow = MainWindow(self,_returnMethod  = _returnMethod)
        self.currentWindow = self.MainWindow

        self.MainWindow.show()

    # To be used to save an entire project in Project handler
    def saveProject(self, listFilesToSave):
        #for path, content in listFilesToSave.items():
            #print(f"Path: {path} \nContent: {content}\n")
            # In place, uncomment when projectThread.requestSave takes in correct parameters
        if self.projectThread:
            self.projectThread.requestSave(listFilesToSave)

    # Used to save an individual file
    def saveFile(self, file): #file -> { path : content}
        self.saveProject(file)

    #Might not need, app can launch from project window 
    #Note: local import to avoid circular import
    #Run event loop to prevent freezing in terminal on launch 
    def startGameSelectionWindow(self, games=None, projects=None, _returnMethod = None):
        from FrontEnd.windows.gameSelectionWindow import GameSelectionWindow 
        if self.currentWindow:
            self.currentWindow.close()

        self.gameWindow = GameSelectionWindow(api=self, games=games, projects=projects, _returnMethod = _returnMethod)
        self.currentWindow = self.gameWindow
        self.gameWindow.show()
    

    #Note: current starting point of program 
    #Run event loop to prevent freezing in terminal on launch 
    def startProjectSelectionWindow(self,_returnMethod = None, projects = None, _deleteMethod = None):
        from FrontEnd.windows.projectSelectionWindow import ProjectSelectionWindow
        if self.currentWindow:
            self.currentWindow.close()
        #this needs to be replaced with projects passed into this function
        self.projectWindow = ProjectSelectionWindow(api=self, projects=projects, _returnMethod = _returnMethod, _deleteMethod = _deleteMethod)
        self.currentWindow = self.projectWindow
        self.projectWindow.show()
        
    #Note: wrapper to access project selection window from central framework  
    def newOrLoadWindow(self):
        self.startProjectSelectionWindow()


    # Event loop to prevent freezing on starting game window
    # this prevented freezing before, but as of 24/08 it isn't needed for the program to function, leaving just in case it is needed later

    # def runEventLoop(self):
    #     if not QApplication.instance().startingUp():
    #         sys.exit(self.app.exec())

    # Sends error message from the rest of the system to error log
    def addErrorMsg(self, msg):
        if self.MainWindow: #If initialised
            self.MainWindow.addErrorMsg(msg)


#     #TODO create game window 
#     def startGameWindow():
#         return None