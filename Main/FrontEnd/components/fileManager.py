import os
from tkinter.tix import Tree
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class FileManager(QTreeView):
    def __init__(self, newTab=None, deleteTabs = None, renameTabs = None, toggleHiddenFiles = None, toggleHiddenFolders = None, path=None, readOnlyFiles = None):
        super(FileManager, self).__init__()

        self.readOnlyFiles = readOnlyFiles
        self.newTab = newTab
        self.deleteTabs = deleteTabs
        self.renameTabs = renameTabs
        # Omitted as menu bar has shortcuts with checkbox state 
        # self.toggleHiddenFiles = toggleHiddenFiles
        # self.toggleHiddenFolders = toggleHiddenFolders
        self.path = str(path)
        self.fileSystemModel = QFileSystemModel()
        self.fileSystemModel.setRootPath(self.path)
        self.setToolTip(f"In {self.path}")
        self.setToolTipDuration(2000)
        self.fileSystemModel.setNameFilters(readOnlyFiles)
        self.fileSystemModel.setNameFilterDisables(False)

        self.setModel(self.fileSystemModel)
        self.setRootIndex(self.fileSystemModel.index(self.path))
        self.setAnimated(False)
        self.setIndentation(20)
        self.setSortingEnabled(False)

        self.clicked.connect(self.OnFileClicked)
        self.setDragEnabled(True)  # Enable dragging from FileManager
        self.setDragDropMode(QAbstractItemView.DragOnly)  # Set drag-only mode

        # Hiding column
        self.hideColumn(1)
        self.hideColumn(2)
        self.hideColumn(3)
        self.setHeaderHidden(True)
        self.setUpExpansion()

    def setUpExpansion(self):
        self.fileSystemModel.directoryLoaded.connect(self.autoExpand)

    # Handles opening all relevant folders, displaying editing files upon loading
    def autoExpand(self,path):
        self.expandAll()

    def OnFileClicked(self, index):
        filePath = self.fileSystemModel.filePath(index)
        if QFileInfo(filePath).isFile():
            self.newTab(filePath)

    def setNewTab(self, newTab):
        self.newTab = newTab

    # Drag operation to create new tabs in the TabView 
    def startDrag(self, supportedActions):
        index = self.currentIndex()
        filePath = self.fileSystemModel.filePath(index)
        if QFileInfo(filePath).isFile(): 
            drag = QDrag(self) # Setup drag action
            mimeData = QMimeData() # Set data required for drag action
            mimeData.setText(filePath)
            drag.setMimeData(mimeData)
            drag.exec_(Qt.CopyAction | Qt.MoveAction)

    def contextMenuEvent(self, event):
        # Create the context menu
        contextMenu = QMenu(self)

        # Get the position of the right-click
        index = self.indexAt(event.pos())
        filePath = self.fileSystemModel.filePath(index)

        #Don't set unless file right clicked
        openInNewTabAction = None
        deleteAction = None
        renameAction = None
        copyPathAction = None
        # toggleFilesAction = None
        # toggleFoldersAction = None
        # Enable/Disable actions based on the file type (file or folder)
        if QFileInfo(filePath).isFile():
            openInNewTabAction = contextMenu.addAction("Open in New Tab")
            deleteAction = contextMenu.addAction("Delete")
            renameAction = contextMenu.addAction("Rename")
            copyPathAction = contextMenu.addAction("Copy File Path")
        else:
            # Add actions (you can add more as needed)
            copyPathAction = contextMenu.addAction("Copy Project Path")
        # toggleFilesAction = contextMenu.addAction("Toggle Hide Files")
        # toggleFoldersAction = contextMenu.addAction("Toggle Hide Folders")
        # Show the context menu and get the selected action
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))

        # Handle the actions
        if action == openInNewTabAction:
            if QFileInfo(filePath).isFile(): # this seems redundant, but it fixes a bug
                self.newTab(filePath)  # You can customize this if needed
        elif action == copyPathAction:
            if not filePath:
                clipboard = QApplication.clipboard()
                clipboard.setText(self.path)
            else:
                clipboard = QApplication.clipboard()
                clipboard.setText(filePath)
        elif action == deleteAction:
            reply = QMessageBox.question(self, 'Delete', f"Are you sure you want to delete {filePath}?\n\nWARNING: This will also remove its tab and cannot be undone.", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                QFile.remove(filePath)
                self.deleteTabs(filePath)
                self.refreshView()
        elif action == renameAction:
            currentDir = QFileInfo(filePath).absoluteDir()
            currentFileName = QFileInfo(filePath).fileName()

            newName, ok = QInputDialog.getText(self, "Rename File", "Enter new name:", QLineEdit.Normal, currentFileName)

            if ok and newName:
                # Validate the new name
                if newName == currentFileName:
                    QMessageBox.warning(self, "Rename Error", "The new name is the same as the current name.")
                elif os.path.exists(currentDir.filePath(newName)):
                    QMessageBox.warning(self, "Rename Error", "A file with this name already exists in the current directory.")
                elif not self.isValidFileName(newName):
                    QMessageBox.warning(self, "Rename Error", "The file name contains invalid characters.")
                else:
                    newPath = currentDir.absoluteFilePath(newName)
                    QFile.rename(filePath, newPath)
                    self.renameTabs(filePath, newPath)
                    self.refreshView()
        # elif action == toggleFilesAction:
        #     self.toggleHiddenFiles()
        # elif action == toggleFoldersAction:
        #     self.toggleHiddenFolders()

    def isValidFileName(self, fileName):
        """
        Check if the given file name is valid. This checks for common invalid characters
        and ensures the name is not a reserved name like "." or "..".
        """
        invalidChars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']  # Add more if needed
        if any(char in fileName for char in invalidChars):
            return False
        if fileName in [".", ".."]:
            return False
        return True
    
    # Refreshes Model
    # This is really stupid and computationally inefficient. Sorry lol 
    # Should probably be changed in the future
    def refreshView(self):
        #copy old filters
        nameFilters = self.fileSystemModel.nameFilters()
        filters = self.fileSystemModel.filter()
        
        #remake whole ass file system
        self.fileSystemModel = QFileSystemModel()
        self.fileSystemModel.setRootPath(self.path)
        self.fileSystemModel.setNameFilters(nameFilters)
        self.fileSystemModel.setNameFilterDisables(False)
        self.fileSystemModel.setFilter(filters)
        self.setModel(self.fileSystemModel)
        self.setRootIndex(self.fileSystemModel.index(self.path))