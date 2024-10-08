from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qsci import *
from PyQt5.QtGui import *
from FrontEnd.frontEndApi import FrontEndApi
import os

class ProjectSelectionWindow(QWidget):
    def __init__(self, api, projects,_returnMethod, _deleteMethod):
        super().__init__()
        self.api: FrontEndApi = api
        self.returnMethod = _returnMethod
        self.deleteMethod = _deleteMethod
        self.setWindowTitle("Load Projects")
        self.setGeometry(400, 400, 400, 400)
        self.setObjectName("SelectionWindow")
        layout = QVBoxLayout()
        
        #Load default theme
        themePath = Path(__file__).parent.parent / "resources/styles/dark.qss"
        
        with themePath.open("r") as f:
                    styleSheet = f.read()
                    self.setStyleSheet(styleSheet)

        # add "NEW PROJECT" button with custom appearance
        newProjectButton = QPushButton("NEW PROJECT")
        newProjectButton.setFont(QFont("Arial", 12, QFont.Bold))
        newProjectButton.setStyleSheet("color: #FF6A6A;")
        newProjectButton.clicked.connect(self.onClickNewProject)
        layout.addWidget(newProjectButton)

        # add other project buttons, should be retrieved from backend 
        # projects = api.ProjectThreadController.getProjects()
        for project in projects:
            projectLayout = QHBoxLayout()
            projectButton = QPushButton(str(os.path.basename(project)))
            projectButton.setFont(QFont("Arial", 12))
            projectButton.clicked.connect(lambda checked, p=project: self.onClickSelectedProject(p))

            deleteButton = QPushButton("X")
            deleteButton.setStyleSheet("color: #FF6A6A;")
            deleteButton.setFont(QFont("Arial", 12))
            deleteButton.clicked.connect(lambda delete, p= project,b1 = projectButton, b2=deleteButton, : self.deleteProject(p,b1,b2))

            projectLayout.addWidget(projectButton, stretch= 9)
            projectLayout.addWidget(deleteButton, stretch=1)

            layout.addLayout(projectLayout)
        
        layout.addItem(QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)
        self.centre()
    
    def onClickNewProject(self):
        self.returnMethod(0)
        self.close()
        
    def onClickSelectedProject(self, project):
        self.returnMethod(project)
        self.close()

    #method to centre window in the screen
    def centre(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def deleteProject(self, project, button1, button2):
        reply = QMessageBox.question(self, "Project Deletion", "Are you sure you want to delete this project?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            button1.deleteLater()
            button2.deleteLater()
            response = self.deleteMethod(project)
            print(response)