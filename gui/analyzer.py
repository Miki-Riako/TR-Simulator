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
DEBUG_MODE = False
NEXT = 450


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
        self.table.setColumnCount(6)
        self.table.setRowCount(4)
        self.bottomLayout.addWidget(self.list, 7)
        self.bottomLayout.addWidget(self.table, 3)
        self.arr = [[], [], []]
        self.cur = [-1, -1, -1]
        self.step = 0
        self.next_state = 'readCapacity'
        self.mode = 0
        if DEBUG_MODE:
            self.simulate()
            for _ in range(NEXT):
                self.next()

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
        return x * (self.arr[0][0]+1) + y

    def pushStack(self):
        self.table.setRowCount(self.table.rowCount()+1)
        self.table.setItem(self.table.rowCount()-1, 0, QTableWidgetItem(str(self.depth)))
        self.table.setItem(self.table.rowCount()-1, 1, QTableWidgetItem(str(self.value)))

    def getNum(self, index, local):
        if self.cur[index] < local:
            self.cur[index] += 1
            return False
        elif self.cur[index] > local:
            self.cur[index] -= 1
            return False
        else:
            return True

    def simulate(self):
        try:
            self.arr = [[], [], []]
            self.initial.getInfos()
            self.arr[0].append(self.initial.c)
            self.arr[0].append(self.initial.n)
            for i in range(self.arr[0][1]):
                self.arr[0].append(int(self.initial.infos_w[i]))
                self.arr[0].append(int(self.initial.infos_v[i]))
            self.arr[1] = []
            self.arr[2] = [0] * self.arr[0][1]
            self.tape.clear()
            self.table.clear()
            self.list.clear()
            self.tape.set(self.arr)
            self.cur = [-1, -1, -1]
            self.step = 0
            self.simulating = True
            
            if self.mode == 0:
                self.dp = [[0]*(self.arr[0][0]+1) for _ in range(self.arr[0][1])]
                self.nowCol = 0
                self.nowRow = self.arr[0][1] - 1
                self.calculated = False
                self.table.setColumnCount(self.arr[0][0]+1)
                self.table.setRowCount(self.arr[0][1])
                for i in range(self.arr[0][1]):
                    for j in range(self.arr[0][0]+1):
                        self.table.setItem(i, j, QTableWidgetItem('0'))
                self.next_state = 'readCapacity'
            else:
                self.bestV = 0
                self.curW = 0
                self.curV = 0
                self.table.setColumnCount(2)
                self.table.setRowCount(0)
                self.table.setHorizontalHeaderLabels(['Depth', 'Value'])
                self.next_state = 'backtrackBegin'

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
        self.step += 1
        getattr(self, self.next_state)()
        self.tape.set(self.arr)
        self.tape.current(self.cur)
    
    def readCapacity(self):
        self.showInfo(f'读取容量\nReading capacity\nStep {self.step}')
        self.cur[0] = 0
        self.next_state = 'readNum'
        self.list.addItem(QListWidgetItem(f'Reading capacity {self.arr[0][0]}.'))
    
    def readNum(self):
        self.showInfo(f'读取数字\nReading number\nStep {self.step}')
        self.cur[0] = 1
        self.next_state = 'readWeight'
        self.list.addItem(QListWidgetItem(f'Reading number {self.arr[0][0]}.'))
    
    def readWeight(self):
        self.showInfo(f'读取重量\nReading weight\nStep {self.step}')
        if self.cur[0] < 2*self.nowRow+2:
            self.cur[0] += 1
        elif self.cur[0] > 2*self.nowRow+2:
            self.cur[0] -= 1
        else:
            self.next_state = 'readValue'
            self.list.addItem(QListWidgetItem(f'Reading weight {self.arr[0][self.cur[0]]}.'))
    
    def readValue(self):
        self.showInfo(f'读取价值\nReading value\nStep {self.step}')
        self.cur[0] += 1
        self.next_state = 'writeM'
        self.list.addItem(QListWidgetItem(f'Reading value {self.arr[0][self.cur[0]]}.'))
    
    def writeM(self):
        self.showInfo(f'写入DP数组\nWriting DP Matrix\nStep {self.step}')
        if self.nowRow == self.arr[0][1]-1 or self.cur[1] == self.nowCol:
            if self.nowCol < self.arr[0][0]+1:
                nowWeight = self.arr[0][self.cur[0]-1]
                nowValue = self.arr[0][self.cur[0]]
                if self.nowRow == self.arr[0][1]-1:
                    self.dp[self.nowRow][self.nowCol] = nowValue if nowWeight <= self.nowCol else 0
                    self.table.setItem(self.nowRow, self.nowCol, QTableWidgetItem(str(self.dp[self.nowRow][self.nowCol])))
                    self.next_state = 'writeM'
                else:
                    self.next_state = 'readM'
                self.arr[1].insert(self.nowCol, self.dp[self.nowRow][self.nowCol])
                self.cur[1] = self.nowCol
                self.list.addItem(QListWidgetItem(f'Writing DP Matrix {self.dp[self.nowRow][self.nowCol]}.'))
                self.nowCol += 1
            if self.nowCol >= self.arr[0][0]+1:
                self.nowCol = 0
                if self.nowRow == 0:
                    self.optimal = [0, self.arr[0][0]]
                    self.next_state = 'readW'
                else:
                    self.nowRow -= 1
                    self.next_state = 'readWeight'
        elif self.cur[1] < self.nowCol:
            self.cur[1] += 1
        else:
            self.cur[1] -= 1
    
    def readM(self):
        self.showInfo(f'读取DP数组\nRead DP Matrix\nStep {self.step}')
        if self.cur[1] < 2*self.nowCol:
            self.cur[1] += 1
        elif self.cur[1] > 2*self.nowCol:
            self.cur[1] -= 1
        else:
            nowWeight = self.arr[0][self.cur[0]-1]
            if self.nowCol >= nowWeight:
                self.next_state = 'calM'
            else:
                self.dp[self.nowRow][self.nowCol] = self.dp[self.nowRow+1][self.nowCol]
                self.table.setItem(self.nowRow, self.nowCol, QTableWidgetItem(str(self.dp[self.nowRow][self.nowCol])))
                self.next_state = 'writeM'
            self.list.addItem(QListWidgetItem(f'Reading DP Matrix {self.dp[self.nowRow][self.nowCol]}.'))
    
    def calM(self):
        self.showInfo(f'计算DP数组\nCalculate DP Matrix\nStep {self.step}')
        if self.cur[1] < len(self.arr[1])-1:
            self.cur[1] += 1
        elif self.cur[1] > len(self.arr[1])-1:
            self.cur[1] -= 1
        else:
            nowWeight = self.arr[0][self.cur[0]-1]
            nowValue = self.arr[0][self.cur[0]]
            self.choose = self.dp[self.nowRow+1][self.nowCol-nowWeight] + nowValue
            if self.calculated:
                self.arr[1][len(self.arr[1])-1] = self.choose
            else:
                self.arr[1].append(self.choose)
            self.cur[1] += 1
            self.calculated = True
            self.next_state = 'cmp'
            self.list.addItem(QListWidgetItem(f'Calculate DP Matrix {self.choose} if chosen.'))
    
    def cmp(self):
        self.showInfo(f'比较DP数组\nCompare DP Matrix\nStep {self.step}')
        if self.dp[self.nowRow+1][self.nowCol] > self.choose:
            self.dp[self.nowRow][self.nowCol] = self.dp[self.nowRow+1][self.nowCol]
            self.table.setItem(self.nowRow, self.nowCol, QTableWidgetItem(str(self.dp[self.nowRow][self.nowCol])))
            self.list.addItem(QListWidgetItem(f'Compare DP Matrix {self.dp[self.nowRow+1][self.nowCol]} > {self.choose}.'))
        else:
            self.dp[self.nowRow][self.nowCol] = self.choose
            self.table.setItem(self.nowRow, self.nowCol, QTableWidgetItem(str(self.dp[self.nowRow][self.nowCol])))
            self.list.addItem(QListWidgetItem(f'Compare DP Matrix {self.dp[self.nowRow+1][self.nowCol]} >= {self.choose}.'))
        self.next_state = 'writeM'
    
    def readW(self):
        self.showInfo(f'读取物品重量\nRead Weight\nStep {self.step}')
        if self.cur[0] < 2*self.nowRow+2:
            self.cur[0] += 1
        elif self.cur[0] > 2*self.nowRow+2:
            self.cur[0] -= 1
        else:
            self.next_state = 'ansM'
            self.list.addItem(QListWidgetItem(f'Reading Weight {self.arr[0][self.cur[0]]}.'))
    
    def ansM(self):
        self.showInfo(f'回溯最优解\nBacktracking\nStep {self.step}')
        if self.cur[1] < self.index(self.optimal[0], self.optimal[1]):
            self.cur[1] += 1
        elif self.cur[1] > self.index(self.optimal[0], self.optimal[1]):
            self.cur[1] -= 1
        else:
            self.next_state = 'cmpAnsM'
            self.list.addItem(QListWidgetItem(f'Backtracking {self.arr[1][self.cur[1]]}.'))
    
    def cmpAnsM(self):
        self.showInfo(f'比较最优解\nCompare Answer\nStep {self.step}')
        if self.cur[1] < self.index(self.optimal[0]+1, self.optimal[1]):
            self.cur[1] += 1
        elif self.cur[1] > self.index(self.optimal[0]+1, self.optimal[1]):
            self.cur[1] -= 1
        else:
            if self.optimal[0] == self.arr[0][1]-1:
                if self.dp[self.optimal[0]][self.optimal[1]] != 0:
                    self.next_state = 'writeAns'
                else:
                    self.cur[2] += 1
                    self.next_state = 'success'
            elif self.dp[self.optimal[0]][self.optimal[1]] != self.dp[self.optimal[0]+1][self.optimal[1]]:
                self.optimal[0] += 1
                self.optimal[1] -= self.arr[0][self.cur[0]]
                self.next_state = 'writeAns'
            else:
                self.optimal[0] += 1
                self.nowRow += 1
                self.cur[2] += 1
                self.next_state = 'readW'
    
    def writeAns(self):
        self.showInfo(f'写入最优解\nWrite Answer\nStep {self.step}')
        self.arr[2][self.nowRow] = 1
        self.cur[2] = self.nowRow
        if self.nowRow == self.arr[0][1]-1:
            self.next_state = 'success'
        else:
            self.nowRow += 1
            self.next_state = 'readW'
        self.list.addItem(QListWidgetItem(f'Write Answer {self.arr[2][self.nowRow-1]}.'))
    
    def success(self):
        self.showInfo(f'成功\nSuccess')
        self.list.addItem(QListWidgetItem(f'The optimal solution is {self.dp[0][self.arr[0][0]]}.'))
        self.simulating = False







    def backtrackBegin(self):
        self.showInfo(f'回溯开始\nBacktracking Begin\nStep {self.step}')
        self.arr[1].append(self.bestV)
        self.arr[1].append(self.curW)
        self.arr[1].append(self.curV)
        self.value = 0
        self.depth = 0
        self.pushStack()
        self.cur = [0, 0, 0]
        self.stack = []
        self.next_state = 'backtrack'
        self.list.addItem(QListWidgetItem(f'Call f({self.value}).'))
    
    def backtrack(self):
        self.showInfo(f'回溯\nBacktracking\nStep {self.step}')
        if self.getNum(0, 2):
            if self.value >= self.arr[0][1]:
                self.next_state = 'back'
                self.list.addItem(QListWidgetItem(f'Compare Value {self.arr[0][1]} and go back.'))
            else:
                self.next_state = 'traverse'
                self.list.addItem(QListWidgetItem(f'Compare Weight {self.arr[0][1]} and go next.'))
    
    def back(self):
        self.showInfo(f'回溯至最初\nBacktracking\nStep {self.step}')
        ...
    
    def traverse(self):
        self.showInfo(f'继续\nTraversing next\nStep {self.step}')
        ...