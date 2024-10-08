from PyQt5.Qsci import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QApplication, QMainWindow

from FrontEnd.components.lexers.pythonLexer import PythonLexer
from FrontEnd.components.lexers.javaLexer import JavaLexer

class Editor(QsciScintilla):
    clicked = pyqtSignal()

    def __init__(self, parent):
        super(Editor,self).__init__()
        self.parent = parent
        self.filePath = ""
        self.initialText = ""
        self.windowFont = QFont("monospace", parent.fontSize, 400)
        self.editorLexer = None
        self.themeName = "dark"

        self.setMarginWidth(0, 40)  # Adjust width as needed
        self.setMarginLineNumbers(0, True)  # Show line numbers
        self.setMarginsFont(QFont("monospace", parent.fontSize, 400))
        self.setFont(self.windowFont) 
        self.setUtf8(True) #encoder
        self.setCaretWidth(2)
        self.setFocusPolicy(Qt.NoFocus)

        #adds a matching closing brace when '(' introduced
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.setMatchedBraceBackgroundColor(QColor('#606060'))
        self.setTabWidth(4)
        self.setIndentationGuides(True)
        self.setIndentationsUseTabs(False) #Makes Indent us whitespce instead of '\t'
        self.setAutoIndent(True)

        # End-Of-Line Behaviour
        self.setEolMode(QsciScintilla.EolUnix) #OS Specific
        self.setEolVisibility(False)

        self.setAcceptDrops(False)  # Editor should not accept drops directly

        self.textChanged.connect(self.onTextChanged)
        

    def mousePressEvent(self, event):
        self.setFocus()  # Ensure the editor gets focus when clicked 
        self.clicked.emit() # once clicked status emit, pass the mouse press event to parent class
        super().mousePressEvent(event)

    def keyPressEvent(self, event):
        # Block zoom keys Ctrl + Minus, which zooms the window out, it clashes with font size adjustment implementation
        if event.modifiers() == Qt.ControlModifier:
            if event.key() in [Qt.Key_Minus, Qt.Key_T]:
                event.ignore()  # Block these key events
            else:
                super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)

    def wheelEvent(self, event):
        # Override to disable zoom with mouse wheel
        if QApplication.keyboardModifiers() == Qt.ControlModifier:
            event.ignore()  # Ignore wheel event when Ctrl is pressed
            return
        else:
            super().wheelEvent(event)

    def onTextChanged(self):
        if self.initialText != self.text():
            self.parent.markUnsavedTab(self, modified=True) # mark unsaved
        else:
            self.parent.markUnsavedTab(self, modified=False) # make no changes

    # sets the file path
    def setFilePath(self, filePath):
        self.filePath = filePath
        self.get_lexer()
    
    def getFilePath(self):
        if self.filePath:
            return self.filePath
        return None
    
    # Will be used in future to check if text has been changed or not (for conditional saving)
    def setInitialText(self, text):
        self.initialText = text
        
    def setAutoCompletionThreshold(self, length):
        super().setAutoCompletionThreshold(length)

    # Private method to be used internally to set lexer
    def get_lexer(self):
        #Check file extension and load corresponding lexer
        if self.filePath.endswith('.py'):
            self.editorLexer = PythonLexer(self)
            self.editorLexer.applyStyle(self.themeName) #default
            self.setLexer(self.editorLexer)

        if self.filePath.endswith('.java'):
            self.editorLexer = JavaLexer(self)
            self.editorLexer.applyStyle(self.themeName) #default
            self.setLexer(self.editorLexer)
        self.setUpAutoCompletion()

    def dragEnterEvent(self, event):
        event.ignore()  # Ignore drag events in the editor

    def dropEvent(self, event):
        event.ignore()  # Ignore drop events in the editor

    def applyStyle(self, themeName):
        self.themeName = themeName

        if themeName == 'dark':
            self.setDarkMode()
        elif themeName == 'light':
            self.setLightMode()
        elif themeName == 'highContrast':
            self.setHighContrastMode()

        if self.editorLexer:
            self.editorLexer.applyStyle(self.themeName)
            self.setLexer(self.editorLexer)
            self.setUpAutoCompletion()
            

        # Reapply margin colors after setting the lexer and theme
        self.setupMargins()

    # Forces update of the fontsize within self.windowFont, the lexer, and the margin
    def updateFontSize(self):
        self.windowFont = QFont("monospace", self.parent.fontSize, 400)
        self.setFont(self.windowFont)
        
        if self.editorLexer:
            self.editorLexer.updateFontSize()
            self.setLexer(self.editorLexer)
        
        self.setupMargins()


    def setupMargins(self):
        # Force the margins to repaint with the correct colors
        if self.themeName == 'dark':
            self.setMarginsBackgroundColor(QColor('#1C1C2C'))  # Dark margin background
            self.setMarginsForegroundColor(QColor('#D9E0EE'))  # Light margin text color
        elif self.themeName == 'light':
            self.setMarginsBackgroundColor(QColor('#DFE5E9'))  # Light margin background
            self.setMarginsForegroundColor(QColor('#2E3440'))  # Dark margin text color
        elif self.themeName == 'highContrast':
            self.setMarginsBackgroundColor(QColor('#181818'))  # High-contrast background
            self.setMarginsForegroundColor(QColor('#E0E0E0'))  # High-contrast text

        self.setMarginWidth(0, 40)  # Adjust width as needed
        self.setMarginLineNumbers(0, True)  # Show line numbers
        self.setMarginsFont(QFont("monospace", self.parent.fontSize, 400))

        # Force repaint to apply the margin changes
        self.update()

    def setDarkMode(self):
        self.setPaper(QColor('#1E1E2E'))  # Dark background color
        self.setColor(QColor('#D9E0EE'))  # Light text color
        self.setSelectionBackgroundColor(QColor('#89B4FA'))  # Selection color
        self.setMatchedBraceBackgroundColor(QColor('#4C566A'))  # Brace color
        self.setCaretForegroundColor(QColor('#D9E0EE'))  # Caret color

    def setLightMode(self):
        self.setPaper(QColor('#d4d4dd'))  # Light background color
        self.setColor(QColor('#2E3440'))  # Dark text color
        self.setSelectionBackgroundColor(QColor('#8caabe'))  # Selection color
        self.setMatchedBraceBackgroundColor(QColor('#8caabe'))  # Brace color
        self.setCaretForegroundColor(QColor('#2E3440'))  # Caret color

    def setHighContrastMode(self):
        self.setPaper(QColor('#101010'))  # Black background
        self.setColor(QColor('#E0E0E0'))  # White text
        self.setSelectionBackgroundColor(QColor('#56dcf3'))  # Red selection
        self.setMatchedBraceBackgroundColor(QColor('#FF00FF'))  # Magenta brace color
        self.setCaretForegroundColor(QColor('#FFFFFF'))  # White caret
        
    def setUpAutoCompletion(self):
        self.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.setAutoCompletionCaseSensitivity(False)
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionFillupsEnabled(True)
        #self.setAutoCompletionReplaceWord(True) # Uncomment if you want to replace connect words, i.e ad|alreadyHere -> add
        self.setCallTipsVisible(1)
        
        if self.themeName == 'default' or self.themeName == 'dark':
            self.setStyleSheet("""
            QsciScintilla {
                background-color: #1E1E2E;
                color: #D9E0EE;
            }
            QsciScintilla QAbstractItemView {
                background-color: #1E1E2E;
                color: #D9E0EE;
            }
            """)
            
        if self.themeName == 'light':
            self.setStyleSheet("""
            QsciScintilla {
                background-color: #d4d4dd;
                color: #2E3440;
                border: 2px solid black; 
            }
            QsciScintilla QAbstractItemView {
                background-color: #d4d4dd;
                color: #2E3440;
                border: 2px solid black
            }
            """)
        
        if self.themeName == 'highContrast':
            self.setStyleSheet("""
            QsciScintilla {
                background-color: #101010;
                color: #E0E0E0;
                selection-background-color: #56dcf3;
                selection-color: #101010;
            }
            QsciScintilla QAbstractItemView {
                background-color: #101010;
                color: #E0E0E0;
                selection-background-color: #56dcf3;
                selection-color: #101010;
            }
            """)