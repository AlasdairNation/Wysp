import os
from abc import ABC, abstractmethod
import sys, os
from pathlib import Path
import importlib.util
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from pathlib import Path
from Main.GameHandler.gameInfo import GameInfo

class plugin_interface(ABC):
    def __init__(self, runFile: str, gameName: str, gamePath: str, fileName: str, programType: str):
        self._runFile = runFile
        self._gameName = gameName
        self._gamePath = gamePath
        self._fileName = fileName
        self._projectFiles = {}
        self.readFiles = []
        self.writeFiles = []
        self._programType = programType
        self.jpypeDir = ''

    # @property and @abstractmethod ensure that the following fields are implemented by plugins.
    # @property.setter allows for the properties to be populated
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
    @abstractmethod
    def gameName(self, newName):
        self._gameName = newName
    
    @property
    @abstractmethod    
    def gamePath(self):
        return str(Path(__file__).resolve().parent)

    @gamePath.setter
    @abstractmethod
    def gamePath(self, newPath):
        self._gamePath = newPath
        
    @property
    @abstractmethod    
    def jpypeDir(self):
        return self.jpypeDir

    @jpypeDir.setter
    @abstractmethod
    def jpypeDir(self, newJpypeDir):
        self.jpypeDir = newJpypeDir()

    @property
    @abstractmethod    
    def projectFiles(self):
        return self._projectFiles

    @projectFiles.setter
    @abstractmethod
    def projectFiles(self, newFiles):
        self._projectFiles = newFiles

    @property
    @abstractmethod    
    def fileName(self):
        return Path(self.gamePath).name

    @fileName.setter
    @abstractmethod
    def fileName(self, newFiles):
        self._fileName = newFiles

    @abstractmethod
    def getInfo(self):
        """Method retrieves plugin info such as the project files, the game name, the game path, 
        its write files and, its read files"""
        gamePath = self.gamePath
        projectFiles = self.getProjectFiles()
        self.jpypeDir = self.getJpypeDir()
        return GameInfo(self.runFile,
                        projectFiles, 
                        self.gameName,
                        gamePath,
                        self.writeFiles,
                        self.readFiles,
                        self.programType,
                        self.jpypeDir) 
        
    @abstractmethod
    def run(self):
        """Method checks if the plugin can be run"""
        if not (Path(self.gamePath + "/" + self.runFile).exists()):
            raise Exception(self.runFile + " does not exist!") 

    def getProjectFiles(self):
        """Method retirces all project files within the plugins directory"""
        project_dir = Path(self.gamePath)
        
        # Populate projectFiles with the directory structure
        for root, dirs, files in os.walk(project_dir):
            for dir_name in dirs:
                self.projectFiles[os.path.join(root, dir_name)] = []
            for file_name in files:
                parent_dir = os.path.join(root, '')
                if parent_dir not in self.projectFiles:
                    self.projectFiles[parent_dir] = []
                self.projectFiles[parent_dir].append(file_name)

        return self
    
    @abstractmethod
    def getJpypeDir(self):
        if hasattr(sys, '_MEIPASS'):
            # PyInstaller will extract the bundled files to _MEIPASS
            bundled_jpype_path = Path(sys._MEIPASS) / "jpype"
            if bundled_jpype_path.exists():
                print(f"JPype bundled path found: {bundled_jpype_path}")
                return bundled_jpype_path
            else:
                raise ImportError("JPype bundled path not found in the executable.")
        else:
            # Fallback to system-installed jpype path (if running outside the executable)
            spec = importlib.util.find_spec("jpype")
            if spec is not None and spec.origin:
                jpype_dir = str(Path(spec.origin).parent)
                print(f"JPype found at: {jpype_dir}")
                return jpype_dir
            else:
                raise ImportError("JPype module not found.")