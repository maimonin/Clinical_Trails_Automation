


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'win_questionnaire_condition.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from nodeeditor.utils import dumpException

questCounter = 0

class Ui_TestCond(object):
    def __init__(self,questions):
        super().__init__()
        self.func=questions


    def setupUi(self, Dialog):
        self.window = Dialog
        Dialog.setObjectName("Dialog")
        Dialog.resize(701, 490)
        self.check_answer_no_lbl = QtWidgets.QLabel(Dialog)
        self.check_answer_no_lbl.setGeometry(QtCore.QRect(260, 80, 120, 16))
        self.check_answer_no_lbl.setObjectName("check_answer_no_lbl")

        self.questionnaire_answerNumber = QtWidgets.QSpinBox(Dialog)
        self.questionnaire_answerNumber.setGeometry(QtCore.QRect(380, 80, 42, 22))
        self.questionnaire_answerNumber.setObjectName("questionnaire_answerNumber")

        self.questionnaire_radio_include = QtWidgets.QRadioButton(Dialog)
        self.questionnaire_radio_include.setGeometry(QtCore.QRect(70, 130, 82, 17))
        self.questionnaire_radio_include.setObjectName("questionnaire_radio_include")

        self.questionnaire_radio_exclude = QtWidgets.QRadioButton(Dialog)
        self.questionnaire_radio_exclude.setGeometry(QtCore.QRect(70, 170, 82, 17))
        self.questionnaire_radio_exclude.setObjectName("questionnaire_radio_exclude")

        self.questionnaire_save = QtWidgets.QPushButton(Dialog)
        self.questionnaire_save.setGeometry(QtCore.QRect(40, 400, 101, 61))
        self.questionnaire_save.setObjectName("questionnaire_save")
        self.questionnaire_save.clicked.connect(self.save_condition)

        self.questionnaire_discard = QtWidgets.QPushButton(Dialog)
        self.questionnaire_discard.setGeometry(QtCore.QRect(160, 400, 101, 61))
        self.questionnaire_discard.setObjectName("questionnaire_discard")
        self.questionnaire_discard.clicked.connect(self.exit_window)

        self.questionnaire_include_text = QtWidgets.QLineEdit(Dialog)
        self.questionnaire_include_text.setGeometry(QtCore.QRect(160, 130, 113, 20))
        self.questionnaire_include_text.setObjectName("questionnaire_include_text")

        self.questionnaire_exclude_text = QtWidgets.QLineEdit(Dialog)
        self.questionnaire_exclude_text.setGeometry(QtCore.QRect(160, 170, 113, 20))
        self.questionnaire_exclude_text.setObjectName("questionnaire_exclude_text")

        self.questionnaire_no_lb = QtWidgets.QLabel(Dialog)
        self.questionnaire_no_lb.setGeometry(QtCore.QRect(60, 80, 180, 20))
        self.questionnaire_no_lb.setObjectName("questionnaire_no_lb")

        self.questionnaire_questtionaire_number = QtWidgets.QSpinBox(Dialog)
        self.questionnaire_questtionaire_number.setGeometry(QtCore.QRect(180, 80, 42, 22))
        self.questionnaire_questtionaire_number.setObjectName("questionnaire_questtionaire_number")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.check_answer_no_lbl.setText(_translate("Dialog", "check answer #"))
        self.questionnaire_radio_include.setText(_translate("Dialog", "include"))
        self.questionnaire_radio_exclude.setText(_translate("Dialog", "exclude"))
        self.questionnaire_save.setText(_translate("Dialog", "Save"))
        self.questionnaire_discard.setText(_translate("Dialog", "Discard"))
        self.questionnaire_no_lb.setText(_translate("Dialog", "questionnaire #"))

    def save_condition(self):
        try:
            global questCounter
            questCounter += 1

            q={"title": "questionnaire condition " + str(questCounter),
               "qNumber": self.questionnaire_questtionaire_number.value(),
               "ansNumber": self.questionnaire_answerNumber.value(),
               "include": self.questionnaire_include_text.text(),
               "exclude": self.questionnaire_exclude_text.text()
               }
            self.func(q)
            self.exit_window()
        except Exception as e:
            dumpException(e)

    def exit_window(self):
        self.window.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_QuestionnaireDialog(lambda x : x)
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
