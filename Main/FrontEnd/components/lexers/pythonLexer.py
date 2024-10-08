from PyQt5.Qsci import *
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import *

# Custom Python Lexer, necessary to change ridiculous out-of-box lexer behaviour
# Who in their right mind wanted the COLOUR, FONT, AND THE FONT SIZE for EACH DAMN TOKEN,
# WHAT WERE THEY SMOKING WHEN THEY MADE THIS

class PythonLexer(QsciLexerPython):

    # Style Currently mimics vsCode colour scheme
    def __init__(self, parent):
        super(PythonLexer, self).__init__()
        self.parent = parent
        self.colours = None
        self.font = QFont(QFont("monospace", parent.parent.fontSize))

    def applyStyle(self, themeName):
        # check if themeName matches, "dark", "light" or "highContrast" and call correct method
        if themeName == 'dark':
            self.setDarkMode()
        elif themeName == 'light':
            self.setLightMode()
        elif themeName == 'highContrast':
            self.setHighContrastMode()
        
        self.setupCustomStyle()

    def updateFontSize(self):
        self.font = QFont("monospace", self.parent.parent.fontSize)
        self.setDefaultFont(self.font)
        self.setFont(self.font)
        #Python lexer messes with fonts and sizes for different token types (ALSO extremely annoying)
        self.setFont(self.font, self.Keyword)
        self.setFont(self.font, self.Comment)
        self.setFont(self.font, self.CommentBlock)
        self.setFont(self.font, self.Number)
        self.setFont(self.font, self.Operator)
        self.setFont(self.font, self.ClassName)
        self.setFont(self.font, self.FunctionMethodName)
        self.setFont(self.font, self.SingleQuotedString)
        self.setFont(self.font, self.DoubleQuotedString)
        self.setFont(self.font, self.SingleQuotedFString)
        self.setFont(self.font, self.DoubleQuotedFString)
        self.setFont(self.font, self.TripleSingleQuotedString)
        self.setFont(self.font, self.TripleDoubleQuotedString)
        self.setFont(self.font, self.TripleSingleQuotedFString)
        self.setFont(self.font, self.TripleDoubleQuotedFString)
        self.setFont(self.font, self.UnclosedString)

    def setDarkMode(self):
        # Dark mode colors
        self.colours = {
            'background': '#1E1E2E',
            'foreground': '#D9E0EE',
            'keyword': '#F38BA8',
            'comment': '#6C7086',
            'className': '#FAB387',
            'function': '#82B4DA',
            'string': '#9EEC99',
            'number': '#EBA0AC',
            'operator': '#F5E0DC',
            'default': '#C6AAE8',
            'decorator': '#FF9E64'

        }

    def setLightMode(self):
        # Light mode colors
        self.colours = {
            'background': '#EFF1F5',
            'foreground': '#4C4F69',
            'keyword': '#D20F39',
            'comment': '#7287FD',
            'className': '#E64553',
            'function': '#209FB5',
            'string': '#40A02B',
            'number': '#DD7878',
            'operator': '#EA76CB',
            'default': '#7287FD',
            'decorator': '#DF8E1D'
        }

    def setHighContrastMode(self):
        # High contrast mode colors
        self.colours = {
            'background': '#000000',
            'foreground': '#FFFFFF',
            'keyword': '#FF00FF',
            'comment': '#00FF00',
            'className': '#00FFFF',
            'function': '#FFFF00',
            'string': '#FF5555',
            'number': '#00FFFF',
            'operator': '#FFFFFF',
            'default': '#FFAAAA',
            'decorator': '#FF9E64'            
        }
        

    def setupCustomStyle(self):
        # Apply background and foreground colors
        self.setDefaultFont(self.font)
        self.setDefaultColor(QColor(self.colours['foreground']))
        self.setDefaultPaper(QColor(self.colours['background']))
        self.setColor(QColor(self.colours['foreground']))
        self.setPaper(QColor(self.colours['background']))

        # Set colors for different token types
        self.setColor(QColor(self.colours['keyword']), self.Keyword)
        self.setColor(QColor(self.colours['comment']), self.Comment)
        self.setColor(QColor(self.colours['className']), self.ClassName)
        self.setColor(QColor(self.colours['function']), self.FunctionMethodName)
        self.setColor(QColor(self.colours['string']), self.SingleQuotedString)
        self.setColor(QColor(self.colours['string']), self.DoubleQuotedString)
        self.setColor(QColor(self.colours['string']), self.SingleQuotedFString)
        self.setColor(QColor(self.colours['string']), self.DoubleQuotedFString)
        self.setColor(QColor(self.colours['string']), self.TripleSingleQuotedString)
        self.setColor(QColor(self.colours['string']), self.TripleDoubleQuotedString)
        self.setColor(QColor(self.colours['string']), self.TripleSingleQuotedFString)
        self.setColor(QColor(self.colours['string']), self.TripleDoubleQuotedFString)
        self.setColor(QColor(self.colours['string']), self.UnclosedString)
        self.setColor(QColor(self.colours['number']), self.Number)
        self.setColor(QColor(self.colours['operator']), self.Operator)
        self.setColor(QColor(self.colours['decorator']), self.Decorator)

        #Python lexer sets paper in the background for different token types (extremely annoying btw)
        self.setPaper(QColor(self.colours['background']), self.SingleQuotedString)
        self.setPaper(QColor(self.colours['background']), self.DoubleQuotedString)
        self.setPaper(QColor(self.colours['background']), self.SingleQuotedFString)
        self.setPaper(QColor(self.colours['background']), self.DoubleQuotedFString)
        self.setPaper(QColor(self.colours['background']), self.TripleSingleQuotedString)
        self.setPaper(QColor(self.colours['background']), self.TripleDoubleQuotedString)
        self.setPaper(QColor(self.colours['background']), self.TripleSingleQuotedFString)
        self.setPaper(QColor(self.colours['background']), self.TripleDoubleQuotedFString)
        self.setPaper(QColor(self.colours['background']), self.UnclosedString)

        #Python lexer messes with fonts and sizes for different token types (ALSO extremely annoying)
        self.setFont(self.font, self.Keyword)
        self.setFont(self.font, self.Comment)
        self.setFont(self.font, self.CommentBlock)
        self.setFont(self.font, self.Number)
        self.setFont(self.font, self.Operator)
        self.setFont(self.font, self.ClassName)
        self.setFont(self.font, self.FunctionMethodName)
        self.setFont(self.font, self.SingleQuotedString)
        self.setFont(self.font, self.DoubleQuotedString)
        self.setFont(self.font, self.SingleQuotedFString)
        self.setFont(self.font, self.DoubleQuotedFString)
        self.setFont(self.font, self.TripleSingleQuotedString)
        self.setFont(self.font, self.TripleDoubleQuotedString)
        self.setFont(self.font, self.TripleSingleQuotedFString)
        self.setFont(self.font, self.TripleDoubleQuotedFString)
        self.setFont(self.font, self.UnclosedString)