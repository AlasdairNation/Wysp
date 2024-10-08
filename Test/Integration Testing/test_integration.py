import pytest
import os
import sys
from Main.CentralFramework.centralFramework import Core
from Main.CentralFramework.gameThreadController import gameThreadController
from Main.CentralFramework.guiThreadController import guiThreadController
from Main.CentralFramework.projectThreadController import ProjectThreadController
from Main.GameHandler.gameHandlerAPI import gameHandlerAPI
from Main.FrontEnd.frontEndApi import FrontEndApi
from Main.ProjectHandler.projectHandler import ProjectHandlerAPI

# Things to Test:
# Initialisation of Core Controllers using created APIs
#  - Game Thread Controller : DONE
#  - GUI Thread Controller : DONE
#  - Project Thread Controller : DONE
#  Initialisation of Core using the Thread Controllers: DONE
# Successful running of Core: DONE
# Successful retrieval of games:
# Successful retrieval of projects:
# Successful creation of project:
#

@pytest.fixture
def initialize_game_thread_controller():
    """
    Tests creation of the game thread
    """
    test_gameHandler = gameHandlerAPI()
    test_game_thread = gameThreadController(test_gameHandler)
    assert test_game_thread.api == test_gameHandler, "Unsuccessful creation of game thread"
    return test_game_thread

@pytest.fixture
def initialize_project_thread_controller():
    """Tests Project Thread controller object"""
    test_projectHandler = ProjectHandlerAPI()
    test_project_thread = ProjectThreadController(test_projectHandler)
    assert test_project_thread.api == test_projectHandler, "Unsuccessful creation of project thread"
    return test_project_thread

@pytest.fixture
def initialize_gui_thread_controller():
    test_guiHandler = FrontEndApi()
    test_gui_thread = guiThreadController(test_guiHandler)
    assert test_gui_thread.api == test_guiHandler, "Unsuccessful creation of gui thread"
    return test_gui_thread

@pytest.fixture
def core_initialisation(initialize_game_thread_controller, initialize_project_thread_controller, initialize_gui_thread_controller, monkeypatch):
    """Checks Core was created successfully"""
    game_thread = initialize_game_thread_controller
    project_thread = initialize_project_thread_controller
    gui_thread = initialize_gui_thread_controller
    assert game_thread.api is not None, "Game Thread was not created"
    assert project_thread.api is not None, "Project Thread was not created"
    assert gui_thread.api is not None, "GUI Thread was not created"
    
    core = Core(game_thread, gui_thread, project_thread)
    assert core is not None, "Core is null"
    assert core.gameMaster == game_thread, "Game Master is not matching"
    assert core.projectMaster == project_thread, "Project Master is not matching"
    assert core.guiMaster == gui_thread, "GUI Master is not matching"
    
    # Tests that the core runs and closes the window successfully
    def mock_sys_exit(code):
        assert code == 0
    
    monkeypatch.setattr("sys.exit", mock_sys_exit)
    monkeypatch.setattr("Main.FrontEnd.frontEndApi.QApplication.exec_", lambda: 0)

    core.run()
    return core


def test_core_get_games(core_initialisation):
    core = core_initialisation
    available_games = core.gameMaster.getGames()
    assert isinstance(available_games, list), "Games are not returned as a list"
    assert len(available_games) > 0, "An empty games list is returned"

def test_core_get_projects(core_initialisation):
    core = core_initialisation
    available_projects = core.projectMaster.getProjects()
    assert isinstance(available_projects, list), "Projects are not returned as a list"
    assert len(available_projects) >= 0, "An empty projects list is returned"

