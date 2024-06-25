from PySide6.QtWidgets import QApplication, QFrame

class About(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.setupUi()
        self.setObjectName(text.replace(' ', '-'))

    def setupUi(self):
        ...
