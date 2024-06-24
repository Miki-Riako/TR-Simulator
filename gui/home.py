import os
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QSizePolicy,
    QVBoxLayout, QWidget, QFrame)

class Home(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.setObjectName(text.replace(' ', '-'))

    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(400, 300)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.logo = QLabel(Form)
        self.logo.setObjectName(u"logo")
        self.logo.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        logo_pix = QPixmap(os.path.join(os.path.dirname(__file__), '../images', 'logo.png'))
        self.logo.setPixmap(logo_pix.scaled(150, 150, Qt.KeepAspectRatio))
        self.horizontalLayout.addWidget(self.logo)
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.label = QLabel('TR-Simulator', self)
        self.label.setFont(QFont('Arial', 42, QFont.Bold))
        self.horizontalLayout.addWidget(self.label)
        self.horizontalLayout.setStretch(0, 4)
        self.horizontalLayout.setStretch(1, 6)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.description = QLabel(Form)
        self.description.setObjectName(u"label_3")
        self.description.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.description = QLabel('Simulator for Turing Machine and Recursive Function', self)
        self.description.setFont(QFont('Arial', 15))
        self.description.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.description)
        self.verticalLayout.setStretch(0, 6)
        self.verticalLayout.setStretch(1, 4)
        QMetaObject.connectSlotsByName(Form)
