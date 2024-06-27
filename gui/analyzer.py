from .template.interface import Interface
from .template.tape import Tape, InitialKnapsackTape
from PySide6.QtCore import QUrl, QPoint, Qt
from PySide6.QtGui import QDesktopServices, QColor, QFont
from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget, QApplication, QListWidgetItem, QListWidget, QHBoxLayout
from PySide6.QtWidgets import QTreeWidgetItem, QHBoxLayout, QTreeWidgetItemIterator, QTableWidgetItem, QListWidgetItem
from qfluentwidgets import InfoBarIcon, InfoBar, PushButton, setTheme, Theme, FluentIcon, InfoBarPosition, InfoBarManager
from qfluentwidgets import TreeWidget, TableWidget, ListWidget, HorizontalFlipView, ListView
from qfluentwidgets import FluentIcon as FIF

URL = 'https://github.com/Miki-Riako/TR-Simulator/blob/main/gui/analyzer.py'



class Analyzer(Interface):
    def __init__(self, text: str, parent=None):
        super().__init__(
            'Performance Analysis',
            'Knapsack Question',
            ['Run', 'Github'],
            ['动态规划\nDynamic programming', '分支界限\nBranches', '备忘录\nMemorandum', '回溯\nLook back upon','Forward', 'Reset', 'Next'],
            [FIF.PLAY, FIF.GITHUB, FIF.MOVE, FIF.TILES, FIF.DICTIONARY, FIF.HISTORY, FIF.LEFT_ARROW, FIF.SYNC, FIF.RIGHT_ARROW],
            self.addFunctions,
            parent=parent
        )
        self.setObjectName(text.replace(' ', '-'))
        self.simulating = False
        self.initial = InitialKnapsackTape(['5', '4', '2', '1', '3', '2', '12', '10', '20', '15'], self)
        self.tape = Tape(self)
        self.bottomLayout = QHBoxLayout()
        self.bottom = QWidget()
        self.bottom.setLayout(self.bottomLayout)
        self.list = ListWidget(self)
        self.table = TableWidget(self)
        self.table.setBorderVisible(True)
        self.table.setBorderRadius(8)
        self.table.setWordWrap(False)
        self.table.setColumnCount(4)
        self.table.setRowCount(4)
        self.bottomLayout.addWidget(self.list, 8)
        self.bottomLayout.addWidget(self.table, 2)
        self.arr = [[], [], []]
        self.cur = [-1, -1, -1]
        self.step = 0
        self.next_state = 'readCapacity'
        self.mode = 0

        self.addExampleCard('Initial Tape', self.initial, [FIF.ADD, FIF.REMOVE, FIF.ROTATE], [self.initial.addItem, self.initial.removeItem, self.initial.initial], 1)
        self.addExampleCard('Tapes', self.tape, [], [], 1)
        self.addExampleCard('History', self.bottom, [], [], 1)
    
    def setMode(self, mode):
        self.mode = mode
        InfoBar.success(
            title='已切换模式\nMode Changed',
            content=f'已切换到{["动态规划", "分支界限", "备忘录", "回溯"][mode]}模式\nSwitched to {["Dynamic programming", "Branches", "Memorandum", "Look back upon"][mode]} mode',
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )
    
    def index(self, x, y):
        return x + y * self.cur[0][1]

    def simulate(self):
        try:
            self.arr = [[], [], []]
            self.initial.getInfos()
            self.arr[0].append(self.initial.c)
            self.arr[0].append(self.initial.n)
            for i in range(self.arr[0][1]):
                self.arr[0].append(int(self.initial.infos_w[i]))
                self.arr[0].append(int(self.initial.infos_v[i]))
                # self.arr[1].append(None for _ in range(self.arr[0][1]))
                self.arr[1].append(None)
            self.arr[1] = [''] * self.arr[0][1] * self.arr[0][1]
            self.arr[2] = [0] * self.arr[0][1]
            self.tape.clear()
            self.table.clear()
            self.table.setColumnCount(self.arr[0][1])
            self.table.setRowCount(self.arr[0][1])
            self.list.clear()
            self.tape.set(self.arr)
            self.cur = [-1, -1, -1]
            self.step = 0
            self.next_state = 'readCapacity'
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
        function_list.append(lambda: self.setMode(0))
        function_list.append(lambda: self.setMode(1))
        function_list.append(lambda: self.setMode(2))
        function_list.append(lambda: self.setMode(3))
        function_list.append(self.forward)
        function_list.append(self.reset)
        function_list.append(self.next)
        return function_list

    def run(self):
        content = '''
            这里是0/1背包问题性能分析！
            给我n元素重量和价值与你的容量c，我将演示并且给出最优解。
            明白了后，你可以修改初始的纸带，然后就让我们点击开始吧！\n
            Hi there is a Performance Analysis of the 0/1 Knapsack question! 
            Give me the weight and value of n elements with your capacity c and I will demonstrate and give the optimal solution.
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
            self.step = 0
            self.tape.clear()
            self.list.clear()
            self.table.clear()
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
            # self.table.setRowCount(self.table.rowCount() + 1)
            # self.table.setItem(self.table.rowCount()-1, 0, QTableWidgetItem(str(self.arr[0][0])))
            # self.table.setItem(self.table.rowCount()-1, 1, QTableWidgetItem(str(self.arr[0][1])))
            # self.table.setItem(self.table.rowCount()-1, 2, QTableWidgetItem(str(self.arr[1][0])))
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
