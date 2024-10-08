from PyQt5.QtCore import QObject, pyqtSignal

class OutputRedirect(QObject):
    terminalOutputSignal = pyqtSignal(str)
    errorOutputSignal = pyqtSignal(str)

    def __init__(self, terminal, errorLog):
        super().__init__()
        self.terminal = terminal
        self.errorLog = errorLog
        self.isStderr = False

        # Connect signals to slots
        self.terminalOutputSignal.connect(self.terminal.appendOutput)
        self.errorOutputSignal.connect(self.errorLog.add)

    def write(self, message):
        if not message.strip():
            return  # Ignore empty messages
        
        # Emit signal to update GUI in the main thread
        if self.isStderr:
            self.errorOutputSignal.emit(message)
        else:
            self.terminalOutputSignal.emit(message)

    def flush(self):
        pass
    
    def set_stderr(self, isStderr=True):
        self.isStderr = isStderr