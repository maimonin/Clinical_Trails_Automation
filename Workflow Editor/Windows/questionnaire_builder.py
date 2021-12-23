# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Raviv Gilady\Desktop\computers\Clinical_Trails_Automation\Workflow Editor\Windows\Questions Windows\questionnaire_builder.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from question_with_options import Ui_MultipleChoiceQuestionAdd
from open_question import Ui_OpenQuestion
from nodeeditor.utils import dumpException
from node_details import Ui_Node_Details

quesionnaire_num = 0


class Ui_QuestionnaireBuild(object):

    def __init__(self, callback):
        super().__init__()
        self.details = {}
        self.callback = callback
        self._num_of_question = 0
        self._questions_list = []
        self.questions = []

    def setupUi(self, QuestionnaireBuild):
        QuestionnaireBuild.setObjectName("QuestionnaireBuild")
        QuestionnaireBuild.resize(837, 717)

        self.widget = QtWidgets.QWidget(QuestionnaireBuild)
        self.widget.setObjectName("centralwidget")
        self.add_multiple_choice_question_btn = QtWidgets.QPushButton(self.widget)
        self.add_multiple_choice_question_btn.setGeometry(QtCore.QRect(460, 120, 351, 91))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.add_multiple_choice_question_btn.setFont(font)
        self.add_multiple_choice_question_btn.setObjectName("add_multiple_choice_question_btn")
        self.add_multiple_choice_question_btn.clicked.connect(self.add_checkbox_question)

        self._questions_list = QtWidgets.QListWidget(self.widget)
        self._questions_list.setGeometry(QtCore.QRect(20, 70, 431, 491))
        self._questions_list.setObjectName("questions_list")

        self.add_one_choice_question_btn = QtWidgets.QPushButton(self.widget)
        self.add_one_choice_question_btn.setGeometry(QtCore.QRect(460, 230, 351, 91))
        self.add_one_choice_question_btn.clicked.connect(self.add_radiobox_question)

        font = QtGui.QFont()
        font.setPointSize(15)
        self.add_one_choice_question_btn.setFont(font)
        self.add_one_choice_question_btn.setObjectName("add_one_choice_question_btn")
        self.add_open_question_btn = QtWidgets.QPushButton(self.widget)
        self.add_open_question_btn.setGeometry(QtCore.QRect(460, 340, 351, 91))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.add_open_question_btn.setFont(font)
        self.add_open_question_btn.setObjectName("add_open_question_btn")
        self.add_open_question_btn.clicked.connect(self.add_open_question)

        self.save_questionnaire_btn = QtWidgets.QPushButton(self.widget)
        self.save_questionnaire_btn.setGeometry(QtCore.QRect(20, 640, 201, 61))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.save_questionnaire_btn.setFont(font)
        self.save_questionnaire_btn.setObjectName("save_questionnaire_btn")
        self.save_questionnaire_btn.clicked.connect(self.save_questionnaire)

        self.discard_btn = QtWidgets.QPushButton(self.widget)
        self.discard_btn.setGeometry(QtCore.QRect(230, 640, 191, 61))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.discard_btn.setFont(font)
        self.discard_btn.setObjectName("discard_btn")
        self.discard_btn.clicked.connect(self.discard)

        self.add_node_details_btn = QtWidgets.QPushButton(self.widget)
        self.add_node_details_btn.setGeometry(QtCore.QRect(460, 640, 201, 61))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.add_node_details_btn.setFont(font)
        self.add_node_details_btn.setObjectName("add_node_details_btn")
        self.add_node_details_btn.clicked.connect(self.add_node_details)

        # QuestionnaireBuild.setCentralWidget(self.widget)

        self.retranslateUi(QuestionnaireBuild)
        QtCore.QMetaObject.connectSlotsByName(QuestionnaireBuild)

    def retranslateUi(self, QuestionnaireBuild):
        _translate = QtCore.QCoreApplication.translate
        QuestionnaireBuild.setWindowTitle(_translate("QuestionnaireBuild", "Build Questionnaire"))
        self.add_multiple_choice_question_btn.setText(_translate("QuestionnaireBuild", "Add Multiple Choice Question"))
        __sortingEnabled = self._questions_list.isSortingEnabled()
        self._questions_list.setSortingEnabled(False)
        self._questions_list.setSortingEnabled(__sortingEnabled)
        self.add_one_choice_question_btn.setText(_translate("QuestionnaireBuild", "Add One Choice Question"))
        self.add_open_question_btn.setText(_translate("QuestionnaireBuild", "Add Open Question"))
        self.save_questionnaire_btn.setText(_translate("QuestionnaireBuild", "Save Questionnaire"))
        self.discard_btn.setText(_translate("QuestionnaireBuild", "Discard"))
        self.add_node_details_btn.setText(_translate("QuestionnaireBuild", "Add Node Details"))

    def add_open_question(self):
        try:
            self.new_window = QtWidgets.QDialog()
            ui = Ui_OpenQuestion(self.add_line)
            ui.setupUi(self.new_window)
            self.new_window.exec_()
        except Exception as e:
            dumpException(e)

    def add_checkbox_question(self):
        try:
            self.new_window = QtWidgets.QDialog()
            ui = Ui_MultipleChoiceQuestionAdd(self.add_line, "multy")
            ui.setupUi(self.new_window)
            self.new_window.exec_()
        except Exception as e:
            dumpException(e)

    def add_radiobox_question(self):
        try:
            self.new_window = QtWidgets.QDialog()
            ui = Ui_MultipleChoiceQuestionAdd(self.add_line, "one choice")
            ui.setupUi(self.new_window)
            self.new_window.exec_()
        except Exception as e:
            dumpException(e)

    def add_line(self, question):
        _translate = QtCore.QCoreApplication.translate
        item = QtWidgets.QListWidgetItem()
        self._questions_list.addItem(item)
        item = self._questions_list.item(self._num_of_question)
        item.setText(_translate("QuestionnaireBuild", f"{question['text']} ; {question['type']}"))
        self.questions.append(question)
        self._num_of_question += 1

    def add_node_details(self):
        self.new_window = QtWidgets.QDialog()
        ui = Ui_Node_Details(self.callback_from_node_details)
        ui.setupUi(self.new_window)
        self.new_window.exec_()

    def callback_from_node_details(self, details):
        self.new_window.close()
        if details is not None:
            self.details = details

    def save_questionnaire(self):
        global quesionnaire_num
        quesionnaire_num +=1
        self.callback({"node_details": self.details, "questions": self.questions,"qusetionnaire_number": quesionnaire_num})
        # TODO : check details exist! if not, present a label

    def discard(self):
        try:
            self.callback(None)
        except Exception as e:
            dumpException(e)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    QuestionnaireBuild = QtWidgets.QDialog()
    ui = Ui_QuestionnaireBuild()
    ui.setupUi(QuestionnaireBuild)
    QuestionnaireBuild.show()
    sys.exit(app.exec_())
