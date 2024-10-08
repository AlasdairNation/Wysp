from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os
import re

class CustomLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setObjectName("Terminal")
        self.promptLength = 0

    def keyPressEvent(self, event):
        cursor_position = self.cursorPosition()
        # Prevent backspace before the prompt
        if event.key() == Qt.Key_Backspace and cursor_position <= self.promptLength:
            return
        super().keyPressEvent(event)

    def updatePromptLength(self, prompt):
        self.promptLength = len(prompt)

class Terminal(QWidget):
    def __init__(self, path, parent=None):
        super().__init__(parent)
        self.setObjectName("Terminal")

        self.currentDirectory = path
        os.chdir(self.currentDirectory)
        self.prompt = f"<font color='#4275f5'>{self.currentDirectory}$</font> "  # Create a prompt variable with color

        # Set up layout
        self.layout = QVBoxLayout(self)

        self.label = QLabel("Terminal")
        self.layout.addWidget(self.label)

        # Create read-only output area
        self.outputArea = QPlainTextEdit(self)
        self.outputArea.setObjectName("Terminal")
        self.outputArea.setReadOnly(True)
        self.layout.addWidget(self.outputArea)

        # Create input area using the CustomLineEdit
        self.inputArea = CustomLineEdit()
        self.inputArea.updatePromptLength(self.stripHTML(self.prompt))
        self.layout.addWidget(self.inputArea)

        # Set the initial prompt in the input area
        self.inputArea.setText(self.stripHTML(self.prompt))
        self.inputArea.setCursorPosition(len(self.stripHTML(self.prompt)))

        # Connect returnPressed signal
        self.inputArea.returnPressed.connect(self.takeInput)

        # Connect to the context menu event of outputArea
        self.outputArea.customContextMenuRequested.connect(self.contextMenu)
        self.outputArea.setContextMenuPolicy(Qt.CustomContextMenu)

        # Initialize QProcess
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.readOutput)
        self.process.readyReadStandardError.connect(self.readError)
        self.process.finished.connect(self.processFinished)

        self.is_ls_command = False

        # Flag to check if a process is running (interactive mode like python shell)
        self.isProcessRunning = False

    def takeInput(self):
        # Take input after the prompt
        command = self.inputArea.text()[len(self.stripHTML(self.prompt)):].strip()
        self.inputArea.clear()

        # If a process is running (like python shell), send input to the process
        if self.isProcessRunning:
            self.process.write(f"{command}\n".encode())
            self.appendOutput(command, isInput=True)
        else:
            if command:
                self.runCommand(command)

        # Reset the prompt in the input area after command
        self.inputArea.setText(self.stripHTML(self.prompt))
        self.inputArea.setCursorPosition(len(self.stripHTML(self.prompt)))

    def runCommand(self, command):
        self.appendOutput(f"{self.prompt}{command}\n")

        # Detect if the command is 'ls'
        self.is_ls_command = command.strip() == "ls"

        if command.strip() in ["python3", "python"]:
            # Display an error message if user tries to run Python shell
            self.appendOutput("Error: Interactive Python shells are not supported in this terminal.\n", isError=True)
            self.terminateProcess() # Terminate process attempt
            
        if command.startswith("cd "):
            new_dir = command[3:].strip()
            try:
                os.chdir(new_dir)
                self.currentDirectory = os.getcwd()
                self.prompt = f"<font color='#4275f5'>{self.currentDirectory}$</font> "
                self.inputArea.updatePromptLength(self.stripHTML(self.prompt))
            except Exception as e:
                self.appendOutput(f"Error: {e}\n", isError=True)
        elif command.lower() == "clear":
            self.outputArea.clear()
        else:
            self.process.start(command)
            self.isProcessRunning = True  # Mark process as running
    
    def readOutput(self):
        output = self.process.readAllStandardOutput().data().decode()
        self.appendOutput(output)

        # Apply special formatting if the command is 'ls'
        # if self.is_ls_command:
        #     self.formatListOutput(output)
        # else:
        #     self.appendOutput(output)

    def readError(self):
        error_output = self.process.readAllStandardError().data().decode()
        self.appendOutput(error_output, isError=True)

    def processFinished(self, exitCode, exitStatus):
        self.appendOutput(f"Process finished with exit code {exitCode}\n")
        self.isProcessRunning = False  # Process is no longer running

    def appendOutput(self, text, isError=False, isInput=False):
        if isError:
            self.outputArea.appendHtml(f"<font color='red'>{text}</font>")
        elif isInput:
            self.outputArea.appendHtml(f"<font color='green'>{text}</font>")
        elif self.is_ls_command:
            self.formatListOutput(text)
            self.is_ls_command = False
        else:
            self.outputArea.appendHtml(text)
        self.outputArea.moveCursor(QTextCursor.End)

    def formatListOutput(self, output):
        lines = output.splitlines()
        for line in lines:
            formatted_line = re.sub(r'\b(\S+)\b', 
                lambda match: f"<span style='font-weight: 900; color: #4275f5;'>{match.group(0)}</span>" if '.' not in match.group(0) else match.group(0), 
                line)
            self.outputArea.appendHtml(formatted_line)

    def stripHTML(self, html):
        return re.sub('<.*?>', '', html)

    def contextMenu(self, position):
        contextMenu = self.outputArea.createStandardContextMenu()

        clearOutputAction = QAction("Clear Terminal Output", self)
        copyOutputAction = QAction("Copy Output", self)
        terminateProcessAction = QAction("Terminate Process", self)

        clearOutputAction.triggered.connect(lambda: self.outputArea.clear())
        copyOutputAction.triggered.connect(self.copyOutput)
        terminateProcessAction.triggered.connect(self.terminateProcess)

        contextMenu.addSeparator()
        contextMenu.addAction(clearOutputAction)
        contextMenu.addAction(copyOutputAction)
        contextMenu.addAction(terminateProcessAction)

        contextMenu.exec_(self.outputArea.mapToGlobal(position))

    def terminateProcess(self):
        if self.process.state() == QProcess.Running:
            self.process.kill()
            self.isProcessRunning = False
            self.appendOutput("Process terminated by user\n", isError=True)

    def copyOutput(self):
        cursor = self.outputArea.textCursor()
        if cursor.hasSelection():
            selected_text = cursor.selectedText()
            clipboard = QApplication.clipboard()
            clipboard.setText(selected_text)
