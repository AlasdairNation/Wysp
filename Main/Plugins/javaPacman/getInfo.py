from pathlib import Path
from Main.GameHandler.plugin_interface import plugin_interface

class GetInfo(plugin_interface):
    def __init__(self):
        # Only change the following 5 line
        self._runFile = "javaPacman.py"
        self._gameName = 'Java Pacman' # Name of main game file.
        self.writeFiles = ['Search.java', 'CornersProblem.java', 'Heuristics.java', 'ClosestDotSearchAgent.java', 'AnyFoodSearchProblem.java', 'commands.txt']  # Files which can be edited.
        self.readFiles = ['All']  # Files which can be read, Make a list of files that you want them to read or use 'All' for full access.
        self._programType = "java"

        # Do not change the following lines
        self._fileName = ''
        self._gamePath = ''
        self.projectFiles = {}
        self.jpypeDir = self.getJpypeDir()
    
    # Implementing the abstract properties
    @property
    def gameName(self):
        return self._gameName
    
    @property
    def runFile(self):
        return self._runFile

    @runFile.setter
    def runFile(self, newRun):
        self._runFile = newRun
        
    @property
    def programType(self):
        return self._programType
    
    @programType.setter
    def programType(self, newType):
        self._programType = newType

    @gameName.setter
    def gameName(self, newName):
        self._gameName = newName

    @property
    def gamePath(self):
        return str(Path(__file__).resolve().parent)

    @gamePath.setter
    def gamePath(self, newPath):
        self._gamePath = newPath

    @property
    def projectFiles(self):
        return self._projectFiles

    @projectFiles.setter
    def projectFiles(self, newFiles):
        self._projectFiles = newFiles

    @property
    def fileName(self):
        return super().fileName

    @fileName.setter
    def fileName(self, newName):
        self._fileName = newName
        
    @property
    def jpypeDir(self):
        return self._jpypeDir

    @jpypeDir.setter
    def jpypeDir(self, newPath):
        self._jpypeDir = newPath
        
    def getJpypeDir(self):
        self.jpypeDir = super().getJpypeDir()
        return self.jpypeDir
        
    def run(self):
        return super().run()

    def getInfo(self):
        return super().getInfo()