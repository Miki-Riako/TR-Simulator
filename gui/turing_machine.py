import re

from .template.interface import Interface
from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QColor, QFont
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
            self.resizeColumnsToContents()
            self.resizeRowsToContents()
            for column in range(self.columnCount()):
                self.setColumnWidth(column, self.columnWidth(column) + 10)
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
        for column in range(self.columnCount()):
            self.setColumnWidth(column, self.columnWidth(column) + 10)
        
        self.default()

    def default(self):
        for row in range(self.rowCount()):
            for column in range(self.columnCount()):
                item = self.item(row, column)
                if item:
                    item.setForeground(QColor(Qt.white))
                    item.setFont(QFont())
    
    def current(self, triplet):
        self.default()
        for i in range(3):
            if triplet[i] == -1:
                continue
            item = self.item(i, triplet[i]+1)
            if item:
                item.setForeground(QColor(Qt.cyan))
                item.setFont(QFont('Arial', 13, QFont.Bold))



class TuringMachine(Interface):
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
        self.list = ListWidget(self)
        self.cur = [-1, -1, -1]
        self.next_state = 'initLow'

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

            self.tape.clear()
            self.tape.set(self.arr)
            self.cur = [-1, -1, -1]
            self.next_state = 'initLow'
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
                duration=3999,
                parent=self
            )
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

    def addFunctions(self):
        function_list = []
        function_list.append(self.run)
        function_list.append(None)
        function_list.append(None)
        function_list.append(self.reset)
        function_list.append(self.next)
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

    def showInfo(self, text):
        InfoBar.success(
            title='Next',
            content=text,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )

    def reset(self):
        content = '''
            这样的话要重新仿真哦，确定吗？\n
            If you want to reset, are you sure?
        '''
        w = InfoBar(
            icon=InfoBarIcon.INFORMATION,
            title='Sure?',
            content=content,
            orient=Qt.Vertical,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=4000,
            parent=self
        )
        btn = PushButton('是的    Yes, let\'s go!')
        def r():
            self.simulating = False
            self.tape.clear()
            self.list.clear()
            InfoBar.success(
                title='重置了！\nReset!',
                content="已重置图灵机。\nThe Turing machine has been reset.",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
        btn.clicked.connect(r)
        w.addWidget(btn)
        w.show()

    def next(self):
        if not self.simulating:
            self.tape.set(self.arr)
            self.tape.current(self.cur)
            return
        getattr(self, self.next_state)()
        self.tape.set(self.arr)
        self.tape.current(self.cur)

    def initLow(self):
        self.showInfo('初始化低位\nInitializing low bit')
        self.cur[0] = 0
        self.next_state = 'writeLow'
        self.list.addItem(QListWidgetItem(f'Get {self.arr[0][0]}.'))
    
    def initHigh(self):
        self.showInfo('初始化高位\nInitializing high bit')
        self.cur[0] = 1
        self.next_state = 'writeHigh'
        self.list.addItem(QListWidgetItem(f'Get {self.arr[0][1]}.'))
    
    def writeLow(self):
        self.showInfo('写入低位\nWriting low bit')
        self.arr[1].append(self.arr[0][0])
        self.cur[1] = 0
        self.next_state = 'initHigh'
        self.list.addItem(QListWidgetItem(f'Write {self.arr[0][0]} as low bit.'))
    
    def writeHigh(self):
        self.showInfo('写入高位\nWriting high bit')
        self.arr[1].append(self.arr[0][1])
        self.cur[1] = 1
        self.next_state = 'compareLow'
        self.list.addItem(QListWidgetItem(f'Write {self.arr[0][1]} as high bit.'))
    
    def compareLow(self):
        self.showInfo('比较低位\nComparing low bit')
        self.cur[1] = 0
        if self.arr[1][0] > self.arr[1][1]:
            self.next_state = 'stop'
            self.list.addItem(QListWidgetItem(f'Compare {self.arr[1][0]} > {self.arr[1][1]}. Stop.'))
        else:
            self.fount = False
            self.next_state = 'calMid'
            self.list.addItem(QListWidgetItem(f'Compare {self.arr[1][0]} and {self.arr[1][1]}.'))
    
    def compareMid(self):
        now = self.arr[0][self.arr[1][-1] + 3]
        self.cur[0] = self.arr[1][-1] + 3
        self.cur[1] = len(self.arr[1]) - 1
        if now < self.arr[0][2]:
            self.showInfo(f'比较中位\nComparing mid bit\n{now} < {self.arr[0][2]}')
            self.next_state = 'updateLow'
            self.list.addItem(QListWidgetItem(f'Compare {now} < {self.arr[0][2]}. Go to update low bit.'))
        elif now > self.arr[0][2]:
            self.showInfo(f'比较中位\nComparing mid bit\n{now} > {self.arr[0][2]}')
            self.next_state = 'updateHigh'
            self.list.addItem(QListWidgetItem(f'Compare {now} > {self.arr[0][2]}. Go to update high bit.'))
        else:
            self.showInfo(f'比较中位\nComparing mid bit\n{now} = {self.arr[0][2]}')
            self.found = True
            self.next_state = 'stop'
            self.list.addItem(QListWidgetItem(f'Compare {now} = {self.arr[0][2]}. Stop.'))
    
    def compareHigh(self):
        self.showInfo('比较高位\nComparing high bit')
        self.cur[1] = 1
        if self.arr[1][0] > self.arr[1][1]:
            self.next_state = 'stop'
            self.list.addItem(QListWidgetItem(f'Compare {self.arr[1][0]} > {self.arr[1][1]}. Stop.'))
        else:
            self.found = False
            self.next_state = 'calMid'
            self.list.addItem(QListWidgetItem(f'Compare {self.arr[1][0]} and {self.arr[1][1]}.'))
    
    def calMid(self):
        self.showInfo('计算中位\nCalculating mid bit')
        if len(self.arr[1]) < 3:
            self.arr[1].append((self.arr[1][0] + self.arr[1][1]) // 2)
        else:
            self.arr[1][2] = (self.arr[1][0] + self.arr[1][1]) // 2
        self.cur[1] = 2
        self.next_state = 'readK'
        self.list.addItem(QListWidgetItem(f'Calculate the index ({self.arr[1][0]} + {self.arr[1][1]}) // 2 = {self.arr[1][-1]}.'))
    
    def readK(self):
        self.showInfo('读取目标值\nReading target value')
        self.cur[0] = 2
        self.next_state = 'readMid'
        self.list.addItem(QListWidgetItem(f'Search {self.arr[0][2]}.'))
    
    def readMid(self):
        self.showInfo('读取中位\nReading mid bit')
        self.cur[0] = self.arr[1][-1] + 3
        self.next_state = 'compareMid'
        self.list.addItem(QListWidgetItem(f'Read Index {self.arr[1][-1] + 3} and get {self.arr[0][self.arr[1][-1] + 3]}.'))
    
    def updateLow(self):
        self.showInfo('更新低位\nUpdating low bit')
        self.cur[1] = 0
        old = self.arr[1][0]
        self.arr[1][0] = self.arr[1][-1] + 1
        self.next_state = 'compareHigh'
        self.list.addItem(QListWidgetItem(f'Update Index {old} to {self.arr[1][0]}.'))
    
    def updateHigh(self):
        self.showInfo('更新高位\nUpdating high bit')
        self.cur[1] = 1
        old = self.arr[1][1]
        self.arr[1][1] = self.arr[1][-1] - 1
        self.next_state = 'compareLow'
        self.list.addItem(QListWidgetItem(f'Update Index {old} to {self.arr[1][1]}.'))
    
    def stop(self):
        self.showInfo('停止\nStopping')
        if self.found:
            self.arr[2].append(self.arr[0][2])
            self.list.addItem(QListWidgetItem(f'Found {self.arr[0][2]} at Index {self.arr[1][-1] + 3}.'))
        else:
            self.arr[2].append(-1)
            self.list.addItem(QListWidgetItem(f'Not found {self.arr[0][2]}.'))
        self.cur[2] = 0
        self.simulating = False
