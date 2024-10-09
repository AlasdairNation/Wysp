from pathlib import Path
from Main.GameHandler.gameHandlerAPI import gameHandlerAPI
import shutil
import os
import subprocess
import sys, threading
import re, ast, glob, platform

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from GameHandler.gameInfo import GameInfo  # Use absolute import

#Project Info Class which is the object that has the project information. Called when making a new project.
class ProjectInfo:
    def __init__(self, inProjectName, inProjectPath, inGameInfo):
        self.projectName = inProjectName
        #self.lastModified = inLastModified
        self.projectPath = inProjectPath
        self.gameInfo = inGameInfo
    
    def getProjectInfoName(self):
        return self.projectName
    
    #def getProjectInfoModified(self):
        #return self.lastModified
    
    #def setProjectInfoModified(self, modified):
        #self.lastModified = modified
    
    def getProjectInfoPath(self):
        return self.projectPath
    
    def getProjectInfoGameInfo(self):
        return self.gameInfo

class ProjectHandlerAPI:

    def __init__(self):
        self.projectHandler = ProjectHandler()

    def bindMainWindow(self,mainWindow):
        self.projectHandler.bindMainWindow(mainWindow=mainWindow)
    
    #return a list of project names
    def getProjects(self,str):
        return ProjectHandler.getProjectDirs(str)
    
    def getCurrentProject(self):
        return ProjectHandler.getCurrentProject()
    
    #loads a selected project and returns a process completion message
    def getProjectsInfo(self,str):
        return ProjectHandler.getProjectsInfo(str)
    
    #Method called when creating a new project or changing into an existing project
    def setProject(self,inProjectInfo):
        return ProjectHandler.setProject(inProjectInfo)
    
    def deleteProject(self,inProjectInfo):
        return ProjectHandler.deleteProject(inProjectInfo)
    
    #Method called when game is selected by user when creating a new project.
    def newGameProject(self,inGameInfo, inProjectName, dir=''):
        if dir == '':
            # Checks if SavedProjects folder exists
            saveFolder = os.path.join(os.getcwd(), "SavedProjects")
            if not os.path.exists(saveFolder):
                os.makedirs(saveFolder)

            # Allows files of same name to exist by apending _num at the end
            saveFolder = Path(saveFolder)
            finalProjectPath = Path(saveFolder / inProjectName)
            if finalProjectPath.exists():
                i = 1
                while finalProjectPath.exists():
                    potentialProjectPath = saveFolder / f"{inProjectName}_{i}"
                    if not potentialProjectPath.exists():
                        finalProjectPath = Path(potentialProjectPath)
                    i += 1
        else:
            script_dir = dir
            finalProjectPath = Path(script_dir + "/" + inProjectName)

        newProjectInfo = ProjectInfo(inProjectName, finalProjectPath, inGameInfo)
        return ProjectHandler.setProject(newProjectInfo)
    
    def saveProject(self, FilesToSave):
        ProjectHandler.saveProject(self, FilesToSave)
    
    def open(FilePath): # FilePath of type File Path
        return "String"
    
    def update(self,NewText): # NewText of type String
        return "String"
    
    def save(self):
        return "String"
    
    def compile(self):
        return "String"
    
    def check(self,args):
        
        return self.projectHandler.CheckSyntax(args[0], javaFiles=args[1])
    
    def runProject(self,args):
        ProjectHandler.Run(args)

