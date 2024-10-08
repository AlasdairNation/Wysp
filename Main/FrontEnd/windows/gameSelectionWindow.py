from pathlib import Path
import re
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qsci import *
from PyQt5.QtGui import *
from FrontEnd.windows.projectSelectionWindow import ProjectSelectionWindow
# from FrontEnd.windows.mainWindow import MainWindow
class GameSelectionWindow(QWidget):
    def __init__(self, api, games, projects, _returnMethod):
        super().__init__()
        self.api = api
        self._returnMethod = _returnMethod
        self.setWindowTitle("Game Selection")
        self.setGeometry(400, 400, 400, 400)
        self.buttonGroup = QButtonGroup(self)
        self.projects = projects
        self.setObjectName("SelectionWindow")
        layout = QVBoxLayout()

        #Load default theme
        themePath = Path(__file__).parent.parent / "resources/styles/dark.qss"
        
        with themePath.open("r") as f:
                    styleSheet = f.read()
                    self.setStyleSheet(styleSheet)

        self.gameList = QListWidget()
        # games = api.gameThreadController.getGames()
        for game in games:
            gameButton = QRadioButton(game.getGameName())
            gameButton.setObjectName("SelectionWindow")
            # gameButton.setFont(QFont("Arial", 12))
            self.buttonGroup.addButton(gameButton)
            #gameButton.clicked.connect(lambda checked, g=game: self.onClickGameSelect(g))
            layout.addWidget(gameButton)

        layout.addItem(QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding))

        buttonLayout = QHBoxLayout()

        backButton = QPushButton("Back")
        # backButton.setFont(QFont("Arial", 12))
        backButton.clicked.connect(self.onBackButtonClicked)
        
        buttonLayout.addWidget(backButton)

        selectButton = QPushButton("Select")
        # selectButton.setFont(QFont("Arial", 12))
        selectButton.clicked.connect(lambda: self.onClickGameSelect(games))
        
        buttonLayout.addWidget(selectButton)

        layout.addLayout(buttonLayout)

        self.setLayout(layout)
        self.centre()

    def showDialog(self):
        while True:
            text, ok = QInputDialog.getText(self, 'Project Name', "Please enter a name for your new project")
            if ok and text:
                valid, errorMsg = self.isValidProjectName(text)
                if valid:
                    return text
                else:
                    QMessageBox.warning(self, "Invalid Project Name", errorMsg)
            elif not ok:
                return None

    def isValidProjectName(self, projectName):
        projectName = projectName.strip()
        if not re.match(r'^[\w-]+$', projectName):
            return False, "project name must only contain letters, numbers, hyphens, and underscores."
        
        windowsReservedNames = ["CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", 
                                "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"]

        if projectName.upper() in windowsReservedNames:
            return False, f"{projectName} \n can't be used as it is a windows reserved folder name"

        if len(projectName) > 255:
            return False, f"{projectName} \n is too long, please limit to 255 characters"

        for p in self.projects:
            if(str(os.path.basename(p)) == projectName):
                return False, f" {projectName} \n A project already exists with that name, try again"

        return True, None
        
    def onClickGameSelect(self, gameList):
        selectedButton = self.buttonGroup.checkedButton()
        if selectedButton:
            name = self.showDialog()
            if (name != None):
                self.setEnabled(False)
                g = self.retrieveGameInfo(gameList, selectedButton.text())
                self._returnMethod(g, name)
                self.close()

    def centre(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def onBackButtonClicked(self):
        self._returnMethod(0)
        self.close()

    def retrieveGameInfo(self, gameList, gameName):
        for gameInfo in gameList:
            if(gameName == gameInfo.getGameName()):
                return gameInfo
