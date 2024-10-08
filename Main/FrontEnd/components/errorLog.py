from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class ErrorLog(QWidget):
    def __init__(self, parent=None, errorLogToggle=None):
        super(ErrorLog, self).__init__(parent)
        self.setObjectName("ErrorLog")
        self.errorBox = QPlainTextEdit()
        self.errorBox.setObjectName("ErrorLog")
        self.errorBox.setReadOnly(True)
        self.setMinimumHeight(100)
        self.errorBox.setPlaceholderText("This is the error log. Any errors regarding file saving and compilation will show up here.")

        self.errorLabel = QLabel("Error Log")
        self.errorCount = 0
        self.errorLogToggle = errorLogToggle

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.errorLabel)
        self.layout.addWidget(self.errorBox)

        # Connect to the context menu event of errorBox
        self.errorBox.customContextMenuRequested.connect(self.contextMenu)
        self.errorBox.setContextMenuPolicy(Qt.CustomContextMenu)

    def add(self, msg: str):
        if (msg == 'clear'):
            self.clearLog()
        else: 
            self.errorBox.insertPlainText(f"{self.errorCount+1}: {msg}\n")
            self.errorCount += 1
            self.updateErrorCountDisplay()
            self.setVisible(True)

    def updateErrorCountDisplay(self):
        print(self.errorLogToggle)
        if self.errorLogToggle:
            self.errorLogToggle.setText(f"Errors ({self.errorCount})")
            
    def clearLog(self):
        self.errorBox.clear()
        self.errorCount = 0
        self.updateErrorCountDisplay()

    def contextMenu(self, position):
        contextMenu = self.errorBox.createStandardContextMenu()

        # Add custom actions to the context menu
        clearLogAction = QAction("Clear Error Log", self)
        clearLogAction.triggered.connect(self.clearLog)

        # Add custom actions at the bottom of the default menu
        contextMenu.addSeparator()  # Optional: Adds a separator
        contextMenu.addAction(clearLogAction)

        # Show the menu at the requested position
        contextMenu.exec_(self.errorBox.mapToGlobal(position))