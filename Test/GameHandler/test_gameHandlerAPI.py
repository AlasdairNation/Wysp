import sys
import os
import pytest
import importlib.util
from pathlib import Path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from Main.GameHandler.gameHandlerAPI import gameHandlerAPI
from Main.GameHandler.gameInfo import GameInfo
from Main.GameHandler.plugin_interface import plugin_interface


@pytest.fixture
def gameHandler():
    return gameHandlerAPI()

# The following testGetGame test function was created with the help of
# chatgpt. The original mockwalk that I tried creating was not working and
# through research and prompting chatpgt with errors, I ended up with the following 
# test harness. I have made minor adjustments as such I do not take ownership of this code.
def testGetGame(monkeypatch, gameHandler):
    def mock_os_walk(directory):
        return iter([("/test/Plugins", ["Game1", "Game2"], [])])

    class MockLoader:
        def create_module(self, spec):
            return None
        def exec_module(self, module):
            module.GetInfo = MockGetInfo

    class MockGetInfo(plugin_interface):
        def __init__(self, gameName="MockedGame", gamePath="MockedPath", fileName="MockedFileName"):
            # Call the __init__ method of the parent class with the required arguments
            super().__init__(gameName=gameName, gamePath=gamePath, fileName=fileName)

        def fileName(self):
            return self._fileName

        def fileName(self, newName):
            self._fileName = newName

        def getGamePath(self):
            return "MockedPath"

        def getGameName(self):
            return "MockedGame.py"

        def getWriteFiles(self):
            return ["MockedWriteFiles"]

        def getReadFiles(self):
            return ["MockedReadFiles"]

        def getInfo(self):
            return self  # Assuming getInfo should return the instance

        def run(self):
            pass  # Mock implementation, no operation needed

        # Implementing the abstract methods from plugin_interface
        def gameName(self):
            return "MockedGame"

        def gamePath(self):
            return "MockedPath"

        def projectFiles(self):
            return ["MockedProjectFiles"]

    def mock_spec_from_file_location(name, path):
        mock_spec = type("MockSpec", (), {
            "loader": MockLoader(),
            "name": name,
            "origin": str(path),
            "submodule_search_locations": [],
            "has_location": True,
            "cached": None,
            "parent": None,
            "has_location": True
        })
        return mock_spec

    def mock_exists(path):
        return True

    monkeypatch.setattr(os, "walk", mock_os_walk)
    monkeypatch.setattr(importlib.util, "spec_from_file_location", mock_spec_from_file_location)
    monkeypatch.setattr(Path, "exists", mock_exists)

    script_dir = Path(__file__).resolve().parent
    result = gameHandler.getGames(script_dir)

    assert len(result) == 2
    assert len(result) == len(gameHandler.getGames(script_dir))
    
    assert result[0].getGameName() == "MockedGame.py"
    assert result[0].getGameName() != "notMockedGame.py"

def testSetGame(gameHandler):
    gameHandler.gameList = [
        GameInfo("mockProjectFiles1", "mock1.py", "mocked/path/1", "mockWriteFiles1", "mockedReadFiles1"),
        GameInfo("mockProjectFiles1", "mock2.py", "mocked/path/2", "mockWriteFiles2", "mockedReadFiles2")
    ]
    gameHandler.setGame(0)
    assert gameHandler.currentGame == gameHandler.gameList[0]
