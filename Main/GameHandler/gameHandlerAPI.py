import importlib.util
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from Main.GameHandler.gameInfo import GameInfo
from Main.GameHandler.plugin_interface import plugin_interface

class gameHandlerAPI:
    def __init__(self):
        self.gameList = []  # Contains the list of games using gameInfo.
        self.currentGame = GameInfo #List which the current game is.
        self.totalGames = 0  # Total number of games in the plugin folder.

    # Function to get the information about each games and save it to a new list which the gameHandlerAPI then stores
    def getGames(self, dir=''):
        gameInfoList = []
        pluginsPath = Path('')
        try:
            if dir == '':
                script_dir = Path(__file__).resolve().parent
                pluginsPath = script_dir.parent / "Plugins"
                if not pluginsPath.exists():
                    print("Plugins directory does not exist.")
                    return gameInfoList
            else:
                pluginsPath = Path(dir)
            
            for game in next(os.walk(pluginsPath))[1]:
                if (game != "__pycache__"):
                    getInfoPath = pluginsPath / game / "getInfo.py"

                    if getInfoPath.exists():
                        spec = importlib.util.spec_from_file_location("getInfo", getInfoPath)
                        getInfoModule = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(getInfoModule)

                        plugin_class_name = "GetInfo"
                        if hasattr(getInfoModule, plugin_class_name):
                            plugin_class = getattr(getInfoModule, plugin_class_name)
            
                            if issubclass(plugin_class, plugin_interface):
                                plugin_instance = plugin_class()

                                game_info = plugin_instance.getInfo()

                                try:
                                    plugin_instance.run()
                                    gameInfoList.append(game_info)
                                except Exception as e:
                                    print(f"Error running {plugin_class_name}: {e}")
                            else:
                                print(f"Error: {plugin_class_name} does not implement plugin_interface.")
                        else:
                            print(f"Error: Class {plugin_class_name} not found in {getInfoPath}")
                    else:
                        print(f"getInfo.py not found in {getInfoPath}")

        except Exception as e:
            print(f"Error: {str(e)}")

        self.gameList = gameInfoList
        return gameInfoList


    # Function to set the game to the users choice/
    def setGame(self, gameChoice):
        self.currentGame = self.gameList[gameChoice]
        return self.gameList[gameChoice]