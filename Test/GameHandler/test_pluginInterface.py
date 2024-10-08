import os
import sys
import pytest
from unittest.mock import create_autospec
from Main.GameHandler.plugin_interface import plugin_interface

class test_gameInfo():
    def __init__(self, project_files, game_name, game_path, read_files, write_files):
        self.project_files = project_files
        self.game_name = game_name
        self.game_path = game_path
        self.read_files = read_files
        self.write_files = write_files
    

class test_plugin(plugin_interface):
    """
    Concrete Class Implementing Interface
    """
    
    def __init__(self, gameName, gamePath, fileName):
        super().__init__(gameName, gamePath, fileName)
        self._projectFiles = {}  # This now works because of the setter

    @property
    def gameName(self):
        return self._gameName

    @gameName.setter
    def gameName(self, newName):
        self._gameName = newName

    @property
    def gamePath(self):
        return self._gamePath

    @gamePath.setter
    def gamePath(self, newPath):
        self._gamePath = newPath

    @property
    def fileName(self):
        return self._fileName

    @fileName.setter
    def fileName(self, newName):
        self._fileName = newName

    @property
    def projectFiles(self):
        return self._projectFiles

    # Future plugins have to implement the following methods
    def getInfo(self) -> test_gameInfo:
        """Method retrieves plugin info such as the project files, the game name, the game path, 
        its write files, and its read files."""

        project_files = {
            "folder1": {
                "subfolder1": ["file1.txt", "file2.txt"]
            }
        }

        game_name = self.gameName
        game_path = self.gamePath  # This should return the correct game path
        read_files = ["important.txt", "default.txt"]
        write_files = ["algorithm.py", "sort.py"]

        game_info = test_gameInfo(project_files, game_name, game_path, read_files, write_files)
        return game_info
    
    def someMethod(self):
        return True
    
    def run(self):
        """Method runs the plugin"""
        return self.someMethod() 

        

def test_Initialize():
    """
    Testing Initialize Function
    """
    testPlugin = test_plugin("test.py", "../Plugins/Test/test.py", "Test")
    assert testPlugin.gameName != "", "Plugin Name should not be blank!"
    assert testPlugin.gameName == "test.py", "Name is not matching"
    
    assert testPlugin._fileName != "", "Plugin filename is blank!"
    assert testPlugin._fileName == "Test", "filename is not matching"    

    assert testPlugin._gamePath != "", "Plugin filepath is blank!"
    assert testPlugin._gamePath == "../Plugins/Test/test.py", "filepath is not matching"
    
def test_getInfo():
    """
    Testing getInfo function
    """
    getInfoTestPlugin = test_plugin("GetInfo", "../Plugins/GetInfo/get_info.py", "get_info.py")
    
    # Use properties instead of protected attributes
    assert getInfoTestPlugin.gameName != "", "Plugin Name should not be blank!"
    assert getInfoTestPlugin.gameName == "GetInfo", "Name is not matching"
    
    assert getInfoTestPlugin._fileName != "", "Plugin filename is blank!"
    assert getInfoTestPlugin._fileName == "get_info.py", "filename is not matching"
    
    assert getInfoTestPlugin._gamePath != "", "Plugin filepath is blank!"
    assert getInfoTestPlugin._gamePath == "../Plugins/GetInfo/get_info.py", "filepath is not matching"
    
    # Now get the plugin info and assert its structure
    plugin_info = getInfoTestPlugin.getInfo()
    
    assert plugin_info is not None, "getInfo() returned None"
    test_structure = {
        "folder1": {
            "subfolder1": ["file1.txt", "file2.txt"]
        }
    }
    assert plugin_info.project_files != {}, "Structure is empty"
    assert plugin_info.project_files == test_structure, "Structure does not match"
    
    assert plugin_info.game_name != "", "Game name is blank!"
    assert plugin_info.game_name == "GetInfo", "Game name does not match"

    assert plugin_info.game_path != "", "Game path is blank!"
    assert plugin_info.game_path == "../Plugins/GetInfo/get_info.py"
    
    assert plugin_info.read_files != [], "Read files are blank!"
    assert plugin_info.read_files == ["important.txt", "default.txt"]
    
    assert plugin_info.write_files != [], "Write files are blank!"
    assert plugin_info.write_files == ["algorithm.py", "sort.py"]

def test_runMethod():
    """
    Testing run method
    """
    runPlugin = test_plugin("Run", "../Plugins/Run/run.py", "run.py")

    assert runPlugin.gameName != "", "Plugin Name should not be blank!"
    assert runPlugin.gameName == "Run", "Name is not matching"
    
    assert runPlugin._fileName != "", "Plugin filename is blank!"
    assert runPlugin._fileName == "run.py", "filename is not matching"    

    assert runPlugin._gamePath != "", "Plugin filepath is blank!"
    assert runPlugin._gamePath == "../Plugins/Run/run.py", "filepath is not matching"

    assert runPlugin.run() == True, "Run method is not working!"
    