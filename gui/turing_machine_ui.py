import re

from .template.interface import Interface
from PySide6.QtCore import QPoint, Qt
from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget, QApplication, QListWidgetItem, QListWidget, QHBoxLayout
from PySide6.QtWidgets import QTreeWidgetItem, QHBoxLayout, QTreeWidgetItemIterator, QTableWidgetItem, QListWidgetItem
from qfluentwidgets import InfoBarIcon, InfoBar, PushButton, setTheme, Theme, FluentIcon, InfoBarPosition, InfoBarManager
from qfluentwidgets import TreeWidget, TableWidget, ListWidget, HorizontalFlipView, ListView
from qfluentwidgets import FluentIcon as FIF



class InitialTape(TableWidget):
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



class Tape(TableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.verticalHeader().hide()
        self.setBorderRadius(8)
        self.setBorderVisible(True)
        self.infos = [[], [], []]

    def set(self, arr):
        self.infos = arr
        self.setRowCount(len(self.infos))
        self.setColumnCount(max(len(self.infos[0]), len(self.infos[1]), len(self.infos[2]))+1)
        
        self.setItem(0, 0, QTableWidgetItem('#input tape:'))
        self.setItem(1, 0, QTableWidgetItem('#work tape:'))
        self.setItem(2, 0, QTableWidgetItem('#output tape:'))
        
        for i in range(len(self.infos)):
            for j in range(len(self.infos[i])):
                self.setItem(i, j+1, QTableWidgetItem(str(self.infos[i][j])))
        
        self.resizeColumnsToContents()
        self.resizeRowsToContents()



class TuringMachineUI(Interface):
    def __init__(self, text: str, parent=None):
        super().__init__(
            'Turing Machine Simulator',
            'Binary Search Question',
            ['Run', 'Github'],
            ['Forward', 'Reset', 'Next'],
            [FIF.PLAY, FIF.GITHUB, FIF.LEFT_ARROW, FIF.SYNC, FIF.RIGHT_ARROW],
            self.addFunctions,
            parent=parent
        )
        self.setObjectName(text.replace(' ', '-'))
        self.simulating = False
        self.initial = InitialTape(self)
        self.tape = Tape(self)
        self.history = []
        self.list = ListWidget(self)

        self.addExampleCard('Initial Tape', self.initial, [FIF.ADD, FIF.REMOVE, FIF.ROTATE], [self.initial.addItem, self.initial.removeItem, self.initial.initial], 1)
        self.addExampleCard('Tapes', self.tape, [], [], 1)
        self.addExampleCard('History', self.list, [], [], 1)

    def simulate(self):
        try:
            self.arr = [[], [], []]
            self.initial.getInfos()
            self.arr[0].append(0)
            self.arr[0] += [int(i) for i in self.initial.infos]
            self.arr[0][1] -= 1

            self.history.append(self.arr)
            self.tape.set(self.arr)

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
        
        self.simulating = True
        InfoBar.success(
            title='开始仿真！\nStart!',
            content='''
                载入成功，现在开始仿真。
                Loaded Successfully, now let's start the simulation. 
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
        btn = PushButton('明白了，开始吧    I see and let\'s go!')
        btn.clicked.connect(self.simulate)
        w.addWidget(btn)
        w.show()
