class GameInfo:
    def __init__(self, runFile, projectFiles, gameName, gamePath, writeFiles, readFiles, programType, jpypLoc):
        self.runFile = runFile
        self.projectFiles = projectFiles
        self.gameName = gameName
        self.gamePath = gamePath
        self.writeFiles = writeFiles
        self.readFiles = readFiles
        self.programType = programType
        self.jpypeLoc = jpypLoc
    
    def getJpypeLocation(self):
        return self.jpypeLoc
    
    def getRunFile(self):
        return self.runFile
    
    def getGamePath(self):
        return self.gamePath
    
    def getProgramType(self):
        return self.programType
    
    def getGameName(self):
        return self.gameName
    
    def getWriteFile(self):
        return self.writeFiles
    
    def getReadFiles(self):
        return self.readFiles
    
    def getProjectFiles(self):
        return self.projectFiles
    
    def setGamePath(self, inGamePath):
        self.gamePath = inGamePath
    
    def setGameName(self, inGameName):
        self.gameName = inGameName
    
    def setWriteFile(self, inWriteFiles):
        self.writeFiles = inWriteFiles
    
    def setReadFiles(self, inReadFiles):
        self.readFiles = inReadFiles
    
    def setProjectFiles(self, inProjectFiles):
        self.projectFiles = inProjectFiles