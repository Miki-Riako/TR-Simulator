# coding:utf-8
from PySide6.QtCore import Qt, Signal, QUrl, QEvent
from PySide6.QtGui import QDesktopServices, QPainter, QPen, QColor
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame

from qfluentwidgets import (ScrollArea, PushButton, ToolButton, FluentIcon,
                            IconWidget, ToolTipFilter, TitleLabel, CaptionLabel,
                            StrongBodyLabel, BodyLabel,
                            TransparentToolButton)


class SeparatorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(6, 16)


class ExampleCard(QWidget):
    def __init__(self, title, widget: QWidget, icon_list, function_list, stretch=0, parent=None):
        super().__init__(parent=parent)
        self.widget = widget
        self.stretch = stretch
        self.titleLabel = StrongBodyLabel(title, self)
        self.card = QFrame(self)
        self.buttonWidget = QFrame(self.card)
        self.vBoxLayout = QVBoxLayout(self)
        self.cardLayout = QVBoxLayout(self.card)
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QHBoxLayout(self.buttonWidget)

        self.vBoxLayout.setSizeConstraint(QVBoxLayout.SetMinimumSize)
        self.cardLayout.setSizeConstraint(QVBoxLayout.SetMinimumSize)
        self.topLayout.setSizeConstraint(QHBoxLayout.SetMinimumSize)
        self.vBoxLayout.setSpacing(12)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.topLayout.setContentsMargins(12, 12, 12, 12)
        self.bottomLayout.setContentsMargins(18, 18, 18, 18)
        self.cardLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignTop)
        self.vBoxLayout.addWidget(self.card, 0, Qt.AlignTop)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.cardLayout.setSpacing(0)
        self.cardLayout.setAlignment(Qt.AlignTop)
        self.cardLayout.addLayout(self.topLayout, 0)
        self.cardLayout.addWidget(self.buttonWidget, 0, Qt.AlignBottom)
        self.widget.setParent(self.card)
        self.topLayout.addWidget(self.widget)
        if self.stretch == 0:
            self.topLayout.addStretch(1)
        self.widget.show()
        self.bottomLayout.addStretch(1)
        
        self.button_list = []
        for i in range(len(icon_list)):
            self.button_list.append(TransparentToolButton(icon_list[i], self))
            self.button_list[i].clicked.connect(function_list[i])
        for i in self.button_list:
            self.bottomLayout.addWidget(i, 0, Qt.AlignRight)

        self.card.setObjectName('card')


class ToolBar(QWidget):
    def __init__(self, title, subtitle, text_list_left, text_list_right, icon_list, function_list, parent=None):
        super().__init__(parent=parent)
        self.titleLabel = TitleLabel(title, self)
        self.subtitleLabel = CaptionLabel(subtitle, self)
        self.button_list_left = []
        self.button_list_right = []

        for i in range(len(text_list_left)):
            self.button_list_left.append(PushButton(text_list_left[i], self, icon_list[i]))
            self.button_list_left[i].clicked.connect(function_list()[i])
        for i in range(len(text_list_right)):
            self.button_list_right.append(ToolButton(icon_list[i+len(text_list_left)], self))
            self.button_list_right[i].clicked.connect(function_list()[i+len(text_list_left)])
            self.button_list_right[i].setToolTip(text_list_right[i])

        self.separator = SeparatorWidget(self)
        self.vBoxLayout = QVBoxLayout(self)
        self.buttonLayout = QHBoxLayout()

        self.setFixedHeight(138)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(36, 22, 36, 12)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addSpacing(4)
        self.vBoxLayout.addWidget(self.subtitleLabel)
        self.vBoxLayout.addSpacing(4)
        self.vBoxLayout.addLayout(self.buttonLayout, 1)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

        self.buttonLayout.setSpacing(4)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        for i in self.button_list_left:
            self.buttonLayout.addWidget(i, 0, Qt.AlignLeft)
        self.buttonLayout.addStretch(1)
        for i in self.button_list_right:
            self.buttonLayout.addWidget(i, 0, Qt.AlignRight)
        self.buttonLayout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        for i in self.button_list_right:
            i.installEventFilter(ToolTipFilter(i))


class Interface(ScrollArea):
    def __init__(self, title: str, subtitle: str, text_list_left, text_list_right, icon_list, function_list, parent=None):
        super().__init__(parent=parent)
        self.view = QWidget(self)
        self.toolBar = ToolBar(title, subtitle, text_list_left, text_list_right, icon_list, function_list, self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, self.toolBar.height(), 0, 0)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setSpacing(30)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.setContentsMargins(36, 20, 36, 36)

        self.view.setObjectName('view')


    def scrollToCard(self, index: int):
        w = self.vBoxLayout.itemAt(index).widget()
        self.verticalScrollBar().setValue(w.y())

    def addExampleCard(self, title, widget, icon_list, function_list, stretch=0):
        card = ExampleCard(title, widget, icon_list, function_list, stretch, self.view)
        self.vBoxLayout.addWidget(card, 0, Qt.AlignTop)
        return card

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.toolBar.resize(self.width(), self.toolBar.height())
