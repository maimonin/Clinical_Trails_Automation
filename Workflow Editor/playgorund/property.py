# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\Workflow Editor\tests\property.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QSpinBox, QLineEdit, QTimeEdit, QComboBox, QDockWidget
import json


class Ui_DockWidget(QDockWidget):
    def __init__(self, data=None):
        super().__init__()
        self.data = data
        self.callback = self.data["callback"]

        self.functions = {
            "Text": self.create_text_input_widget,
            "time": self.create_time_input_widget,
            "combobox": self.create_combobox_input_widget,
            "list": self.create_list_widget,
            "spinbox": self.create_spinbox_widget
        }

    def setupUi(self):
        self.setObjectName("Properties")
        self.resize(527, 423)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.treeWidget = QtWidgets.QTreeWidget(self.dockWidgetContents)
        self.treeWidget.setGeometry(QtCore.QRect(0, 0, 531, 401))
        self.treeWidget.setMidLineWidth(1)
        self.treeWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.treeWidget.setItemsExpandable(True)
        self.treeWidget.setObjectName("treeWidget")
        # self.treeWidget.set

        self.treeWidget.header().setVisible(True)
        self.treeWidget.header().setHighlightSections(True)
        self.setWidget(self.dockWidgetContents)
        self.retranslateUi()
        if self.data is not None:
            self.build_tree()
        # QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("DockWidget", "DockWidget"))
        self.treeWidget.headerItem().setText(0, _translate("DockWidget", "Property"))
        self.treeWidget.headerItem().setText(1, _translate("DockWidget", "Value"))
        self.treeWidget.setColumnWidth(0, 170)
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        # self.treeWidget.topLevelItem(0).setText(0, _translate("DockWidget", "!!!"))
        # self.treeWidget.topLevelItem(0).setText(1, _translate("DockWidget", "44"))
        self.treeWidget.setSortingEnabled(__sortingEnabled)

    def build_tree(self):
        # self.callback is in the init function
        for section in self.data["sections"]:
            self.create_section(section)
    def create_section(self, section):
        main_section_widget = QtWidgets.QTreeWidgetItem(self.treeWidget)
        print(f"sedction name: {section['name']}")
        main_section_widget.setText(0, section["name"])
        for field in section["fields"]:
            filled_line = QtWidgets.QTreeWidgetItem(main_section_widget)
            filled_line.setText(0, field["name"])
            print(field)
            print(field["type"])
            if field["type"] in self.functions.keys():
                self.functions[field["type"]](filled_line, field)

            # item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
            # widget = QSpinBox()
            # widget.setValue(5)
            # self.treeWidget.setItemWidget(father: item_0,row: 1,widget: widget)
            pass

    def create_text_input_widget(self, father, field):
        # print(f"create_text_input_widget:: {field}")
        widget = QLineEdit()
        widget.setText(field["value"])
        self.treeWidget.setItemWidget(father, 1, widget)

    def create_time_input_widget(self, father, field):
        # print(f"create_time_input_widget:: {field}")
        widget = QTimeEdit()
        widget.setTime(field["value"])
        self.treeWidget.setItemWidget(father, 1, widget)

    def create_combobox_input_widget(self, father, field):
        # print(f"create_combobox_input_widget:: {field}")
        widget = QComboBox()
        options = field["options"]
        for opt in options:
            widget.addItem(opt)

        # cbstyle = "QComboBox QAbstractItemView {"
        # cbstyle += " border: 1px solid grey;"
        # cbstyle += " background: white;"
        # cbstyle += " selection-background-color: blue;"
        # cbstyle += " }"
        # cbstyle += " QComboBox {"
        # cbstyle += " background: white;"
        # cbstyle += "}"
        # widget.setStyleSheet(cbstyle)

        self.treeWidget.setItemWidget(father, 1, widget)

    def create_spinbox_widget(self, father, field):
        widget = QSpinBox()
        # widget.setText(field["value"])
        widget.setValue(field["value"])
        self.treeWidget.setItemWidget(father, 1, widget)

    def create_list_widget(self, father, field):
        items = field["items"]
        for item in items:
            item_line = QtWidgets.QTreeWidgetItem(father)
            item_line.setText(0, item["name"])
            if item["type"] in self.functions.keys():
                self.functions[item["type"]](item_line, item)

            # self.treeWidget.setItemWidget(item_line, 1, widget)


if __name__ == "__main__":
    data = {
        "sections": [{
            "name": "Node Details",
            "fields": [
                {"name": "title", "type": "Text", "value": ""},
                {"name": "time", "type": "time", "value": datetime.time(hour=1, minute=50)},
                {"name": "actor_in_charge", "type": "combobox",
                 "options": ["Nurse", "Doctor", "Participant", "Investigator", "Lab Technician"], "value": "Nurse"},
                {"name": "actors", "type": "list",
                 "items": [{"name": "Nurse", "value": 0, "type": "spinbox"}, {"name": "Doctor", "value":0, "type":"spinbox"}, {"name":"Participant","value":0, "type":"spinbox"}, {"name":"Investigator","value":0, "type":"spinbox"},{"name":"Lab Technician","value":0, "type":"spinbox"}]}
            ]},
            {
                "name": "Text",
                "fields": [
                    {"name": "text", "type": "Text", "value": ""}
                ]
            }

        ],
        "callback": "g"

    }
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # DockWidget = QtWidgets.QDockWidget()
    ui = Ui_DockWidget(data=data)

    ui.setupUi()
    ui.show()
    # DockWidget.show()
    sys.exit(app.exec_())
