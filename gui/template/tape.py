from .interface import Interface
from PySide6.QtCore import QUrl, QPoint, Qt
from PySide6.QtGui import QDesktopServices, QColor, QFont
from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget, QApplication, QListWidgetItem, QListWidget, QHBoxLayout
from PySide6.QtWidgets import QTreeWidgetItem, QHBoxLayout, QTreeWidgetItemIterator, QTableWidgetItem, QListWidgetItem
from qfluentwidgets import InfoBarIcon, InfoBar, PushButton, setTheme, Theme, FluentIcon, InfoBarPosition, InfoBarManager
from qfluentwidgets import TreeWidget, TableWidget, ListWidget, HorizontalFlipView, ListView
from qfluentwidgets import FluentIcon as FIF

URL = 'https://github.com/Miki-Riako/TR-Simulator/blob/main/gui/turing_machine.py'



class InitialTape(TableWidget):
    def __init__(self, arr, parent=None):
        super().__init__(parent)

        self.arr = arr
        self.verticalHeader().hide()
        self.setBorderRadius(8)
        self.setBorderVisible(True)

        self.initial()

    def initial(self):
        self.infos = self.arr
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



class InitialKnapsackTape(TableWidget):
    def __init__(self, arr, parent=None):
        super().__init__(parent)
        self.arr = arr
        self.verticalHeader().hide()
        self.setBorderRadius(8)
        self.setBorderVisible(True)

        self.initial()

    def initial(self):
        self.c = int(self.arr[0])
        self.n = int(self.arr[1])
        self.infos_w = self.arr[2:6]
        self.infos_v = self.arr[6:]
        self.reset()

    def reset(self):
        try:
            assert self.n == len(self.infos_w) == len(self.infos_v)
            self.setColumnCount(2+2*self.n)
            self.setRowCount(1)
            header = []
            header.append('c')
            header.append('n')
            self.setItem(0, 0, QTableWidgetItem(str(self.c)))
            self.setItem(0, 1, QTableWidgetItem(str(self.n)))
            for i in range(self.n):
                self.setItem(0, i+2, QTableWidgetItem(self.infos_w[i]))
                header.append(f'w{i}')
            for i in range(self.n):
                self.setItem(0, i+2+self.n, QTableWidgetItem(self.infos_v[i]))
                header.append(f'v{i}')
            self.setHorizontalHeaderLabels(header)
            # self.resizeColumnsToContents()
            # self.resizeRowsToContents()
            # for column in range(self.columnCount()):
            #     self.setColumnWidth(column, self.columnWidth(column) + 10)
        except:
            InfoBar.warning(
                title='N\n',
                content='N应该为正确的值！\nN should be correct!',
                orient=Qt.Horizontal,
                isClosable=False,
                position=InfoBarPosition.TOP_LEFT,
                duration=2000,
                parent=self
            )
            return

    def getInfos(self):
        self.infos_w = []
        self.infos_v = []
        for i in range(self.columnCount()):
            item = self.item(0, i)
            if item is not None:
                if i == 0:
                    self.c = int(item.text())
                elif i == 1:
                    self.n = int(item.text())
                elif i < self.n+2:
                    self.infos_w.append(item.text())
                else:
                    self.infos_v.append(item.text())

    def addItem(self):
        self.getInfos()
        self.n += 1
        self.infos_w.append(None)
        self.infos_v.append(None)
        self.reset()

    def removeItem(self):
        self.getInfos()
        try:
            assert self.n > 0
            self.infos_v.pop()
            self.infos_w.pop()
            self.n -= 1
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
