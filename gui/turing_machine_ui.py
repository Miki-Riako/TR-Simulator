from .template.interface import Interface
from PySide6.QtCore import QPoint, Qt
from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget
from PySide6.QtWidgets import QTreeWidgetItem, QHBoxLayout, QTreeWidgetItemIterator, QTableWidgetItem, QListWidgetItem
from qfluentwidgets import InfoBarIcon, InfoBar, PushButton, setTheme, Theme, FluentIcon, InfoBarPosition, InfoBarManager
from qfluentwidgets import TreeWidget, TableWidget, ListWidget, HorizontalFlipView
from qfluentwidgets import FluentIcon as FIF



class InputTape(TableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.verticalHeader().hide()
        self.setBorderRadius(8)
        self.setBorderVisible(True)

        self.infos = [10, 5, 0, 1, 2, 3, 4, 6, 7, 8, 9, 10]
        self.setColumnCount(len(self.infos))
        self.setRowCount(1)
        for i in range(len(self.infos)):
            self.setItem(0, i, QTableWidgetItem(str(self.infos[i])))

        # self.resizeColumnsToContents()
        # self.resizeRowsToContents()
    
    def addItem(self):
        ...
    
    def removeItem(self):
        ...



class TuringMachineUI(Interface):
    def __init__(self, text: str, parent=None):
        super().__init__(
            'Turing Machine Simulator',
            'Binary Search Question',
            ['Run', 'Github'],
            ['1', '2', '3'],
            [FIF.PLAY, FIF.GITHUB, FIF.ADD, FIF.ADD, FIF.ADD],
            self.addFunctions,
            parent=parent
        )
        self.setObjectName(text.replace(' ', '-'))
        self.input = InputTape(self)

        self.addExampleCard('Input Tape', self.input, [FIF.ADD, FIF.REMOVE], [self.input.addItem, self.input.removeItem], 1)

    def simulate(self):
        
        ...
        
        InfoBar.success(
            title='开始仿真！\nStart!',
            content='''
            载入成功，现在开始仿真，注意哦，输入的纸袋将以如下形式给出：
            Loaded Successfully, now let's start the simulation. Note that the input paper bag will be given in the following form:\n
            input tape:[n, k, a_0, a_2 , ..., a_{n-1}]
            ''',
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=4000,
            parent=self
        )

    def addFunctions(self):
        function_list = []
        
        def run():
            content = '''
                这里是图灵机仿真迭代二分搜索算法！
                给我一个排列好的n元素数组与你的目标值k，我将演示并且给出k的索引，找不到的话给出-1。
                明白了后，你可以修改初始的纸带，然后就让我们点击开始吧！\n
                Hi there is a Turing machine simulator for binary search question! 
                Give me an array of aligned n elements with your target value k. I will demonstrate and give you the index of k, and -1 if you can't find it. 
                Once you understand that, you can modify the initial paper tape and then let's click start!
            '''
            w = InfoBar(
                icon=InfoBarIcon.INFORMATION,
                title='Title',
                content=content,
                orient=Qt.Vertical,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=10000,
                parent=self
            )
            btn = PushButton('明白了\nI see')
            btn.clicked.connect(self.simulate)
            w.addWidget(btn)
            w.show()
        
        function_list.append(run)
        function_list.append(None)
        function_list.append(None)
        function_list.append(None)
        function_list.append(None)
        return function_list
