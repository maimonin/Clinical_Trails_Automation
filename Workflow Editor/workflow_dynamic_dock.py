from PyQt5.QtWidgets import QDockWidget, QPushButton


class QDynamicDock(QDockWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Attributes")
        self.setWidget(QPushButton("Save",self))