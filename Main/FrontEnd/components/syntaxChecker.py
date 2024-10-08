import subprocess
from PyQt5.Qsci import QsciScintilla
from PyQt5.QtGui import QColor
import threading
import re

class SyntaxChecker:
    global lock
    lock = threading.Lock()
    def __init__(self):
        self.errorIndicatorNumber = 1
        self.editor = None
        
    def setupIndicator(self, editor):
        global lock
        lock.acquire()
        # if (self.editor != None):
        #     #clears underlines without locking
        #     self.editor.SendScintilla(QsciScintilla.SCI_INDICATORCLEARRANGE, 0, self.editor.length())
        self.editor = editor  # Set editor dynamically here
        editor.indicatorDefine(QsciScintilla.INDIC_SQUIGGLE, self.errorIndicatorNumber)
        editor.setIndicatorForegroundColor(QColor(255, 0, 0), self.errorIndicatorNumber)
        lock.release()

    def underlineErrors(self, line, startPos, errorPart):
        self._underLineErrorsFrom(line,startPos,errorPart,self.editor.filePath)

    def calculateLineLength(self,errorLineNum, errorCol, errorPart):
        endPos = errorCol + len(errorPart)
        lineLength = self.editor.lineLength(errorLineNum)
        if endPos > lineLength:
            endPos = lineLength
        
        return endPos

    def clearUnderlines(self):
        self._clearUnderlinesFrom(self.editor.filePath)

    def _underlineErrorsFrom(self, line, startPos, errorPart,filePath):
        global lock
        lock.acquire()
        if (not self._fileHasChanged(filePath)):
            # Dynamically calculate the length of the underline
            endPos = self.calculateLineLength(line, startPos,errorPart)

            if endPos is None:
                endPos = startPos + 10  # Arbitrary length to underline if endPos isn't provided
            # Calculate the start and end positions for underlining
            startIndex = self.editor.positionFromLineIndex(line, startPos)
            endIndex = self.editor.positionFromLineIndex(line, endPos)

            # Underline the exact portion in the editor
            self.editor.SendScintilla(QsciScintilla.SCI_INDICATORFILLRANGE, startIndex, endIndex - startIndex)
        lock.release()
        
    def _underlineWhole(self, line, startPos, errorPart,filePath):
        global lock
        lock.acquire()
        if (not self._fileHasChanged(filePath)):
            # Get the length of the entire line
            lineLength = self.editor.lineLength(line)
            
            # Start underlining from the beginning of the line
            startPos = 0
            endPos = lineLength

            # Calculate the start and end positions for underlining
            startIndex = self.editor.positionFromLineIndex(line, startPos)
            endIndex = self.editor.positionFromLineIndex(line, endPos)

            # Underline the whole line in the editor
            self.editor.SendScintilla(QsciScintilla.SCI_INDICATORFILLRANGE, startIndex, endIndex - startIndex)
        lock.release()

    def _clearUnderlinesFrom(self,filePath):
        global lock
        lock.acquire()
        if (not self._fileHasChanged(filePath)):
            self.editor.SendScintilla(QsciScintilla.SCI_INDICATORCLEARRANGE, 0, self.editor.length())
        lock.release()     

    def _fileHasChanged(self,filepath):
        return self.editor.filePath != filepath
