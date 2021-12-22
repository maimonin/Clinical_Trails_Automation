# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'win_decision_node.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from win_questionnaire_condition import Ui_QuestionnaireDialog
from win_test_condition import Ui_TestCond
from win_trait_condition import Ui_TraitCond
from nodeeditor.utils import dumpException

class Ui_Dialog(object):
    def __init__(self):
        super().__init__()
        self.details = {}
        self._num_of_question = 0
        self.questions = []

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(812, 645)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(9, 9, 791, 631))
        self.widget.setObjectName("widget")

        self.decision_addCond_questionnaire = QtWidgets.QPushButton(self.widget)
        self.decision_addCond_questionnaire.setGeometry(QtCore.QRect(520, 280, 191, 61))
        self.decision_addCond_questionnaire.setObjectName("decision_addCond_questionnaire")
        self.decision_addCond_questionnaire.clicked.connect(self.add_cond_questionnaire)

        self.decision_addCond_test = QtWidgets.QPushButton(self.widget)
        self.decision_addCond_test.setGeometry(QtCore.QRect(520, 210, 191, 61))
        self.decision_addCond_test.setObjectName("decision_addCond_test")
        self.decision_addCond_test.clicked.connect(self.add_cond_test)

        self.decision_addCond_trait = QtWidgets.QPushButton(self.widget)
        self.decision_addCond_trait.setGeometry(QtCore.QRect(520, 140, 191, 61))
        self.decision_addCond_trait.setObjectName("decision_addCond_trait")
        self.decision_addCond_trait.clicked.connect(self.add_cond_trait)

        self.decision_save = QtWidgets.QPushButton(self.widget)
        self.decision_save.setGeometry(QtCore.QRect(40, 560, 101, 61))
        self.decision_save.setObjectName("decision_save")

        self.decision_discard = QtWidgets.QPushButton(self.widget)
        self.decision_discard.setGeometry(QtCore.QRect(160, 560, 101, 61))
        self.decision_discard.setObjectName("decision_discard")

        self.decision_edit = QtWidgets.QPushButton(self.widget)
        self.decision_edit.setGeometry(QtCore.QRect(280, 560, 101, 61))
        self.decision_edit.setObjectName("decision_edit")

        self.questions_list = QtWidgets.QListWidget(self.widget)
        self.questions_list.setGeometry(QtCore.QRect(30, 30, 431, 491))
        self.questions_list.setObjectName("questions_list")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.decision_addCond_questionnaire.setText(_translate("Dialog", "add questionnaire  result condition"))
        self.decision_addCond_test.setText(_translate("Dialog", "add test result condition"))
        self.decision_addCond_trait.setText(_translate("Dialog", "add trait condition"))
        self.decision_save.setText(_translate("Dialog", "Save"))
        self.decision_discard.setText(_translate("Dialog", "Discard"))
        self.decision_edit.setText(_translate("Dialog", "Edit Node details"))

    def add_cond_questionnaire(self):
        try:
            self.new_window = QtWidgets.QDialog()
            ui = Ui_QuestionnaireDialog(self.add_line)
            ui.setupUi(self.new_window)
            self.new_window.exec_()
        except Exception as e : dumpException(e)

    def add_cond_test(self):
        try:
            self.new_window = QtWidgets.QDialog()
            ui = Ui_TestCond(self.add_line)
            ui.setupUi(self.new_window)
            self.new_window.exec_()
        except Exception as e : dumpException(e)

    def add_cond_trait(self):
        try:
            self.new_window = QtWidgets.QDialog()
            ui = Ui_TraitCond(self.add_line)
            ui.setupUi(self.new_window)
            self.new_window.exec_()
        except Exception as e:
            dumpException(e)

    def add_line(self, question):
        _translate = QtCore.QCoreApplication.translate
        item = QtWidgets.QListWidgetItem()
        self.questions_list.addItem(item)
        item = self.questions_list.item(self._num_of_question)
        item.setText(_translate("Dialog", f"{question['title']}"))
        self.questions.append(question)
        self._num_of_question += 1

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
