# # Tests the Core
# # Methods to test
# # - run()
# # - chooseProject()
# # - startEditor()
# # - endProgram()

# # Behaviours to Test:
# # 1. Initializing the thread handlers:
# #   - Each handler is initialized with it's relevant handler
# # 2.Choosing the project:
# #   - Boots project selection screen
# #   - Returned choice results in:
# #       - VALID CHOICE "load": running editor
# #       - VALID CHOICE "new": Loads game selection window
# #       - VALID CHOICE "exit": ends program
# #       - INVALID CHOICE: display error, reboot project selection screen
# # 3.Choosing the Game:
# #   - Boots 
# # 4.Running the Editor:
# #   - Boots main window with reference to game & project handler   
# #   - returned choice results in:
# #       - VALID CHOICE "choose": runs project selection screen
# #       - VALID CHOICE "new": runs game selection screen
# #       - VALID CHOICE "exit": ends program
# #       - INVALID CHOICE: ends program
# # 5.Ending the Program:
# #   - calls endThread() on all three threadcontrollers and finishes
# #
# # Paths to Test for full prime path coverage: (See prime path diagram in report)
# #   - [1,2,5] :Path 1 (Exit on project)
# #   - [1,2,3,5] :Path 2 (Exit on Game)
# #   - [1,2,4,5] :Path 3 (Exit on Editor)
# #   - [1,2,4,2,3,4,5] :Path 4 (Loop Tester)


# import os
# import sys
# import pytest
# from unittest.mock import MagicMock
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# from Main.CentralFramework.gameThreadController import gameThreadController
# from Main.CentralFramework.guiThreadController import guiThreadController
# from Main.CentralFramework.projectThreadController import ProjectThreadController
# from Main.CentralFramework.centralFramework import Core 

# from Main.ProjectHandler.projectHandler import ProjectHandlerAPI
# from Main.FrontEnd.frontEndApi import FrontEndApi
# from Main.GameHandler.gameHandlerAPI import gameHandlerAPI

# @pytest.fixture
# def guiMaster():
#     return guiThreadController(FrontEndApi())

# @pytest.fixture
# def gameMaster():
#     return gameThreadController(gameHandlerAPI())

# @pytest.fixture
# def projectMaster():
#     return ProjectThreadController(ProjectHandlerAPI())

# def runCore(gameMaster,guiMaster,projectMaster):
#     tester = Core(gameMaster,guiMaster,projectMaster)
#     tester.run()
#     return tester
   

# def test_path1(guiMaster, gameMaster, projectMaster): # exit on project selection [1,2,5]
#     success = True

#     guiMaster.projectSelectionScreen = MagicMock(return_value = None)
#     gameMaster.getGames = MagicMock(return_value = None)
#     projectMaster.getProjects = MagicMock(return_value = None)
#     guiMaster.closeThread = MagicMock(return_value = None) 
#     guiMaster.gameSelectionScreen = MagicMock(return_value = None) 
#     projectMaster.setProject = MagicMock(return_value = None)
    
#     core = runCore(gameMaster,guiMaster,projectMaster)

#     try:
#         #Ensures path 1-2-5 taken
#         guiMaster.projectSelectionScreen.assert_called_once() #Checks reached [2]
#         guiMaster.gameSelectionScreen.assert_not_called() # Checks not reached [3]
#         projectMaster.setProject.assert_not_called() # Checks not reaching for [4]
#         guiMaster.closeThread.assert_called_once() #Checks reached [5]
#     except AssertionError as e:
#         success = False
#         print(e)

#     assert success
    

# def test_path2(guiMaster, gameMaster, projectMaster): # exit on game selection [1,2,3,5]
#     success = True

#     guiMaster.projectSelectionScreen = MagicMock(return_value = 0)
#     gameMaster.getGames = MagicMock(return_value = None)
#     projectMaster.getProjects = MagicMock(return_value = None)
#     projectMaster.newGameProject = MagicMock(return_value = None)
#     guiMaster.closeThread = MagicMock(return_value = None) 
#     guiMaster.gameSelectionScreen = MagicMock(return_value = None) 
#     projectMaster.setProject = MagicMock(return_value = None)

#     runCore(gameMaster,guiMaster,projectMaster)

#     try:
#         guiMaster.projectSelectionScreen.assert_called_once() #Checks reached [2]
#         guiMaster.gameSelectionScreen.assert_called_once() # Checks reached [3]
#         projectMaster.newGameProject.assert_not_called() # Checks not reaching for [4]
#         projectMaster.setProject.assert_not_called() # Checks not reaching for [4]
#         guiMaster.closeThread.assert_called_once() # checks closure [5]
#     except AssertionError as e:
#         success = False
#         print(e)

#     assert success

# def test_path3(guiMaster, gameMaster, projectMaster): # exit on loaded project editor [1,2,4,5]
#     success = True

#     guiMaster.projectSelectionScreen = MagicMock(return_value = 1)
#     guiMaster.codeScreen = MagicMock(return_value = True)
#     gameMaster.getGames = MagicMock(return_value = None)
#     projectMaster.getProjects = MagicMock(return_value = None)
#     guiMaster.closeThread = MagicMock(return_value = None) 
#     projectMaster.setProject = MagicMock(return_value = None)
    
#     runCore(gameMaster,guiMaster,projectMaster)

#     try:
#         guiMaster.projectSelectionScreen.assert_called_once() #Checks reached [2]
#         projectMaster.setProject.assert_called_once() # Checks reaching for [4], skipping over [3]
#         guiMaster.codeScreen.assert_called_once() # Checks reached [4]
#         guiMaster.closeThread.assert_called_once() # checks closure [5]
#     except AssertionError as e:
#         success = False
#         print(e)

#     assert success

# def test_path4(guiMaster, gameMaster, projectMaster): # Loop Tester [1,2,4,2,3,4,5] choose project - start editor, load project - choose game - start editor - close program
#     success = True

#     guiMaster.projectSelectionScreen = MagicMock()
#     guiMaster.projectSelectionScreen.side_effect = [1,0]
#     guiMaster.codeScreen = MagicMock()
#     guiMaster.codeScreen.side_effect = [False,True]
    
#     guiMaster.gameSelectionScreen = MagicMock(return_value = 1)
#     gameMaster.getGames = MagicMock(return_value = None)
#     projectMaster.getProjects = MagicMock(return_value = None)
#     projectMaster.newGameProject = MagicMock(return_value = None)
#     guiMaster.closeThread = MagicMock(return_value = None) 
#     projectMaster.setProject = MagicMock(return_value = None)
    
#     runCore(gameMaster,guiMaster,projectMaster)

#     try:
#         guiMaster.projectSelectionScreen.assert_called() #Checks reached [2]
#         projectMaster.setProject.assert_called_once() # Checks [2]-[4] path taken once
#         guiMaster.gameSelectionScreen.assert_called_once() # Checks [2]-[3]-[4] path taken once
#         guiMaster.codeScreen.assert_called() # Checks reached [4]
#         guiMaster.closeThread.assert_called_once() # checks closure [5] (once)
#     except AssertionError as e:
#         success = False
#         print(e)

#     assert success
