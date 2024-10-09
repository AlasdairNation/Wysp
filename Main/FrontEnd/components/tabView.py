from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pathlib import Path
from FrontEnd.components.editor import Editor
from FrontEnd.frontEndApi import FrontEndApi

# Extends QTabWidget with custom functionality, e.g custom new/close tab and file saving
class TabView(QTabWidget):
    switched = pyqtSignal()

    def __init__(self, api=None):
        super(TabView, self).__init__()
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setDocumentMode(True)
        self.tabCloseRequested.connect(self.closeTab)
        self.fontSize = 12 #default font size for editors

        # Default styles for active and inactive states
        self.inactiveStyle = ""
        self.activeStyle = ""
        self.themeName = 'dark'
        self.active = False
        self.switchTheme(self.themeName)
        self.setStyleSheet(self.inactiveStyle)  # Set initial style
        self.api : FrontEndApi = api
        self.openFiles = []
        self.newTabs = []

        self.setAcceptDrops(True)  # Enable dropping into TabView

    # Creates a new tab with a text editor
    def newTab(self, filePath=None):
        editor = self.createEditor()
        
        if filePath: #exists
            if filePath not in self.openFiles: #not open already
                # Create new tab and fill editor with file content
                try:
                    with open(filePath, 'r') as file:
                        content = file.read()
                        editor.setInitialText(content)
                        editor.setText(content)
                        editor.setFilePath(filePath)
                    index = self.addTab(editor, QFileInfo(filePath).fileName())
                    self.openFiles.append(filePath) # add to open files for tracking tabs
                    self.setCurrentIndex(index) # put new tab in focus
                    self.switched.emit() # trigger click to make tab view active after 'drop
                    editor.setUpAutoCompletion()
                except Exception as e:
                    print(f"Could not open file: {e}")
            else: # Switch to the already existing tab
                for index in range(self.count()):
                    tab : Editor = self.widget(index)
                    if tab.filePath == filePath:
                        self.setCurrentIndex(index)
                        self.switched.emit() # trigger click to make tab view active after 'drop
                        break
        else: # Open blank tab
            editor.setFilePath(f"New Tab ({len(self.newTabs)})") # Set Tab name as File Path
            index = self.addTab(editor, editor.filePath)
            self.newTabs.append(editor.filePath) #Increment new tab count by 1
            self.setCurrentIndex(index)
            self.switched.emit() # trigger click to make tab view active after 'drop
            editor.setUpAutoCompletion()

    # Closes open tab and handles saving logic
    def closeTab(self, index):
        if self.count() > 0: # Don't do anything if no tabs present
            editor: Editor = self.widget(index)

            # Text is not empty
            if editor.text() != "":
                if editor.initialText != editor.text(): # if text different to how it was when first opened
                    reply = QMessageBox.question(self, "Save File", "Do you want to save changes to the file?",
                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                    if reply == QMessageBox.Yes:
                        self.saveFile()
                    
                    
            if editor.filePath in self.openFiles:
                self.openFiles.remove(editor.filePath)

            if editor.filePath in self.newTabs:
                self.newTabs.remove(editor.filePath)

            self.removeTab(index)

    # Gets editor instance
    def getEditor(self):
        currentIndex = self.currentIndex() 
        if currentIndex != -1:
            editor = self.widget(currentIndex)  
            if isinstance(editor, Editor):
                editor.applyStyle(self.themeName)
                return editor
        return None
    
    def getEditors(self, index):
        return self.widget(index)
    
    # Creates editor instance, USE THIS METHOD AT ALL TIMES WHEN CONTRUCTING AN INSTANCE, DO NOT INTIALISE WITHIN METHODS
    def createEditor(self):
        editor = Editor(parent=self)
        editor.applyStyle(self.themeName)
        editor.clicked.connect(lambda: self.switched.emit())
        return editor

    # Save's current file
    def saveFile(self):
        currentIndex = self.currentIndex()
        editor: Editor = self.widget(currentIndex)
        
        if editor:
            currentText = editor.text()
            if currentText: # If text is present and not an empty tab
                if editor.filePath in self.openFiles: #If already present file (not a new tab)
                    filePath = editor.filePath
                    if self.api: # Ensure API is present
                        file = {}
                        file[filePath] = currentText
                        self.api.saveFile(file)
                        editor.setInitialText(currentText)
                        self.setTabText(currentIndex, self.tabText(currentIndex).rstrip('*'))  # Remove the asterisk if no longer modified
                    else:
                        print("NO API PRESENT")
                        # No point in keeping this code active, API will always be present
                        # try:
                        #     with open(filePath, 'w') as file:
                        #         file.write(currentText)
                        #     editor.setInitialText(currentText) # Reset the initial text after successful save
                        #     print(f"Saved: {filePath}")
                        #     self.setTabText(currentIndex, self.tabText(currentIndex).rstrip('*'))  # Remove the asterisk if no longer modified
                        # except Exception as e:
                        #     print(f"Could not save file: {e}")

                else: # Perform save as function
                    # print("here")
                    self.saveAs()

    # Save text in a new file
    def saveAs(self):
        currentIndex = self.currentIndex()
        editor: Editor = self.widget(currentIndex)
        if editor:
            currentText = editor.text()
            if currentText: # If text is present and not an empty tab
                options = QFileDialog.Options()
                filePaths = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*);;Python Files (*.py);;Java Files (*.java);;Text Files (*.txt)",
                                                            options=options) #This returns tuple of file paths
                if filePaths:
                    filePath = filePaths[0]
                    # if not self.api: # Conditional if statement so that file handling still usable if api not present

                    #If saveAs is replacing an already present file that is currently open, replace the contents and close the tab saveAs was called on
                    # Very specific edge case, may not happen that often, but ensures consistency
                    if filePath in self.openFiles:
                        self.removeTab(currentIndex)

                        for index in range(self.count()):
                            tab : Editor = self.widget(index)
                            if tab.filePath == filePath:
                                tab.setInitialText(currentText)
                                tab.setText(currentText)
                        
                        # Save into file contents as well
                        try:
                            with open(filePath, 'w') as file:
                                file.write(currentText)
                                print(f"Saved: {filePath}")
                        except Exception as e:
                            print(f"Could not save file: {e}")

                    else:

                        try:
                            with open(filePath, 'w') as file:
                                file.write(currentText)
                            editor.setInitialText(currentText) # Reset the initial text after successful save
                            editor.filePath = filePath
                            index = self.addTab(editor, QFileInfo(filePath).fileName())
                            self.openFiles.append(editor.filePath)
                            self.setCurrentIndex(index)
                            # self.setTabText(index, self.tabText(index=index).rstrip('*'))  # Remove the asterisk
                            print(f"Saved: {filePath}")
                        except Exception as e:
                            print(f"Could not save file: {e}")

    ## Methods for saving entire project **
    # Returns every open file path, and their contents
    def getAllOpenFiles(self):
        listFilesToSave = {}

        for filePath in self.openFiles:
            listFilesToSave[filePath] = self.getContentByPath(filePath)
        
        return listFilesToSave
    
    # aqcuires file contents based off file path
    def getContentByPath(self, filePath):
        for index in range(self.count()):
            tab : Editor = self.widget(index)
            if tab.filePath == filePath:
                return tab.text()
    
    # sets the style sheet according to whether tab is currently active or inactive
    def setActive(self, active):
        self.active = active
        if active:
            self.setStyleSheet(self.activeStyle)
        else:
            self.setStyleSheet(self.inactiveStyle)

    # marks the tab title when it has been modified but not saved
    def markUnsavedTab(self, editor, modified):
        index = self.indexOf(editor)
        title = self.tabText(index)
        if modified:
            if not title.endswith('*'):
                self.setTabText(index, title + '*')  # Add an asterisk if not already present
        else:
            self.setTabText(index, title.rstrip('*'))  # Remove the asterisk if no longer modified

    #updates the details of corresponding tab when file is renamed
    def updateTabOnRename(self, oldPath, newPath):
        for index in range(self.count()):
            tab : Editor = self.widget(index)
            if tab.filePath == oldPath:
                self.openFiles.remove(oldPath)
                self.openFiles.append(newPath)
                tab.filePath = newPath
                self.setTabText(index,QFileInfo(newPath).fileName())

    def removeTabByPath(self, filePath):
         for index in range(self.count()):
            tab : Editor = self.widget(index)
            if tab.filePath == filePath:
                self.openFiles.remove(filePath)
                self.closeTab(index)
            
    ## Event handling and signal emmitting ##
    #emits switched signal so that mainWindow knows which tabView to make active
    def mousePressEvent(self, event):
        self.switched.emit()
            
    # validates item being dragged has some sort of data
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    # validates item being dropped contains a file path, that is also valid
    def dropEvent(self, event):
        file_path = event.mimeData().text()
        if QFileInfo(file_path).isFile():
            self.newTab(file_path)
            event.acceptProposedAction()
        else:
            event.ignore()

    def swapAtIndex(self,index):
        tab : Editor = self.widget(index)
        self.setCurrentIndex(index)
        self.switched.emit() # trigger click to make tab view active after 'drop
    
    def switchTheme(self, themeName):
        if themeName == 'dark':
            self.setDarkMode()
        elif themeName == 'light':
            self.setLightMode()
        elif themeName == 'highContrast':
            self.setHighContrastMode()
        
        # Loop through every open tab
        for index in range(self.count()):
            editor: Editor = self.widget(index)
            editor.applyStyle(themeName)

        self.themeName = themeName

    # Calls update font
    def setFontSize(self, newFontSize):
        self.fontSize = newFontSize
        # Loop through every open tab
        for index in range(self.count()):
            editor: Editor = self.widget(index)
            editor.updateFontSize()

    # manually set the colours of the editor
    def setDarkMode(self):
        base_path = Path(__file__).parent.parent  # Goes up one directory from FrontEnd/components to FrontEnd

        activePath = base_path / "resources/styles/tabView/darkActive.qss"
        inactivePath = base_path / "resources/styles/tabView/darkInactive.qss"

        if activePath.exists():
            with activePath.open("r") as f:
                self.activeStyle = f.read()
        else:
            print(f"Theme file {activePath} not found.")

        if inactivePath.exists():
            with inactivePath.open("r") as f:
                self.inactiveStyle = f.read()
        else:
            print(f"Theme file {inactivePath} not found.")

        self.setActive(self.active)
    
    def setLightMode(self):
        base_path = Path(__file__).parent.parent  # Goes up one directory from FrontEnd/components to FrontEnd

        activePath = base_path / "resources/styles/tabView/lightActive.qss"
        inactivePath = base_path / "resources/styles/tabView/lightInactive.qss"

        if activePath.exists():
            with activePath.open("r") as f:
                self.activeStyle = f.read()
        else:
            print(f"Theme file {activePath} not found.")

        if inactivePath.exists():
            with inactivePath.open("r") as f:
                self.inactiveStyle = f.read()
        else:
            print(f"Theme file {inactivePath} not found.")

        self.setActive(self.active)

    def setHighContrastMode(self):
        base_path = Path(__file__).parent.parent  # Goes up one directory from FrontEnd/components to FrontEnd

        activePath = base_path / "resources/styles/tabView/contrastActive.qss"
        inactivePath = base_path / "resources/styles/tabView/contrastInactive.qss"

        if activePath.exists():
            with activePath.open("r") as f:
                self.activeStyle = f.read()
        else:
            print(f"Theme file {activePath} not found.")

        if inactivePath.exists():
            with inactivePath.open("r") as f:
                self.inactiveStyle = f.read()
        else:
            print(f"Theme file {inactivePath} not found.")

        self.setActive(self.active)