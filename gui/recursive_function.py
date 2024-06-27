from .template.interface import Interface
from .template.tape import Tape, InitialTape
from PySide6.QtCore import QUrl, QPoint, Qt
from PySide6.QtGui import QDesktopServices, QColor, QFont
from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget, QApplication, QListWidgetItem, QListWidget, QHBoxLayout
from PySide6.QtWidgets import QTreeWidgetItem, QHBoxLayout, QTreeWidgetItemIterator, QTableWidgetItem, QListWidgetItem
from qfluentwidgets import InfoBarIcon, InfoBar, PushButton, setTheme, Theme, FluentIcon, InfoBarPosition, InfoBarManager
from qfluentwidgets import TreeWidget, TableWidget, ListWidget, HorizontalFlipView, ListView
from qfluentwidgets import FluentIcon as FIF

URL = 'https://github.com/Miki-Riako/TR-Simulator/blob/main/gui/recursive_function.py'



class RecursiveFunction(Interface):
    def __init__(self, text: str, parent=None):
        super().__init__(
            'Recursive Function Simulator',
            'Binary Search Question',
            ['Run', 'Github'],
            ['Forward', 'Reset', 'Next'],
            [FIF.PLAY, FIF.GITHUB, FIF.LEFT_ARROW, FIF.SYNC, FIF.RIGHT_ARROW],
            self.addFunctions,
            parent=parent
        )
        self.setObjectName(text.replace(' ', '-'))
        self.simulating = False
        self.initial = InitialTape(['10', '5', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], self)
        self.tape = Tape(self)
        self.bottomLayout = QHBoxLayout()
        self.bottom = QWidget()
        self.bottom.setLayout(self.bottomLayout)
        self.list = ListWidget(self)
        self.stack = TableWidget(self)
        self.stack.setBorderVisible(True)
        self.stack.setBorderRadius(8)
        self.stack.setWordWrap(False)
        self.stack.setColumnCount(3)
        self.stack.setHorizontalHeaderLabels(['Low', 'High', 'Mid'])
        self.bottomLayout.addWidget(self.list, 8)
        self.bottomLayout.addWidget(self.stack, 2)
        self.arr = [[], [], []]
        self.cur = [-1, -1, -1]
        self.next_state = 'function'

        self.addExampleCard('Initial Tape', self.initial, [FIF.ADD, FIF.REMOVE, FIF.ROTATE], [self.initial.addItem, self.initial.removeItem, self.initial.initial], 1)
        self.addExampleCard('Tapes', self.tape, [], [], 1)
        self.addExampleCard('History', self.bottom, [], [], 1)

    def simulate(self):
        try:
            self.arr = [[], [], []]
            self.initial.getInfos()
            self.arr[0].append(0)
            self.arr[0] += [int(i) for i in self.initial.infos]
            self.arr[0][1] -= 1

            self.tape.clear()
            self.stack.clear()
            self.list.clear()
            self.tape.set(self.arr)
            self.cur = [-1, -1, -1]
            self.next_state = 'readLow'
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
        function_list.append(lambda: QDesktopServices.openUrl(QUrl(URL)))
        function_list.append(self.forward)
        function_list.append(self.reset)
        function_list.append(self.next)
        return function_list

    def run(self):
        content = '''
            这里是图灵机仿真递归二分搜索算法！
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
            self.stack.clear()
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

    def forward(self):
        self.showInfo('进入了还未实现的 0&1 世界。')

    def next(self):
        if not self.simulating:
            self.tape.set(self.arr)
            self.tape.current(self.cur)
            return
        getattr(self, self.next_state)()
        self.tape.set(self.arr)
        self.tape.current(self.cur)
    
    def readLow(self):
        self.showInfo('读取低位\nReading low bit')
        self.cur[0] = 0
        self.next_state = 'compareHigh'
        self.list.addItem(QListWidgetItem(f'Low index {self.arr[0][0]}.'))
    
    def compareHigh(self):
        self.showInfo('比较高位\nComparing high bit')
        self.cur[0] = 1
        self.next_state = 'calMid'
        self.list.addItem(QListWidgetItem(f'Compare {self.arr[0][0]} and {self.arr[0][1]}.'))
    
    def calMid(self):
        self.showInfo('计算中位\nCalculating mid bit')
        if len(self.arr[1]) < 1:
            self.arr[1].append((self.arr[0][0] + self.arr[0][1]) // 2)
        else:
            self.arr[1][0] = (self.arr[0][0] + self.arr[0][1]) // 2
        self.cur[1] = 0
        self.next_state = 'readK'
        self.list.addItem(QListWidgetItem(f'Calculate the index ({self.arr[0][0]} + {self.arr[0][1]}) // 2 = {self.arr[1][0]}.'))
    
    def readK(self):
        self.showInfo('读取目标值\nReading target value')
        self.cur[0] = 2
        self.next_state = 'readMid'
        self.list.addItem(QListWidgetItem(f'Search {self.arr[0][2]}.'))
    
    def readMid(self):
        self.showInfo('读取中位\nReading mid bit')
        self.cur[0] += 1
        if self.cur[0] == self.arr[1][0] + 3:
            self.next_state = 'compareMid'
            self.list.addItem(QListWidgetItem(f'Read Index {self.arr[1][0]} and get {self.arr[0][self.arr[1][0] + 3]}.'))
    
    def compareMid(self):
        now = self.arr[0][self.arr[1][-1] + 3]
        self.cur[0] = self.arr[1][0] + 3
        self.cur[1] = 0
        if now < self.arr[0][2]:
            self.showInfo(f'比较中位\nComparing mid bit\n{now} < {self.arr[0][2]}')
            self.next_state = 'call'
            self.list.addItem(QListWidgetItem(f'Compare {now} < {self.arr[0][2]}. Call recursive function.'))
        elif now > self.arr[0][2]:
            self.showInfo(f'比较中位\nComparing mid bit\n{now} > {self.arr[0][2]}')
            self.next_state = 'call'
            self.list.addItem(QListWidgetItem(f'Compare {now} > {self.arr[0][2]}. Call recursive function.'))
        else:
            self.showInfo(f'比较中位\nComparing mid bit\n{now} = {self.arr[0][2]}')
            self.found = True
            self.next_state = 'end'
            self.list.addItem(QListWidgetItem(f'Compare {now} = {self.arr[0][2]}. End.'))
    
    def call(self):
        self.showInfo('调用递归函数')
        if self.cur[0] > 0:
            self.cur[0] -= 1
        else:
            now = self.arr[0][self.arr[1][0]+2]
            low = self.arr[0][0] if self.arr[0][2] < now else self.arr[1][0] + 1
            high = self.arr[0][1] if self.arr[0][2] > now else self.arr[1][0] - 1
            if low == high:
                self.found = False
                self.end()
                return
            self.tape.set(self.arr)
            self.tape.current(self.cur)
            self.stack.setRowCount(self.stack.rowCount() + 1)
            self.stack.setItem(self.stack.rowCount()-1, 0, QTableWidgetItem(str(self.arr[0][0])))
            self.stack.setItem(self.stack.rowCount()-1, 1, QTableWidgetItem(str(self.arr[0][1])))
            self.stack.setItem(self.stack.rowCount()-1, 2, QTableWidgetItem(str(self.arr[1][0])))
            self.arr[0][0] = low
            self.arr[0][1] = high
            self.arr[1].pop
            self.tape.set(self.arr)
            self.next_state = 'readLow'
            self.list.addItem(QListWidgetItem('Call recursive function.'))

    def end(self):
        self.showInfo('结束\nEnd')
        if self.found:
            self.arr[2].append(self.arr[0][2])
            self.list.addItem(QListWidgetItem(f'Found {self.arr[0][2]} at Index {self.arr[1][0] + 3}.'))
        else:
            self.arr[2].append(-1)
            self.list.addItem(QListWidgetItem(f'Not found {self.arr[0][2]}.'))
        self.cur[2] = 0
        self.simulating = False
