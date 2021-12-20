import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QWidget

class WelcomeWindow(QDialog):
    def __init__(self):
        super(WelcomeWindow,self).__init__()
        loadUi("welcome_screen.ui", self)