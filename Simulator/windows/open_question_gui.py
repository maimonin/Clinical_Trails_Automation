# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'open_question_gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_open_question_gui(object):
    def setupUi(self, open_question_gui):
        open_question_gui.setObjectName("open_question_gui")
        open_question_gui.resize(687, 422)
        self.widget = QtWidgets.QWidget(open_question_gui)
        self.widget.setGeometry(QtCore.QRect(-1, -1, 691, 421))
        self.widget.setObjectName("widget")
        self.question_txt = QtWidgets.QLabel(self.widget)
        self.question_txt.setGeometry(QtCore.QRect(60, 30, 181, 51))
        self.question_txt.setObjectName("question_txt")
        self.textEdit = QtWidgets.QTextEdit(self.widget)
        self.textEdit.setGeometry(QtCore.QRect(60, 80, 341, 181))
        self.textEdit.setObjectName("textEdit")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(60, 290, 75, 23))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(open_question_gui)
        QtCore.QMetaObject.connectSlotsByName(open_question_gui)

    def retranslateUi(self, open_question_gui):
        _translate = QtCore.QCoreApplication.translate
        open_question_gui.setWindowTitle(_translate("open_question_gui", "Dialog"))
        self.question_txt.setText(_translate("open_question_gui", "Question"))
        self.textEdit.setPlaceholderText(_translate("open_question_gui", "Answer"))
        self.pushButton.setText(_translate("open_question_gui", "Next"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    open_question_gui = QtWidgets.QDialog()
    ui = Ui_open_question_gui()
    ui.setupUi(open_question_gui)
    open_question_gui.show()
    sys.exit(app.exec_())
