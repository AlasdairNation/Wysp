import pytest
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from Main.GameHandler.gameHandlerAPI import gameHandlerAPI
from Main.GameHandler.gameInfo import GameInfo

@pytest.fixture
def game_info():
    return GameInfo(projectFiles={}, gameName="testGame", gamePath="/test/path", writeFiles=["testWrite"], readFiles=["testRead"])

def testInitilise(game_info):
    assert game_info.gameName == "testGame"
    assert game_info.gamePath == "/test/path"
    assert game_info.writeFiles == ["testWrite"]
    assert game_info.readFiles == ["testRead"]

    assert game_info.gameName != "notTestGame"
    assert game_info.gamePath != "not/test/path"
    assert game_info.writeFiles != ["notTestWrite"]
    assert game_info.readFiles != ["notTestRead"]

def testSettersGetters(game_info):
    game_info.setGameName("testGame2")
    assert game_info.getGameName() == "testGame2"
    game_info.setGameName("testGame3")
    assert game_info.getGameName() != "testGame2"
    assert game_info.getGameName() == "testGame3"

    game_info.setGamePath("/new/test/path")
    assert game_info.getGamePath() == "/new/test/path"
    game_info.setGamePath("new/new/test/path")
    assert game_info.getGamePath() != "/new/test/path"
    assert game_info.getGamePath() == "new/new/test/path"

    game_info.setWriteFile(["newTestWrite"])
    assert game_info.getWriteFile() == ["newTestWrite"]
    game_info.setWriteFile(["newNewTestWrite"])
    assert game_info.getWriteFile() != ["newTestWrite"]
    assert game_info.getWriteFile() == ["newNewTestWrite"]

    game_info.setReadFiles(["newTestRead"])
    assert game_info.getReadFiles() == ["newTestRead"]
    game_info.setReadFiles(["newNewTestRead"])
    assert game_info.getReadFiles() != ["newTestRead"]
    assert game_info.getReadFiles() == ["newNewTestRead"]

    game_info.setProjectFiles({"dir": ["file1", "file2"]})
    assert game_info.getProjectFiles() == {"dir": ["file1", "file2"]}
    game_info.setProjectFiles({"dir": ["file1", "file2", "file3"]})
    assert game_info.getProjectFiles() != {"dir": ["file1", "file2"]}
    assert game_info.getProjectFiles() == {"dir": ["file1", "file2", "file3"]}