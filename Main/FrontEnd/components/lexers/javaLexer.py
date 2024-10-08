from PyQt5.Qsci import QsciLexerJava
from PyQt5.QtGui import QFont, QColor

# Custom Java Lexer, necessary to change ridiculous out-of-box lexer behaviour
# Who in their right mind wanted the COLOUR, FONT, AND THE FONT SIZE for EACH DAMN TOKEN,
# WHAT WERE THEY SMOKING WHEN THEY MADE THIS

class JavaLexer(QsciLexerJava):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.colours = None
        self.font = QFont("monospace", parent.parent.fontSize)

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
        self.setFont(self.font)

    def setDarkMode(self):
        self.colours = {
            'background': '#1E1E2E',
            'foreground': '#D9E0EE',
            'keyword': '#F38BA8',
            'comment': '#6C7086',
            'string': '#9EEC99',
            'number': '#82B4DA',
            'operator': '#F5E0DC',
            'default': '#C6AAE8',
        }


    def setLightMode(self):
        # Light mode colors here
        self.colours = {
            'background': '#EFF1F5',
            'foreground': '#4C4F69',
            'keyword': '#D20F39',
            'comment': '#7287FD',
            'string': '#40A02B',
            'number': '#DD7878',
            'operator': '#EA76CB',
            'default': '#7287FD',
        }

    def setHighContrastMode(self):
        # High contrast mode colors
        self.colours = {
            'background': '#000000',
            'foreground': '#FFFFFF',
            'keyword': '#FF00FF',
            'comment': '#00FF00',
            'string': '#FF5555',
            'number': '#00FFFF',
            'operator': '#FFFFFF',
            'default': '#FFAAAA',
        }

    def setupCustomStyle(self):
        # Apply background and foreground colors
        self.setDefaultColor(QColor(self.colours['foreground']))
        self.setDefaultPaper(QColor(self.colours['background']))
        self.setColor(QColor(self.colours['foreground']))
        self.setPaper(QColor(self.colours['background']))

        # Set colors for different token types
        self.setColor(QColor(self.colours['keyword']), self.Keyword)
        self.setColor(QColor(self.colours['comment']), self.Comment)
        self.setColor(QColor(self.colours['comment']), self.CommentLine)
        self.setColor(QColor(self.colours['comment']), self.CommentDoc)  # Block comments
        self.setColor(QColor(self.colours['string']), self.SingleQuotedString)
        self.setColor(QColor(self.colours['string']), self.DoubleQuotedString)
        self.setColor(QColor(self.colours['number']), self.Number)
        self.setColor(QColor(self.colours['operator']), self.Operator)

        # Set the font for all elements
        self.setFont(self.font)
