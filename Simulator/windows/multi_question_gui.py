# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'multi_question_gui.ui'
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
        self.quetion_txt = QtWidgets.QLabel(self.widget)
        self.quetion_txt.setGeometry(QtCore.QRect(60, 30, 181, 51))
        self.quetion_txt.setObjectName("quetion_txt")
        self.next_btn = QtWidgets.QPushButton(self.widget)
        self.next_btn.setGeometry(QtCore.QRect(60, 290, 75, 23))
        self.next_btn.setObjectName("next_btn")
        self.groupBox = QtWidgets.QGroupBox(self.widget)
        self.groupBox.setGeometry(QtCore.QRect(60, 80, 341, 201))
        self.groupBox.setObjectName("groupBox")
        self.checkBox1 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox1.setGeometry(QtCore.QRect(10, 20, 83, 18))
        self.checkBox1.setObjectName("checkBox1")
        self.checkBox_2 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_2.setGeometry(QtCore.QRect(10, 50, 83, 18))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_3 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_3.setGeometry(QtCore.QRect(10, 80, 83, 18))
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_4 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_4.setGeometry(QtCore.QRect(10, 110, 83, 18))
        self.checkBox_4.setObjectName("checkBox_4")
        self.checkBox_6 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_6.setGeometry(QtCore.QRect(10, 170, 83, 18))
        self.checkBox_6.setObjectName("checkBox_6")
        self.checkBox_5 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_5.setGeometry(QtCore.QRect(10, 140, 83, 18))
        self.checkBox_5.setObjectName("checkBox_5")

        self.retranslateUi(open_question_gui)
        QtCore.QMetaObject.connectSlotsByName(open_question_gui)

    def retranslateUi(self, open_question_gui):
        _translate = QtCore.QCoreApplication.translate
        open_question_gui.setWindowTitle(_translate("open_question_gui", "Dialog"))
        self.quetion_txt.setText(_translate("open_question_gui", "Question"))
        self.next_btn.setText(_translate("open_question_gui", "Next"))
        self.groupBox.setTitle(_translate("open_question_gui", "Choose One Answer"))
        self.checkBox1.setText(_translate("open_question_gui", "Answer 1"))
        self.checkBox_2.setText(_translate("open_question_gui", "Answer 2"))
        self.checkBox_3.setText(_translate("open_question_gui", "Answer 3"))
        self.checkBox_4.setText(_translate("open_question_gui", "Answer 4"))
        self.checkBox_6.setText(_translate("open_question_gui", "Answer 6"))
        self.checkBox_5.setText(_translate("open_question_gui", "Answer 5"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    open_question_gui = QtWidgets.QDialog()
    ui = Ui_open_question_gui()
    ui.setupUi(open_question_gui)
    open_question_gui.show()
    sys.exit(app.exec_())
