import pytest
import os
import sys, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from Main.ProjectHandler.projectHandler import *
from queue import Queue

class TempGameInfo():
    def __init__(self, inGameName, inGamePath, inWriteFiles, inReadFiles):
        self.gameName = inGameName
        self.gamePath = inGamePath
        self.writeFiles = inWriteFiles
        self.readFiles = inReadFiles

    def getGamePath(self):
        return self.gamePath

def test_project_info_creation_and_getters():
    #Create a GameInfo object (locally created for test purposes)
    gameinfo = TempGameInfo("TestGame", "2024-11-twin-pac-man/Main/Plugins/pythonPacman", "These are write files", "These are read files")
    #Create a ProjectInfo object
    project_info_test = ProjectInfo("TestProjectName", "../main/ProjectHandler/SavedProjects/" + "TestProjectName", gameinfo)

    #assert if it was successfully created
    assert project_info_test.projectName == "TestProjectName"
    assert project_info_test.projectPath == "../main/ProjectHandler/SavedProjects/TestProjectName"
    assert project_info_test.gameInfo == gameinfo

    #assert if the getters work
    assert project_info_test.getProjectInfoName() == "TestProjectName"  
    assert project_info_test.getProjectInfoPath() == "../main/ProjectHandler/SavedProjects/TestProjectName"
    assert project_info_test.getProjectInfoGameInfo() == gameinfo

def test_project_handler_load_project():
    script_dir = Path(__file__).resolve().parent
    script_dir = str(script_dir)
    script_dir = script_dir + "/SavedProjects/"

    listOfFiles = ProjectHandlerAPI.getProjects(ProjectHandlerAPI, script_dir)
    print(listOfFiles)
    assert listOfFiles[0].name == "Project1"
    assert listOfFiles[1].name == "Project2"

    assert ProjectHandler.getCurrentProject() == ProjectInfo
    
    ProjectOne = ProjectHandlerAPI.getProjectsInfo(ProjectHandlerAPI, listOfFiles[0])
    assert ProjectOne == "Project loading Successful."
    assert ProjectHandler.getCurrentProject().getProjectInfoName() == "Project1"
    assert ProjectHandler.getCurrentProject().getProjectInfoName() != "Project2"

    ProjectTwo = ProjectHandlerAPI.getProjectsInfo(ProjectHandlerAPI, listOfFiles[1])
    assert ProjectTwo == "Project loading Successful."
    assert ProjectHandler.getCurrentProject().getProjectInfoName() == "Project2"
    assert ProjectHandler.getCurrentProject().getProjectInfoName() != "Project1"

def test_project_handler_create_new_project():
   
   script_dir = Path(__file__).resolve().parent
   script_dir = str(script_dir.parent.parent)

   gameinfo = TempGameInfo("helloworld.py", script_dir + "/Test/ProjectHandler/SavedProjects/pythonExample", "These are write files", "These are read files")
   message = ProjectHandlerAPI.newGameProject(ProjectHandlerAPI, gameinfo, "Project3", script_dir + "/Test/ProjectHandler/SavedProjects")
   assert message == "Successfully set project."
   assert ProjectHandler.getCurrentProject().getProjectInfoName() == "Project3"

   expectedProject = ProjectInfo("Project3", Path(script_dir + "/Test/ProjectHandler/SavedProjects/Project3"), gameinfo)
   createdProject = ProjectHandler.getCurrentProject()
   assert expectedProject.getProjectInfoGameInfo() == createdProject.getProjectInfoGameInfo()
   assert expectedProject.getProjectInfoName() == createdProject.getProjectInfoName()
   assert expectedProject.getProjectInfoPath() == createdProject.getProjectInfoPath()
   shutil.rmtree(createdProject.getProjectInfoPath())   #Delete created project after tests passed

def test_project_handler_save_files():
    script_dir = Path(__file__).resolve().parent
    script_dir = str(script_dir.parent.parent)

    #Creating file paths and file contents to be save within our system
    listOfFiles =  {
        script_dir+"/Test/ProjectHandler/SavingFilesTest/File1.txt": "Saving This text",
        script_dir+"/Test/ProjectHandler/SavingFilesTest/File2.txt": "Change this and see if its different",
    }

    #Save these files and check that they now exist with the correct contents
    ProjectHandler.saveProject(ProjectHandler, listOfFiles)
    with open(script_dir+"/Test/ProjectHandler/SavingFilesTest/File1.txt") as f1: s1 = f1.read()
    with open(script_dir+"/Test/ProjectHandler/SavingFilesTest/File2.txt") as f2: s2 = f2.read()
    assert s1 == listOfFiles.get(script_dir+"/Test/ProjectHandler/SavingFilesTest/File1.txt")
    assert s2 == listOfFiles.get(script_dir+"/Test/ProjectHandler/SavingFilesTest/File2.txt")

    #Now the same file paths but with different content
    listOfFiles =  {
        script_dir+"/Test/ProjectHandler/SavingFilesTest/File1.txt": "",
        script_dir+"/Test/ProjectHandler/SavingFilesTest/File2.txt": "",
    }

    #assess that the file have been saved and that the contents is what we expect
    ProjectHandler.saveProject(ProjectHandler, listOfFiles)
    with open(script_dir+"/Test/ProjectHandler/SavingFilesTest/File1.txt") as f1: s1 = f1.read()
    with open(script_dir+"/Test/ProjectHandler/SavingFilesTest/File2.txt") as f2: s2 = f2.read()
    assert s1 == listOfFiles.get(script_dir+"/Test/ProjectHandler/SavingFilesTest/File1.txt")
    assert s2 == listOfFiles.get(script_dir+"/Test/ProjectHandler/SavingFilesTest/File2.txt")

