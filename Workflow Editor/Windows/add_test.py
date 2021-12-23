



# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Raviv Gilady\Desktop\temp dir\add_test.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from nodeeditor.utils import dumpException


class Ui_Add_Test(object):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.staff=[]
        self.staff_count=0

    def setupUi(self, Add_Test):
        Add_Test.setObjectName("Add_Test")
        Add_Test.resize(384, 572)
        self.window = Add_Test
        self.widget = QtWidgets.QWidget(Add_Test)
        self.widget.setGeometry(QtCore.QRect(-1, -1, 381, 571))
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(50, 40, 251, 91))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.test_name = QtWidgets.QLineEdit(self.widget)
        self.test_name.setGeometry(QtCore.QRect(50, 140, 211, 31))
        self.test_name.setObjectName("lineEdit")
        self.test_instructions = QtWidgets.QTextEdit(self.widget)
        self.test_instructions.setGeometry(QtCore.QRect(50, 190, 211, 61))
        self.test_instructions.setObjectName("textEdit")
        self.timeEdit = QtWidgets.QLineEdit(self.widget)
        self.timeEdit.setGeometry(QtCore.QRect(50, 280, 118, 22))
        self.timeEdit.setObjectName("timeEdit")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(50, 260, 47, 13))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.listWidget = QtWidgets.QListWidget(self.widget)
        self.listWidget.setGeometry(QtCore.QRect(50, 390, 211, 101))
        self.listWidget.setObjectName("listWidget")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(50, 320, 47, 13))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.staff_line = QtWidgets.QLineEdit(self.widget)
        self.staff_line.setGeometry(QtCore.QRect(50, 350, 211, 31))
        self.staff_line.setObjectName("staff_line")
        self.add_staff_btn = QtWidgets.QPushButton(self.widget)
        self.add_staff_btn.setGeometry(QtCore.QRect(280, 350, 75, 23))
        self.add_staff_btn.setObjectName("add_staff_btn")
        self.add_staff_btn.clicked.connect(self.add_line)
        self.save_test_btn = QtWidgets.QPushButton(self.widget)
        self.save_test_btn.setGeometry(QtCore.QRect(50, 500, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.save_test_btn.setFont(font)
        self.save_test_btn.setObjectName("save_questionnaire_btn")
        self.save_test_btn.clicked.connect(self.save_test)
        self.discard_btn = QtWidgets.QPushButton(self.widget)
        self.discard_btn.setGeometry(QtCore.QRect(180, 500, 121, 41))
        self.discard_btn.clicked.connect(self.exit_window)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.discard_btn.setFont(font)
        self.discard_btn.setObjectName("save_questionnaire_btn_2")
        self.retranslateUi(Add_Test)
        QtCore.QMetaObject.connectSlotsByName(Add_Test)


    def retranslateUi(self, Add_Test):
        _translate = QtCore.QCoreApplication.translate
        Add_Test.setWindowTitle(_translate("Add_Test", "Dialog"))
        self.label.setText(_translate("Add_Test", "Please Enter Test Data"))
        self.test_name.setPlaceholderText(_translate("Add_Test", "Test Name"))
        self.test_instructions.setPlaceholderText(_translate("Add_Test", "Test Instructions"))
        self.label_2.setText(_translate("Add_Test", "Duration"))
        self.label_3.setText(_translate("Add_Test", "Staff:"))
        self.timeEdit.setPlaceholderText(_translate("Add_Test", "time in minutes"))
        self.staff_line.setPlaceholderText(_translate("Add_Test", "Staff Type"))
        self.add_staff_btn.setText(_translate("Add_Test", "Add Staff"))
        self.save_test_btn.setText(_translate("Add_Test", "Save Test"))
        self.discard_btn.setText(_translate("Add_Test", "Discard"))

    def add_line(self):
        try:
            self.staff.append(self.staff_line.text())
            _translate = QtCore.QCoreApplication.translate
            item = QtWidgets.QListWidgetItem()
            self.listWidget.addItem(item)
            item = self.listWidget.item(self.staff_count)
            item.setText(_translate("Add_Test", f"{self.staff_line.text()}"))
            self.staff_count += 1
        except Exception as e:
            dumpException(e)

    def save_test(self):
        print("DEBUG")
        self.callback({"name" : self.test_name.text(), "instructions" : self.test_instructions.toPlainText(),"staff" : self.staff, "duration":self.timeEdit.text() })
        self.exit_window()

    def exit_window(self):
        self.window.close()
