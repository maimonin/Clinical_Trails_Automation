# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test_pop_up.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def __init__(self, participant, test, instruction):
        self.nameHolder_lbl.setText(participant)
        self.testHolder_lbl.setText(test)
        self.instructionHolder_lbl.setText(instruction)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(773, 557)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(19, 19, 741, 521))
        self.widget.setObjectName("widget")
        self.static1_lbl = QtWidgets.QLabel(self.widget)
        self.static1_lbl.setGeometry(QtCore.QRect(60, 80, 161, 19))
        self.static1_lbl.setObjectName("static1_lbl")
        self.nameHolder_lbl = QtWidgets.QLabel(self.widget)
        self.nameHolder_lbl.setGeometry(QtCore.QRect(220, 80, 141, 20))
        self.nameHolder_lbl.setObjectName("nameHolder_lbl")
        self.static2_lbl = QtWidgets.QLabel(self.widget)
        self.static2_lbl.setGeometry(QtCore.QRect(130, 110, 101, 19))
        self.static2_lbl.setObjectName("static2_lbl")
        self.static3_lbl = QtWidgets.QLabel(self.widget)
        self.static3_lbl.setGeometry(QtCore.QRect(60, 160, 231, 19))
        self.static3_lbl.setObjectName("static3_lbl")
        self.testHolder_lbl = QtWidgets.QLabel(self.widget)
        self.testHolder_lbl.setGeometry(QtCore.QRect(150, 210, 361, 19))
        self.testHolder_lbl.setObjectName("testHolder_lbl")
        self.instructionHolder_lbl = QtWidgets.QLabel(self.widget)
        self.instructionHolder_lbl.setGeometry(QtCore.QRect(150, 240, 381, 211))
        self.instructionHolder_lbl.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.instructionHolder_lbl.setObjectName("instructionHolder_lbl")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.static1_lbl.setText(_translate("Dialog", "Update: participant"))
        self.nameHolder_lbl.setText(_translate("Dialog", "nameHolder"))
        self.static2_lbl.setText(_translate("Dialog", "has arrived."))
        self.static3_lbl.setText(_translate("Dialog", "Please perform test:"))
        self.testHolder_lbl.setText(_translate("Dialog", "testHolder"))
        self.instructionHolder_lbl.setText(_translate("Dialog", "instructionHolder"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    ui.updateHolders('David','Billirubin','prepare 2 test tubes')
    sys.exit(app.exec_())
