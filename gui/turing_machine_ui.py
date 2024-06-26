import re

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

        self.initial()

    def initial(self):
        self.infos = ['10', '5', '0', '1', '2', '3', '4', '6', '7', '8', '9', '10']
        self.reset()

    def reset(self):
        try:
            self.setColumnCount(len(self.infos))
            self.setRowCount(1)
            header = []
            for i in range(len(self.infos)):
                self.setItem(0, i, QTableWidgetItem(self.infos[i]))
                header.append(f'a{i-2}')
            self.setItem(0, 0, QTableWidgetItem(str(len(self.infos)-2)))
            header[0] = 'n'
            header[1] = 'k'
            self.setHorizontalHeaderLabels(header)
            # self.resizeColumnsToContents()
            # self.resizeRowsToContents()
        except:
            return

    def getInfos(self):
        self.infos = []
        for i in range(self.columnCount()):
            item = self.item(0, i)
            if item is not None:
                self.infos.append(item.text())

    def addItem(self):
        self.getInfos()
        self.infos.append(None)
        self.setItem(0, len(self.infos)-1, QTableWidgetItem(None))
        self.reset()

    def removeItem(self):
        self.getInfos()
        try:
            assert len(self.infos) > 2
            self.infos.pop()
        except:
            InfoBar.warning(
                title='空\nEmpty',
                content='纸带已空！\nThe tape is empty!',
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.TOP_LEFT,
                duration=2000,
                parent=self
            )
        self.reset()



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

        self.addExampleCard('Input Tape', self.input, [FIF.ADD, FIF.REMOVE, FIF.ROTATE], [self.input.addItem, self.input.removeItem, self.input.initial], 1)

    def simulate(self):
        try:
            self.input.getInfos()
            self.arr = [int(i) for i in self.input.infos]
            self.arr.pop(0)
            self.arr.pop(0)

            ...
            
        except Exception as e:
            InfoBar.error(
                title='失败了！\nFailed!',
                content=f'请检查输入是否正确！\nPlease check if the input is correct!\n\nError:\n{str(e)}',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.BOTTOM_RIGHT,
                duration=-1,
                parent=self
            )
            return
        
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
        function_list.append(self.run)
        function_list.append(None)
        function_list.append(None)
        function_list.append(None)
        function_list.append(None)
        return function_list

    def run(self):
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