class ProjectHandler:
    global process
    global processLock
    processLock = threading.Lock()
    process = None

    def __init__(self):
        self.gameRunning = False
        self.lock = threading.Lock()
        self.mainWindow = None
        self.languageHandler = None

    def bindMainWindow(self,mainWindow):
        self.mainWindow = mainWindow  # Store the instance of MainWindow
        self.languageHandler = languageHandler(self.mainWindow.syntaxHighlighter) #sets up front end syntax highlighter link
        
    # FileHandler = FileEditor
    # LanguageHandler = Language Handler
    CurrentProject = ProjectInfo
    
    # CurrentFile = File
    
    def setCurrentProject(inProjectInfo):
        ProjectHandler.CurrentProject = inProjectInfo

    def getCurrentProject():
        return ProjectHandler.CurrentProject
    
    def getProjectsInfo(inPrjPath):
        message = "Project loading not successful."
        projectName = os.path.basename(inPrjPath)
        gHandlerAPI = gameHandlerAPI()
        gameInfoList = gHandlerAPI.getGames(inPrjPath.parent)
        for game in gameInfoList:
            if os.path.basename(game.getGamePath()) == projectName:
                gameInfo = game
                projectInfo = ProjectInfo(projectName, inPrjPath, gameInfo)
                ProjectHandler.setCurrentProject(projectInfo)
                message = "Project loading Successful."
        return message
    
    #Creates a new project in SavedProjects by copying games from plugin into 
    def setProject(inProjectInfo):
        successful = "Project was not set!"

        try:
            if not(os.path.exists(inProjectInfo.getProjectInfoPath())): 
                successful = "Successfully set project."    
                ProjectHandler.setCurrentProject(inProjectInfo)                                                                     #Set as current project
                gameInfo = inProjectInfo.getProjectInfoGameInfo()                                                                   #Now using GameInfo within PrjectInfo we will close the files from the plugin to clone into SavedProjects
                shutil.copytree(gameInfo.getGamePath(), inProjectInfo.getProjectInfoPath())                                         #Copy game into newly created project folder
            else:
                ProjectHandler.setCurrentProject(inProjectInfo)                                                                     #Just set it as the current project
                successful = "Successfully set project."
        except Exception as e:
            successful = e

        return successful
    
    # Deletes project given a projectInfo class
    # Contains modified code from an online tutorial
    #<Dharmkar, A (03-Aug-2023) "How to delete all files in a directory with Python?" (V1.0) [Tutorial]. https://www.tutorialspoint.com/how-to-delete-all-files-in-a-directory-with-python
    def deleteProject(inProjectInfo):
        response = "Project Successfully Deleted"
        try:
            projectPath = inProjectInfo#.getProjectInfoPath()
            if (os.path.exists(projectPath)):
                with os.scandir(projectPath) as entries:
                    for entry in entries:
                        if entry.is_file():
                            os.remove(entry.path)
                        else:
                            shutil.rmtree(entry.path)
                shutil.rmtree(projectPath)
        except Exception as e:
                        response = "Failed to Delete Project: \n" + str(e)
        return response

    
    #Method will receive a list of files to save via dictionary (Key:File Path Value:Contents of file)
    def saveProject(self, ListOfFiles):
        for k, v in ListOfFiles.items():        #For each file
            try:
                if(os.path.exists(k)):              #If it exists
                    f = open(k, 'w')                #Re-create the file
                    f.write(v)                      #Write the new contents to the file which was just re-created
            except Exception as e:
                print(e)
    
    #This methods code was adapted from EWANS getProjectFiles() method inside getInfo.py (thank you ewan)
    def getProjectDirs(inStr):
        listOfProjects = []
        if inStr == '':
            saveFolder = os.path.join(os.getcwd(), "SavedProjects")
            if not os.path.exists(saveFolder):
                os.makedirs(saveFolder)
        else:
            saveFolder = inStr
            
        path = Path(saveFolder).resolve()
        for entry in path.iterdir():
            if entry.is_dir():
                listOfProjects.append(entry)

        listOfProjects.sort()

        return listOfProjects

    def SetLanguage(LanguageHandler):
        return None
    
    def OpenFile():
        return None
    
    def CloseFile():
        return None
    
    def UpdateCurrentFile():
        return None
    
    def SaveCurrentFile():
        return None
    
    def CompileProject():
        return None
    
    def ReportErrorToUser():
        return None
    
    def CheckSyntax(self,filepath, javaFiles):
        if (self.languageHandler != None):  
            self.languageHandler.checkSyntax(filepath, javaFiles=javaFiles)


    def Run(args):
        global processLock
        global process
        compiled = False
        ProjectHandler.close()
        projectInfo = ProjectHandler.getCurrentProject()
        if projectInfo is None: raise ValueError("No current project set.") # Makes sure there is a project chosen.
        
        # Gets the various information needed about the game.
        gameProjectInfo = projectInfo.getProjectInfoGameInfo() 
        programtype = gameProjectInfo.getProgramType()
        runFile = str(gameProjectInfo.getRunFile())
        gamePath = str(projectInfo.getProjectInfoPath())
  
        if (runFile.endswith(".py")): # Checks if the run file is a python file.
            def getPyExec():
            # Check if python3 exists
                py3Path = shutil.which('python3')
                pyPath = shutil.which('python')
                if pyPath:
                    return 'python'
                
                if py3Path:
                    return 'python3'

                # If neither python3 nor python exists, raise an error
                raise EnvironmentError("Neither 'python3' nor 'python' is found in the system's PATH.")
            
            pythonExec = getPyExec()
            # Run python files using your python COMMENT OUT WHEN PACKAGING
            if programtype == "java":
                compiled = ProjectHandler.Compile()
                jpypDir = gameProjectInfo.getJpypeLocation()
                command = [pythonExec, os.path.join(gamePath, runFile), '--jpype-dir', str(jpypDir)] + args.split()
            else: 
                command = [pythonExec, os.path.join(gamePath, runFile),] + args.split() # Runs python file using the inputed arguments=
            compiled = True
        
        elif (str(runFile).endswith(".java")): # Checks if the run file is java.
            compiled = ProjectHandler.Compile()
            if (compiled):
                #ONLY UNCOMMENT WHEN PACKAGING GAME
                #jrePath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'Libraries', 'Windows', 'windows-jdk', 'bin', 'java.exe') # USE WHEN USING WINDOWS
                #jrePath =  os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'Libraries', 'Linux', 'linux-jdk', 'bin', 'java') # USE WHEN DOING LINUX
                #command = [jrePath, "-cp", gamePath, gameName.replace(".java", "")] + args.split()
                # Run Java files using your JRE COMMENT OUT WHEN PACKAGING
                classpath_separator = ";" if os.name == "nt" else ":"
                jpypDir = gameProjectInfo.getJpypeLocation()
                classpath = f"{gamePath}{classpath_separator}{jpypDir}"
                command = ['java', "-cp", classpath, runFile.replace(".java", "")] + args.split()
                
        if compiled:
            processLock.acquire()
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, bufsize=1)
            processLock.release()
            
        def runOutput():
            global process
            global processLock
            myProcess = process #prevents reference to original process from being nulled
            try:
                if (myProcess!=None):
                    for stdoutLine in iter(myProcess.stdout.readline, ''):
                        if (myProcess!= None):
                            print(stdoutLine, end='', flush=True)  # Send to terminal
                if (myProcess!=None):
                    print("clear", file=sys.stderr)
                    for stderrLine in iter(myProcess.stderr.readline, ''):
                        if (myProcess!= None):
                            print(stderrLine, file=sys.stderr, flush=True)  # Send to error log
                processLock.acquire()
                myProcess.stderr.close()
                myProcess.stdout.close()
                processLock.release()
            except Exception as e:
                print("Game Runner Error: ",e)
            finally:
                processLock.acquire()
                if (myProcess!= None):
                    myProcess.terminate()
                    myProcess.wait()
                    myProcess = None
                processLock.release()
                
        if (compiled):
            outCapture = threading.Thread(target=runOutput)
            outCapture.start()

        # This thread loop handles redirecting output to the terminal
        # Modified Ewans method to enable threading
        # This isn't particularly good coding practice, but it's fine because we're not modifying anything.
        # Does it throw exceptions if you spam the run button? hell yeah. Is it all accounted for? god I hope so.

    # Closes the game running process so that a new one can be made
    def close():
        global process
        global processLock
        processLock.acquire()
        if (process!= None):
            process.terminate()
            process = None
        processLock.release()
        
    def Compile():
        projectInfo = ProjectHandler.getCurrentProject()
        
        if projectInfo is None: raise ValueError("No current project set.")  # Ensure a project is chosen
        
        gamePath = str(projectInfo.getProjectInfoPath())
        
        # Collect all Java files in the gamePath recursively
        # ADD CLEAR TO STDERR
        javaFiles = []
        for root, dirs, files in os.walk(gamePath):
            for file in files:
                if file.endswith(".java"):
                    javaFiles.append(os.path.join(root, file))
        
        if not javaFiles: raise ValueError("No Java files found to compile.")

        # Path to the bundled JRE's javac (Java compiler) ONLY UNCOMMENT WHEN PACKAGING GAME
        # jrePath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'Libraries', 'Windows', 'windows-jdk', 'bin', 'javac.exe')
        # jrePath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'Libraries', 'Linux', 'linux-jdk', 'bin', 'javac')
        # compProcess = subprocess.Popen([jrePath] + javaFiles, stdout=subprocess.PIPE,  stderr=subprocess.PIPE, universal_newlines=True)
        
        # Compile Java files using the bundled JRE COMMENT OUT WHEN PACKAGING
        if platform.system() == "Windows":
            compileScriptName = "build-java-pacman.bat"
        else:
            compileScriptName = "build-java-pacman.sh"
        scriptSearch = glob.glob(f"**/{compileScriptName}", recursive=True)
        if not scriptSearch:
            raise FileNotFoundError(f"Could not find Java build file {compileScriptName}")
        
        script = Path(scriptSearch[0]).resolve()
        try:
            compProcess = subprocess.Popen([script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            stdout, stderr = compProcess.communicate()
        except Exception:
            # Dear god I don't know why this works
            # For some reason it might not recognise the build file, but it will after you save and write it again.
            # This is a stupid fix for stupid problem.
            if os.path.exists(script):
                file = open(script,'r')
                contents = file.read()
                file.close()
                file = open(script,'w')
                file.write(contents)
                file.close()

                compProcess = subprocess.Popen([script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                stdout, stderr = compProcess.communicate()
                
                

        # Redirect output to the terminal and error log
        if stdout:
            print(stdout)  # Redirect to terminal
        if stderr:
            print("clear", file=sys.stderr)
            print(stderr, file=sys.stderr)  # Redirect to error log
            return False
        
        return True  # Return any errors if present
    
class projectLoader:
    # ProjectFileDirectory = File Path
    # ProjectList = List<ProjectClass>
    
    #MIGHT NOT NEED?
    def NewGameProject(GameInfo):   
        return 0 # Return ProjectInfo
    
    def DeleteProject():
        return None
    
    def LoadProject(ChosenProject): # ChoosenProject of type ProjectInfo
        return 0 # Return ProjectInfoClass
    
    def GetProjectList(): 
        return 0 # Return List<ProjectInfoClass>

class fileEditor:
    def OpenFile():
        return None
    
    def Close():
        return None
    
    def Update():
        return None
    
class languageHandler:
    def __init__(self,highlighter):
        self.highlighter = highlighter

    def checkSyntax(self, filePath, javaFiles):
            
        def runChecker():
            # Runs java or Python Error checking in a subprocess, ends early if file doesn't belong to either
            if filePath.endswith('.py'):
                try:
                    # Use AST parsing to catch any syntax issues
                    with open(filePath, 'r') as source_file:
                        source_code = source_file.read()
                        try:
                            ast.parse(source_code)
                        except SyntaxError as e:
                            error_msg = f"SyntaxError: {e.msg} at line {e.lineno}, column {e.offset}" # Puts it way that the syntax checker can read
                            self.highlighter._clearUnderlinesFrom(filePath)
                            self.handleSyntaxErrorPython(error_msg, filePath)

                except Exception as e:
                    print(f"Exception while checking syntax: {str(e)}")
            elif filePath.endswith('.java'):
                process = subprocess.Popen(['javac'] + javaFiles, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = process.communicate()
                if out:
                    self.highlighter._clearUnderlinesFrom(filePath)
                    for line in out.decode('utf-8').splitlines():
                        self.handleSyntaxErrorJava(line, filePath)
                if err:
                    self.highlighter._clearUnderlinesFrom(filePath)
                    for line in err.decode('utf-8').splitlines():
                        self.handleSyntaxErrorJava(line, filePath)

        if (filePath != None):            
            syntaxCheckThread = threading.Thread(target=runChecker, daemon=True)
            syntaxCheckThread.start()

    
    def handleSyntaxErrorPython(self, errorMSG, filePath):
        match = re.search(r'at line (\d+), column (\d+)', errorMSG)
        if match:
            errorLineNum = int(match.group(1)) - 1  # Convert to 0-indexed
            errorCol = int(match.group(2)) - 1      # Convert to 0-indexed

            # Read the file to find the exact line of code
            with open(filePath, 'r') as f:
                lines = f.readlines()

            if errorLineNum < len(lines):
                errorLine = lines[errorLineNum]

                if errorCol < len(errorLine) - 1: # Checks if the column is within the length of the line.
                    errorPart = errorLine[errorCol:].strip()
                    self.highlighter._underlineErrorsFrom(errorLineNum, errorCol, errorPart, filePath)
                else: #Column exceeds line length - highlight whole line
                    self.highlighter._underlineWhole(errorLineNum, 0, len(errorLine), filePath) 
            
    def handleSyntaxErrorJava(self, errorLine,filePath):
        # Match line and column numbers, and the error message
        match = re.match(r'.+\.java:(\d+): error: (.+)', errorLine)
        if match:
            errorLineNum = int(match.group(1)) - 1  # Changes starting at 1 to 0
            errorMsg = match.group(2).strip()

            lineLength = len(errorLine)
             
            #errorPart = self.extractProblematicPart(errorMsg)

            # Underline the error part in the editor
            self.highlighter._underlineWhole(errorLineNum, 0, lineLength, filePath)

    def extractProblematicPart(self, errorMsg):
        # Look for 'invalid syntax' or part of the message that is relevant
        if "invalid syntax" in errorMsg:
            return "invalid syntax"

        # If the message contains a problematic part in quotes, return that part
        match = re.search(r"'(.+)'", errorMsg)
        if match:
            return match.group(1)

        # Return part of the error message indicating the problematic symbol
        return errorMsg.split(' ')[-1]  # Return the last word in the error message
