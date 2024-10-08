import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QPixmap
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ProjectHandler.projectHandler import *
class RunCluster(QWidget):
    def __init__(self, parent=None, projectThreadController=None):
        super().__init__(parent)
        self.initUI(parent)
        self.parent = parent
        global projectMaster
        projectMaster = projectThreadController

    def initUI(self, parent):
        self.toolbar = self.initToolBar(parent)

        runClusterLayout = QVBoxLayout()
        runClusterLayout.addWidget(self.toolbar)
        self.setLayout(runClusterLayout)

    def initToolBar(self, parent):
        toolbar = QToolBar()
        # Container widget for the toolbar, layouts cannot be added to the toolbar directly
        containerWidget = QWidget()
        horizontalLayout = QHBoxLayout()

        # Define the base path (two levels up from the current file)
        basePath = Path(__file__).parent.parent
        
        # Append the relative path to the icon file
        iconPath = basePath / 'resources' / 'icons' / 'playButton.svg'

        runButton = QPushButton(parent)
        runButton.setToolTip("Run Game")
        runButton.setIcon(QIcon(str(iconPath)))
        runButton.setIconSize(QSize(32, 32))

        textEdit = QLineEdit(parent)
        textEdit.setPlaceholderText("-params -mazesize 3 - pacman game run")
        
        horizontalLayout.addWidget(runButton)
        horizontalLayout.addWidget(textEdit)

        # cotainer widget stores the layout in place of the toolbar, because toolbars can't have layout
        containerWidget.setLayout(horizontalLayout)

        runButton.clicked.connect(lambda: self.onClickedRunButton(textEdit.text()))
        toolbar.addWidget(containerWidget)
        return toolbar
        
    def onClickedRunButton(self, parameters):
        if not parameters:
            parameters = ""
            print("Running with default parametres...")
        else:
            print("Running with the following parametres: (", parameters + ")")

        global projectMaster
        
        self.parent.saveProject()
        projectMaster.requestRun(parameters)