def test_Compile():
    def decompileJava():  # Removes class files to ensure recompilation
        paths_to_remove = [
            "Test/ProjectHandler/SavedProjects/javaExample/helloworld.class",
            "Test/ProjectHandler/SavedProjects/javaExample/helloworld2.class",
            "Test/ProjectHandler/SavedProjects/javaExample/JavaExampleINside/helloworld3.class"
        ]
        for path in paths_to_remove:
            if Path(path).exists():
                os.remove(path)

    decompileJava()
    # Ensure no class files exist before compilation
    assert not Path("Test/ProjectHandler/SavedProjects/javaExample/helloworld.class").exists()
    assert not Path("Test/ProjectHandler/SavedProjects/javaExample/helloworld2.class").exists()
    assert not Path("Test/ProjectHandler/SavedProjects/javaExample/JavaExampleINside/helloworld3.class").exists()
    
    projectInfoJava = ProjectInfo("MyProject", "Test/ProjectHandler/SavedProjects/javaExample", GameInfo('', 'helloworld.java', "./Main/Plugins/pythonPacman", 'All', 'All'))
    ProjectHandler.setCurrentProject(projectInfoJava)
    ProjectHandler.Compile()
    
    
    # Check that class files have been created
    assert Path("Test/ProjectHandler/SavedProjects/javaExample/helloworld.class").exists()
    assert Path("Test/ProjectHandler/SavedProjects/javaExample/helloworld2.class").exists()
    assert Path("Test/ProjectHandler/SavedProjects/javaExample/JavaExampleINside/helloworld3.class").exists()

    # Decompile Java to clean up files
    decompileJava()

    # Ensure no class files exist after decompilation
    assert not Path("Test/ProjectHandler/SavedProjects/javaExample/helloworld.class").exists()
    assert not Path("Test/ProjectHandler/SavedProjects/javaExample/helloworld2.class").exists()
    assert not Path("Test/ProjectHandler/SavedProjects/javaExample/JavaExampleINside/helloworld3.class").exists()

def test_Run(monkeypatch, capsys):
    mockSystemCall = []

    def decompileJava():  # Removes class files to ensure recompilation
            paths_to_remove = [
                "Test/ProjectHandler/SavedProjects/javaExample/helloworld.class",
                "Test/ProjectHandler/SavedProjects/javaExample/helloworld2.class",
                "Test/ProjectHandler/SavedProjects/javaExample/JavaExampleINside/helloworld3.class"
            ]
            for path in paths_to_remove:
                if Path(path).exists():
                    os.remove(path)
                    
    decompileJava()
    
    outputQueue = Queue()
    
    def captureOutput(stdoutLine, *args, **kwargs):
        outputQueue.put(stdoutLine)
        
    monkeypatch.setattr("builtins.print", captureOutput)
    
    # Set Python project and run
    projectInfoPython = ProjectInfo("MyProject", "Test/ProjectHandler/SavedProjects/pythonExample", GameInfo('', 'helloworld.py', "./Main/Plugins/pythonPacman", 'All', 'All'))
    ProjectHandler.setCurrentProject(projectInfoPython)
    ProjectHandler.Run('')

    time.sleep(1)

    output = []
    while not outputQueue.empty():
        output.append(outputQueue.get())
    
    assert "Hello Python World\n" in "".join(output)

    # Set Java project and run
    projectInfoJava = ProjectInfo("MyProject", "Test/ProjectHandler/SavedProjects/javaExample", GameInfo('', 'helloworld.java', "./Main/Plugins/pythonPacman", 'All', 'All'))
    ProjectHandler.setCurrentProject(projectInfoJava)
    ProjectHandler.Run('')
    
    time.sleep(1)
    
    output = []
    while not outputQueue.empty():
        output.append(outputQueue.get())
    
    assert "Hello Java World\n" in "".join(output)

    # Run the inner Java project inside the directory
    result = subprocess.run(["java", "Test/ProjectHandler/SavedProjects/javaExample/JavaExampleINside/helloworld3.java"],
        capture_output=True,
        text=True
    )
    assert "Hello Java World3\n" in result.stdout
    
    decompileJava()