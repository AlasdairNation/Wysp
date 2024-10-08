import pytest
import os
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))     # Importing modules does not work without it.
from Main.Plugins.javaPacman.getInfo import GetInfo


@pytest.fixture
def getInfo():
    return GetInfo()

def testGetGameName(getInfo):
    assert getInfo.gameName == 'pacman.java'  # Access as an attribute
    assert getInfo.gameName != 'pacman.py'

def testGetWriteFiles(getInfo):
    assert getInfo.writeFiles == ['search.java', 'searchAgents.java']  # Access as an attribute
    assert getInfo.writeFiles != ['search.py', 'searchAgents.py']

def testGetReadFiles(getInfo):
    assert getInfo.readFiles == ['All']  # Access as an attribute
    assert getInfo.readFiles != ['None']

def testGetGamePath(getInfo):
    with patch('pathlib.Path.resolve') as mock_resolve:
        mock_resolve.return_value = Path('/mocked/path/game.py')
        gamePath = getInfo.gamePath  # Access as an attribute
        
        # The file will get the parent of the file it is in so it should not return game.py
        assert gamePath == '/mocked/path' 
        assert gamePath != '/mocked/path/game.py'
        assert gamePath != '/mocked'
        mock_resolve.assert_called_once()