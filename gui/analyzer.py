from .template.interface import Interface
from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget
from qfluentwidgets import FluentIcon as FIF


class Analyzer(Interface):
    def __init__(self, text: str, parent=None):
        super().__init__(
            'Performance Analysis',
            'Knapsack Question',
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