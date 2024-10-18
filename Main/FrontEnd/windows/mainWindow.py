import sys
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qsci import *
from PyQt5.QtGui import *
from FrontEnd.components.OutputRedirect import OutputRedirect
from PyQt5.QtGui import QIcon, QPixmap
from FrontEnd.components.errorLog import ErrorLog
from FrontEnd.components.tabView import TabView
from FrontEnd.components.runCluster import RunCluster
from FrontEnd.components.fileManager import FileManager
from FrontEnd.components.terminal import Terminal
from FrontEnd.frontEndApi import FrontEndApi
from FrontEnd.components.editor import Editor
from FrontEnd.components.syntaxChecker import SyntaxChecker
from ProjectHandler.projectHandler import ProjectHandler
import os
import importlib.util

# This initialises the main window and its corresponding UI elements and containers
class MainWindow(QMainWindow):
    saveSignal = pyqtSignal(str)
    
    def __init__(self, api=None, path=None, _returnMethod = None):
        super(QMainWindow, self).__init__()

        self.api : FrontEndApi = api
        self._returnMethod = _returnMethod

        self.viewHiddenFiles = False
        self.viewHiddenFolders = True
        
        self.autocompleteEnabled = True
        self.syntaxCheckerEnabled = True
        self.autosaveEnabled = True
    
        #Path to directory, for testing purposes
        if path != None:
            self.path = path
        else:
            # Gets absolute path file and then directs it to the test directory.
            self.path = self.api.projectThread.getCurrentProject().getProjectInfoPath()
        
        # Acquires files that should be shown
        self.writeFiles = self.api.projectThread.getCurrentProject().getProjectInfoGameInfo().getWriteFile()
        if any(writeFiles.lower() == "all" for writeFiles in self.writeFiles):
            for root, _, files in os.walk(self.path):
                self.writeFiles.extend([f for f in files if not f.endswith('.class')])
            
        self.fileManager = FileManager(
            newTab = self.newTab,
            deleteTabs=self.removeTabsOnDelete,
            renameTabs=self.updateTabsOnFileRename,
            toggleHiddenFiles=self.toggleHiddenFiles,
            toggleHiddenFolders=self.toggleHiddenFolders,
            path=self.path,
            readOnlyFiles= self.writeFiles
        )
        
        # Create an error label to display the error count
        self.errorLabel = QLabel("Errors: 0")  # Initialize with 0 errors
        self.errorLabel.setStyleSheet("color: red;")  # Customize the appearance of the label
        self.errorLabel.setFixedHeight(25)

        # initialising here for readability purposes
        self.mainTabView = None
        self.secondTabView = None
        self.terminalWindow = None
        self.errorLog = None
        self.compileCluster = None
        self.activeTabView = None
        self.projectHandler = None
        self.stderrRedirector = None
        self.syntaxHighlighter = None
        self.initUI()
        self.switchTheme("dark") # default
        
        self.javaFiles = None

        
    def initUI(self):
        # Body
        #.getProjectInfoName()
        result = self.api.projectThread.getCurrentProject()
        self.setWindowTitle(result.getProjectInfoName())
        self.resize(1600,1024)
        self.initMenu()
        self.initBody()
        self.setUpRedirect() # Redirects to terminal in the ide
        self.syntaxHighlighter = SyntaxChecker()
        self.api.projectThread.bindMainWindow(self)

    #Sets up the menu bar and its shortcuts for the main window
    def initMenu(self):
        #QT inbuilt menu bar function
        menuBar = self.menuBar()

        fileMenu = menuBar.addMenu("File")
        viewMenu = menuBar.addMenu("View")
        toolMenu = menuBar.addMenu("Tools")
        helpMenu = menuBar.addMenu("Help")

        #File Menu
        newTab = fileMenu.addAction("New Tab")
        newTab.setShortcut("Ctrl+N")
        newTab.triggered.connect(self.newTab)

        closeTab = fileMenu.addAction("Close Tab")
        closeTab.setShortcut("Ctrl+W")
        closeTab.triggered.connect(self.closeTab)

        saveFile = fileMenu.addAction("Save File")
        saveFile.setShortcut("Ctrl+S")
        saveFile.triggered.connect(self.saveFile)

        saveAs = fileMenu.addAction("Save As")
        saveAs.setShortcut("Shift+Ctrl+S")
        saveAs.triggered.connect(self.saveAs)

        saveProject = fileMenu.addAction("Save Project")
        saveProject.setShortcut("Ctrl+P")
        saveProject.triggered.connect(self.saveProject)

        windowMenu = QMenu("Layout", self)

        secondWindow = windowMenu.addAction("Split Tab")
        secondWindow.setShortcut("Ctrl+Tab")
        secondWindow.setShortcutContext(Qt.ApplicationShortcut)  # Ensure it works globally
        secondWindow.triggered.connect(self.onClickedToggleSplitTab)

        errorLog = windowMenu.addAction("Error Log")
        # errorLog.setShortcut("Shift+Ctrl+E") # Disabled until event propagation and filtering addressed
        errorLog.setShortcutContext(Qt.ApplicationShortcut)  # Ensure it works globally
        errorLog.triggered.connect(self.onClickedToggleErrorLog)

        terminalWindow = windowMenu.addAction("Terminal Window")
        # terminalWindow.setShortcut("Shift+Ctrl+T") # Disabled until event propagation and filtering addressed
        terminalWindow.setShortcutContext(Qt.ApplicationShortcut)  # Ensure it works globally
        terminalWindow.triggered.connect(self.onClickedToggleTerminal)

        runConsole = windowMenu.addAction("Run Console")
        # runConsole.setShortcut("Shift+Ctrl+R") # Disabled until event propagation and filtering addressed
        runConsole.setShortcutContext(Qt.ApplicationShortcut)  # Ensure it works globally
        runConsole.triggered.connect(self.onClickedToggleCompilerView)

        viewFiles = viewMenu.addAction("Toggle Hide Files")
        viewFiles.setShortcut("Ctrl+H")
        viewFiles.triggered.connect(self.toggleHiddenFiles)
        viewFiles.setCheckable(True)
        viewFiles.setChecked(True)

        viewFolders = viewMenu.addAction("Toggle Hide Folders")
        viewFolders.setShortcut("Ctrl+J")
        viewFolders.triggered.connect(self.toggleHiddenFolders)
        viewFolders.setCheckable(True)

        # View Menu: Add a "Themes" submenu
        themeMenu = QMenu("Themes", self)

        # View Menu: Add options to switch themes
        darkTheme = themeMenu.addAction("Dark Theme")
        darkTheme.triggered.connect(lambda: self.switchTheme("dark"))

        lightTheme = themeMenu.addAction("Light Theme")
        lightTheme.triggered.connect(lambda: self.switchTheme("light"))

        highContrastTheme = themeMenu.addAction("High Contrast Theme")
        highContrastTheme.triggered.connect(lambda: self.switchTheme("highContrast"))

        fontSizeMenu = QMenu("Font Size", self)

        increaseSize = fontSizeMenu.addAction("Increase Size")
        increaseSize.setShortcut("Shift+Ctrl+=")
        increaseSize.triggered.connect(lambda: self.adjustFontSize('increment'))

        decreaseSize = fontSizeMenu.addAction("Decrease Size")
        decreaseSize.setShortcut("Shift+Ctrl+-")
        decreaseSize.triggered.connect(lambda: self.adjustFontSize('decrement'))

        resetSize = fontSizeMenu.addAction("Reset (Size 12)")
        resetSize.setShortcut("Shift+Ctrl+0")
        resetSize.triggered.connect(lambda: self.adjustFontSize('reset'))

        returnToProjectSelect = fileMenu.addAction("Return to Project Selection Screen")
        returnToProjectSelect.triggered.connect(self.returnFromCodeEditor)

        viewMenu.addMenu(windowMenu)
        viewMenu.addSeparator()
        viewMenu.addMenu(fontSizeMenu)
        viewMenu.addMenu(themeMenu)

        #Help Menu
        # tutorial = helpMenu.addAction("Tutorial")
        # tutorial.triggered.connect(lambda: print("Shortcut not bound yet"))

        #Tool Menu
        syntaxCheckerMenu = toolMenu.addAction("Toggle Syntax Checker")
        syntaxCheckerMenu.triggered.connect(self.toggleSyntaxChecker)
        syntaxCheckerMenu.setCheckable(True)
        syntaxCheckerMenu.setChecked(True)

        autocompleteMenu = toolMenu.addAction("Toggle Autocomplete")
        autocompleteMenu.triggered.connect(self.toggleAutocomplete)
        autocompleteMenu.setCheckable(True)
        autocompleteMenu.setChecked(True)

        autosaveMenu = toolMenu.addAction("Toggle Autosave")
        autosaveMenu.triggered.connect(self.toggleAutosave)
        autosaveMenu.setCheckable(True)
        autosaveMenu.setChecked(True)
        self.startAutosave()
    
    # Calls newTab in tabView
    def newTab(self, filePath=None):
        self.activeTabView.newTab(filePath)
        # sets active highlight to track active tab
        activeEditor = self.getActiveEditor()
        if activeEditor is not None:
            self.syntaxHighlighter.setupIndicator(activeEditor)

    # Calls close_tab in tabView
    def closeTab(self):
        self.activeTabView.closeTab(self.activeTabView.currentIndex())

    # Calls save_file in tabView
    def saveFile(self):
        self.activeTabView.saveFile()
        self.checkSyntax()

    # Calls save_as in tabView
    def saveAs(self):
        self.activeTabView.saveAs()

    # Saves every file that has been changed
    # by providing a dict with file paths and contents to save to the api
    def saveProject(self):
        if (self.activeTabView != None):        
            self.api.saveProject(self.activeTabView.getAllOpenFiles())
            self.checkSyntax()
        
    # Standard method to create empty QFrame
    def createFrame(self) -> QFrame:
        frame = QFrame()
        frame.setFrameShape(QFrame.NoFrame)
        frame.setFrameShadow(QFrame.Plain)
        frame.setContentsMargins(0, 0, 0, 0)
        return frame

    # Establishes stucture of the main window UI and sequentially isntantiates the necessary components
    def initBody(self):
        # MAIN BODY #
        # Set up basic frame to hold box layout
        bodyFrame = self.createFrame()
        bodyFrame.setLineWidth(0)
        bodyFrame.setMidLineWidth(0)
        bodyFrame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set up body layout
        mainVerticalLayout = QVBoxLayout()
        mainVerticalLayout.setContentsMargins(0, 0, 0, 0)
        mainVerticalLayout.setSpacing(0)
        bodyFrame.setLayout(mainVerticalLayout)

        # Set up left panel layout for file manager, compile cluster, and toggle buttons
        leftPanelLayout = QVBoxLayout()
        leftPanelLayout.setContentsMargins(0, 0, 0, 0)
        leftPanelLayout.setSpacing(0)
        
        fileManagerFrame = self.createFrame()
        
        fileManagerLayout = QVBoxLayout()
        fileManagerLayout.setContentsMargins(0, 0, 0, 0)
        fileManagerLayout.setSpacing(0)
        
        self.compileCluster = RunCluster(self, projectThreadController=self.api.projectThread)

        fileManagerLayout.addWidget(self.fileManager)
        fileManagerLayout.addWidget(self.compileCluster)
        
        fileManagerFrame.setLayout(fileManagerLayout)
        
        # Toggle buttons setup
        self.errorLogToggle = QToolButton()
        self.errorLogToggle.setText("Errors (0)")
        
        self.errorLog = ErrorLog(self, self.errorLogToggle)
        
        compilerToggle = QToolButton()
        compilerToggle.setText("Run Console")
        splitTabToggle = QToolButton()
        splitTabToggle.setText("Split Tab")
        terminalToggle = QToolButton()
        terminalToggle.setText("Terminal")
        
        compilerToggle.clicked.connect(self.onClickedToggleCompilerView)
        self.errorLogToggle.clicked.connect(self.onClickedToggleErrorLog)
        splitTabToggle.clicked.connect(self.onClickedToggleSplitTab)
        terminalToggle.clicked.connect(self.onClickedToggleTerminal)
        
        buttonFrame = self.createFrame()
        buttonFrame.setLineWidth(0)
        buttonFrame.setMidLineWidth(0)
        buttonFrame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        buttonLayout = QHBoxLayout()
        buttonLayout.setContentsMargins(3, 0, 3, 0)
        buttonLayout.setSpacing(0)
        buttonLayout.addWidget(splitTabToggle)
        buttonLayout.addWidget(self.errorLogToggle)
        buttonLayout.addWidget(compilerToggle)
        buttonLayout.addWidget(terminalToggle)
    
        buttonLayout.setAlignment(Qt.AlignCenter)
        buttonFrame.setLayout(buttonLayout)
        
        leftPanelLayout.addWidget(fileManagerFrame)
        leftPanelLayout.addWidget(buttonFrame)
        
        # Set up right panel layout for tab views, terminal, and error log
        rightPanelLayout = QVBoxLayout()
        rightPanelLayout.setContentsMargins(0, 0, 0, 0)
        rightPanelLayout.setSpacing(0)
        
        self.mainTabView = TabView(self.api)
        self.secondTabView = TabView(self.api)
        self.mainTabView.switched.connect(lambda: self.switchActiveTabView(self.mainTabView))
        self.secondTabView.switched.connect(lambda: self.switchActiveTabView(self.secondTabView))
        self.mainTabView.tabBarClicked.connect(self.swapAtMainIndex)
        self.secondTabView.tabBarClicked.connect(self.swapAtSecondIndex)

        self.activeTabView = self.mainTabView
        self.activeTabView.setActive(True)
        self.secondTabView.setVisible(False)
        
        tabViewSplitter = QSplitter(Qt.Horizontal)
        tabViewSplitter.addWidget(self.mainTabView)
        tabViewSplitter.addWidget(self.secondTabView)
        
        self.terminalWindow = Terminal(path=self.path)

        editorVerticalSplitter = QSplitter(Qt.Vertical)
        editorVerticalSplitter.addWidget(tabViewSplitter)
        editorVerticalSplitter.addWidget(self.terminalWindow)
    
        
        editorVerticalSplitter.addWidget(self.errorLog)
        editorVerticalSplitter.setSizes([800, 200, 100])
        
        rightPanelLayout.addWidget(editorVerticalSplitter)
        
        # Create frames for left and right panels
        leftPanelFrame = self.createFrame()
        leftPanelFrame.setLayout(leftPanelLayout)
        leftPanelFrame.setMinimumWidth(300)
        leftPanelFrame.setMaximumWidth(400)

        rightPanelFrame = self.createFrame()
        rightPanelFrame.setLayout(rightPanelLayout)

        # Main splitter to separate left and right panels
        mainSplitter = QSplitter(Qt.Horizontal)  # Horizontal splitter to separate left and right
        mainSplitter.addWidget(leftPanelFrame)
        mainSplitter.addWidget(rightPanelFrame)

        # Optionally, set initial sizes for the panels (adjustable at runtime)
        mainSplitter.setSizes([leftPanelFrame.width(), rightPanelFrame.width()])  # Left panel starts at 360px, right panel takes the rest

        mainVerticalLayout.addWidget(mainSplitter)
        
        self.setCentralWidget(bodyFrame)
        
    # sets The activeTabView to given parameter, 
    # controls which tab View shortcuts effect, sets active style too
    def switchActiveTabView(self, tabView):
        activeEditor = None
        gotEditor = False
        if tabView != self.activeTabView:
            self.activeTabView.setActive(False)

            # Activate the new TabView
            self.activeTabView = tabView
            self.activeTabView.setActive(True)
            self.fileManager.setNewTab(self.newTab)

            # sets active highlight to track active tab
            activeEditor = self.getActiveEditor()
            gotEditor = True
            if activeEditor is not None:
                self.syntaxHighlighter.setupIndicator(self.getActiveEditor())
                self.checkSyntax()
                
        if (not gotEditor):
            activeEditor = self.getActiveEditor()
        if activeEditor is not None:
            QTimer.singleShot(0, lambda: self.applyAutocompleteState(activeEditor)) #Issue persisted that toggling didnt work due to timing, thus added timer to 
                
    def applyAutocompleteState(self, activeEditor):
        if self.autocompleteEnabled:
            activeEditor.setAutoCompletionSource(QsciScintilla.AcsAll)
        else:
            activeEditor.setAutoCompletionSource(QsciScintilla.AcsNone)

    def onClickedToggleCompilerView(self):
        visible = self.compileCluster.isVisible()
        self.compileCluster.setVisible(not visible)

    def onClickedToggleErrorLog(self):
        visible = self.errorLog.isVisible()
        self.errorLog.setVisible(not visible)

    def onClickedToggleTerminal(self):
        visible = self.terminalWindow.isVisible()
        self.terminalWindow.setVisible(not visible)

    def onClickedToggleSplitTab(self):
        if self.secondTabView.isVisible(): #if visible, hide it, and vice versa
            self.switchActiveTabView(self.mainTabView)
            self.secondTabView.setVisible(False)
        else:
            self.switchActiveTabView(self.secondTabView)
            self.secondTabView.setVisible(True)

    def adjustFontSize(self, action):
        if self.mainTabView != None:
            currentSize = self.mainTabView.fontSize

            match action:
                case 'increment':
                    if currentSize < 16:
                        self.mainTabView.setFontSize(currentSize+1)
                        self.secondTabView.setFontSize(currentSize+1)
                case 'decrement':
                    if currentSize > 8:
                        self.mainTabView.setFontSize(currentSize-1)
                        self.secondTabView.setFontSize(currentSize-1)
                case 'reset':
                    self.mainTabView.setFontSize(12)
                    self.secondTabView.setFontSize(12)

    def switchTheme(self, themeName):
        base_path = Path(__file__).parent.parent  # Goes up one directory from FrontEnd/windows to FrontEnd

        # Map theme names to relative paths
        themePaths = {
            "dark": base_path / "resources/styles/dark.qss",
            "light": base_path / "resources/styles/light.qss",
            "highContrast": base_path / "resources/styles/contrast.qss",
        }

        if themeName in themePaths:
            themePath = themePaths[themeName]
            if themePath.exists():
                with themePath.open("r") as f:
                    styleSheet = f.read()
                    self.setStyleSheet(styleSheet)

                    #TabView needs separate themes due to active and inactive styling
                    if self.mainTabView != None:
                        self.mainTabView.switchTheme(themeName)
                    if self.secondTabView != None:
                        self.secondTabView.switchTheme(themeName)
                self.currentTheme = themeName

            else:
                print(f"Theme file {themePath} not found.")

    # Handles user attempting to close main window
    def closeEvent(self,event):
        self.checkIfFilesSaved()
        self._returnMethod(True) # returns True to main window, thereby requesting the program to shutdown

    # Toggls files to be hidden or not
    def toggleHiddenFiles(self): 
        if (not self.viewHiddenFiles):
            self.fileManager.fileSystemModel.setNameFilters(["*"])
        else:
            self.fileManager.fileSystemModel.setNameFilters(self.writeFiles)

        # Flip boolean
        self.viewHiddenFiles = not self.viewHiddenFiles

    def toggleHiddenFolders(self):
        if (self.viewHiddenFolders):
            self.viewHiddenFolders = False
            self.fileManager.fileSystemModel.setFilter(QDir.Files)
        else:
            self.viewHiddenFolders = True
            self.fileManager.fileSystemModel.setFilter( QDir.AllEntries | QDir.NoDotAndDotDot | QDir.AllDirs)
        
    def checkIfFilesSaved(self):
        unsavedFiles = False
        
        for i in range(self.mainTabView.count()):
            editor = self.mainTabView.getEditors(i)
            if (editor.initialText != editor.text()):
                unsavedFiles = True
            
        if unsavedFiles:
            reply = QMessageBox.question(self, "Save All Files", "Do you want to save changes to the files?",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.saveProject()
            
    def returnFromCodeEditor(self):
        os.chdir("..")
        os.chdir("..")
        self._returnMethod(False)

    def setUpRedirect(self):
        # Create separate redirectors for stdout and stderr
        self.stdoutRedirector = OutputRedirect(self.terminalWindow, self.errorLog)
        self.stderrRedirector = OutputRedirect(self.terminalWindow, self.errorLog)
        self.stderrRedirector.set_stderr(True)  # Indicate that this is for stderr

        sys.stdout = self.stdoutRedirector  # Redirect standard output to the custom terminal
        sys.stderr = self.stderrRedirector  # Redirect standard error to the custom error log
    
    def getRedirector(self):
        return self.stderrRedirector
    
    def checkSyntax(self):
        if (self.syntaxCheckerEnabled):
            filePath = self.getActiveFilePath()
            if (not QFileInfo(filePath).isDir()):
                if self.javaFiles == None: # Compiles all files first time to make sure imports dont throw errors
                    self.javaFiles = []
                    for root, _, files in os.walk(self.path):
                        self.javaFiles.extend([os.path.join(root, f) for f in files if f.endswith('.java')])      
                    args = [filePath, self.javaFiles]
                    self.api.projectThread.requestCheck(args)
                else:
                    args = [filePath, [filePath]] # only compiles the current file other times, to fix performance.
                    self.api.projectThread.requestCheck(args)
    
    def getActiveFilePath(self):
        currentEditor = self.activeTabView.getEditor()  # Get the editor for the active tab
        if currentEditor:
            filePath = currentEditor.getFilePath()
            if filePath:
                return filePath
        return None
    
    def getActiveEditor(self):
        return self.activeTabView.getEditor()
    

    # This group handles swapping tabs without without causing issues for syntax checking or split tab targeting

    def swapAtMainIndex(self,index):
        self._swapAtIndex(self.mainTabView,index)

    def swapAtSecondIndex(self,index):
        self._swapAtIndex(self.secondTabView,index)

    def _swapAtIndex(self,tabView, index):
        tabView.swapAtIndex(index)
        self.syntaxHighlighter.setupIndicator(self.getActiveEditor())
        self.checkSyntax()
    
    def toggleAutocomplete(self):
        activeEditor = self.getActiveEditor()
        if activeEditor:
            self.autocompleteEnabled = not self.autocompleteEnabled
            
            if not self.autocompleteEnabled:
                activeEditor.setAutoCompletionSource(QsciScintilla.AcsNone)  # Disable autocomplete
            else:
                activeEditor.setAutoCompletionSource(QsciScintilla.AcsAll)  # Enable autocomplete
                
    def getAutoCompleteState(self):
        return self.autocompleteEnabled
    
    def toggleSyntaxChecker(self):
        self.syntaxCheckerEnabled = not self.syntaxCheckerEnabled

    # Saves project every 20 seconds
    def startAutosave(self):
        self.autosaveTimer = QTimer(self)
        self.autosaveTimer.setSingleShot(False)
        self.autosaveTimer.timeout.connect(self.autosave)
        self.autosaveTimer.start(20000)

    def toggleAutosave(self):
        self.autosaveEnabled = not self.autosaveEnabled

    def autosave(self):
        if (self.autosaveEnabled):
            self.saveProject()
        



    # These methods related to renaming and deleting files;
    #   This ensures that when file changes are made in FileManager, the tab views are up to date as well

    # Removes tabs from both tab views when its associated file is deleted
    def removeTabsOnDelete(self, filePath):
        self.mainTabView.removeTabByPath(filePath)
        self.secondTabView.removeTabByPath(filePath)

    #Renames tabs and updates its file when its associated file is renamed
    def updateTabsOnFileRename(self, oldFilePath, newFilePath):
        self.mainTabView.updateTabOnRename(oldFilePath, newFilePath)
        self.secondTabView.updateTabOnRename(oldFilePath, newFilePath)