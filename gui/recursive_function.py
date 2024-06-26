from .template.interface import Interface
from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget
from qfluentwidgets import (
    CaptionLabel, PlainTextEdit, PushButton, CheckBox, BodyLabel, SpinBox, ComboBox, qrouter,
    NavigationItemPosition, MessageBox, TabBar, SubtitleLabel, setFont, TabCloseButtonDisplayMode, IconWidget,
    TransparentDropDownToolButton, TransparentToolButton, setTheme, Theme, isDarkTheme,
    InfoBar, InfoBarPosition, InfoBarManager
    )
from qfluentwidgets import FluentIcon as FIF

class RecursiveFunction(Interface):
    def __init__(self, text: str, parent=None):
        super().__init__(
            'Recursive Function Simulator',
            'Binary Search Question',
            ['Run', 'Github'],
            ['1', '2', '3'],
            [FIF.PLAY, FIF.GITHUB, FIF.ADD, FIF.ADD, FIF.ADD],
            self.addFunctions,
            parent=parent
        )
        self.setObjectName(text.replace(' ', '-'))

    def addFunctions(self):
        function_list = [None, None, None, None, None]
        return function_list