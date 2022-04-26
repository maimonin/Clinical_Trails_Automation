# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\node_details_simple.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_node_details_simple(object):
    def __init__(self, callback, details=None):
        super().__init__()
        self.actors=[]
        self.actors_count=0
        self.callback=callback
        self.details=None if details == {} else details

    def setupUi(self, Add_Test):
        Add_Test.setObjectName("Add_Test")
        Add_Test.resize(371, 506)
        self.widget = QtWidgets.QWidget(Add_Test)
        self.widget.setGeometry(QtCore.QRect(-1, -1, 371, 501))
        self.widget.setObjectName("widget")
        self.save_details_btn = QtWidgets.QPushButton(self.widget)
        self.save_details_btn.setGeometry(QtCore.QRect(40, 390, 201, 61))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.save_details_btn.setFont(font)
        self.save_details_btn.setObjectName("save_details_btn")
        self.save_details_btn.clicked.connect(self.save_datails)

        self.actors_comboBox = QtWidgets.QComboBox(self.widget)
        self.actors_comboBox.setGeometry(QtCore.QRect(40, 160, 171, 31))
        self.actors_comboBox.setObjectName("actors_comboBox")
        self.actors_comboBox.addItem("")
        self.actors_comboBox.addItem("")
        self.actors_comboBox.addItem("")
        self.actors_comboBox.addItem("")
        self.actors_comboBox.addItem("")
        self.listWidget = QtWidgets.QListWidget(self.widget)
        self.listWidget.setGeometry(QtCore.QRect(40, 210, 171, 161))
        self.listWidget.setObjectName("listWidget")

        self.add_actor_btn = QtWidgets.QPushButton(self.widget)
        self.add_actor_btn.setGeometry(QtCore.QRect(220, 160, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.add_actor_btn.setFont(font)
        self.add_actor_btn.setObjectName("add_actor_btn")
        self.add_actor_btn.clicked.connect(self.add_actor_btn_click)

        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setGeometry(QtCore.QRect(40, 130, 131, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.node_title = QtWidgets.QLineEdit(self.widget)
        self.node_title.setGeometry(QtCore.QRect(40, 69, 141, 31))
        self.node_title.setObjectName("node_title")

        self.retranslateUi(Add_Test)
        QtCore.QMetaObject.connectSlotsByName(Add_Test)

        if self.details is not None:
            self.load_details()

    def retranslateUi(self, Add_Test):
        _translate = QtCore.QCoreApplication.translate
        Add_Test.setWindowTitle(_translate("Add_Test", "Dialog"))
        self.save_details_btn.setText(_translate("Add_Test", "Save Details"))
        self.actors_comboBox.setItemText(0, _translate("Add_Test", "Nurse"))
        self.actors_comboBox.setItemText(1, _translate("Add_Test", "Doctor"))
        self.actors_comboBox.setItemText(2, _translate("Add_Test", "Investigator"))
        self.actors_comboBox.setItemText(3, _translate("Add_Test", "Participant"))
        self.actors_comboBox.setItemText(4, _translate("Add_Test", "Lab Technician"))
        self.add_actor_btn.setText(_translate("Add_Test", "Add Actor"))
        self.label_4.setText(_translate("Add_Test", "Add Actors"))
        self.node_title.setPlaceholderText(_translate("Add_Test", "Node Title"))

    def load_details(self):
        self.node_title.setText(self.details["title"])
        for actor in self.details["actors"]:
            self.add_line(actor)

    def save_datails(self):
        self.callback({"actors" : self.actors, "title": self.node_title.text()})

    def add_line(self,actor):

        self.actors.append(actor)
        _translate = QtCore.QCoreApplication.translate
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = self.listWidget.item(self.actors_count)
        item.setText(_translate("Node_Details", f"{actor}"))
        self.actors_count += 1

    def add_actor_btn_click(self):
        self.add_line(self.actors_comboBox.currentText())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Add_Test = QtWidgets.QDialog()
    ui = Ui_node_details_simple()
    ui.setupUi(Add_Test)
    Add_Test.show()
    sys.exit(app.exec_())