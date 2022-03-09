import copy

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDockWidget, QPushButton, QFormLayout, QLabel, QLineEdit, QComboBox, QSpinBox, QTimeEdit, \
    QCheckBox


class QDynamicDock(QDockWidget):
    def __init__(self, parent=None):
        super().__init__(None)
        self.data = None
        self.callback = None
        self.content = None

        self.functions = {
            "text": self.create_text_input_widget,
            "time": self.create_time_input_widget,
            "combobox": self.create_combobox_input_widget,
            "list": self.create_list_widget,
            "spinbox": self.create_spinbox_widget,
            "checklist": self.create_checklist_widget,
            "sub tree": self.create_subtree_widget
        }
        self.setupUi()
        self.generator = numGenerator()


    def setupUi(self):
        self.setWindowTitle("Attributes")

        self.setObjectName("Properties")
        # self.resize(5000, 423)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.treeWidget = QtWidgets.QTreeWidget(self.dockWidgetContents)
        self.treeWidget.setGeometry(QtCore.QRect(0, 0, 400, 500))
        self.treeWidget.setMidLineWidth(2)
        self.treeWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.treeWidget.setItemsExpandable(True)
        self.treeWidget.setObjectName("treeWidget")
        # self.treeWidget.set

        self.treeWidget.header().setVisible(True)
        self.treeWidget.header().setHighlightSections(True)
        # self.treeWidget.itemChanged.connect(self.handleItemChanged)

        self.setWidget(self.dockWidgetContents)

        self.retranslateUi()
        if self.data is not None:
            self.build_tree()
        # QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.treeWidget.headerItem().setText(0, _translate("DockWidget", "Property"))
        self.treeWidget.headerItem().setText(1, _translate("DockWidget", "Value"))
        self.treeWidget.setColumnWidth(0, 170)
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.setSortingEnabled(__sortingEnabled)

    def change_data(self, data):
        self.data = data
        self.treeWidget.clear()
        self.generator.reset()
        if data is not None:
            self.callback = data["callback"]
            self.build_tree()

        return self.callback

    def build_tree(self):
        for section in self.data.keys():
            if section != "callback":
                self.create_section(section)
        self.treeWidget.expandAll()

    def create_section(self, section):
        main_section_widget = QtWidgets.QTreeWidgetItem(self.treeWidget)
        main_section_widget.setText(0, section)
        for field in self.data[section]:
            filled_line = QtWidgets.QTreeWidgetItem(main_section_widget)
            filled_line.setText(0, field["name"])
            if field["type"] in self.functions.keys():
                self.functions[field["type"]](filled_line, field)
            else:
                print(f"DynamicDock::create_section: ERR field type: {field['type']} is unknown")

    def create_text_input_widget(self, father, field):
        widget = QLineEdit()
        widget.setPlaceholderText("Enter Text Here")
        widget.setText(field["value"])
        # widget.textChanged.connect(lambda text: self.change_value(field, text))
        widget.editingFinished.connect(lambda: self.change_value(field, widget.text()))
        self.treeWidget.setItemWidget(father, 1, widget)

    def create_time_input_widget(self, father, field):
        widget = QTimeEdit()
        widget.setTime(field["value"])
        self.treeWidget.setItemWidget(father, 1, widget)

    def create_checklist_widget(self, father, field):
        options = field["options"]
        for option in options:
            option_line = QtWidgets.QTreeWidgetItem(father)
            option_line.setText(0, option)
            option_widget = QCheckBox()
            option_widget.setChecked(option in field["value"])
            option_widget.stateChanged.connect(lambda newState, text=option: self.change_checklist(field, text,
                                                                                                   newState))  # text = option so it will capture option value
            self.treeWidget.setItemWidget(option_line, 1, option_widget)

    def create_combobox_input_widget(self, father, field):
        widget = QComboBox()
        options = field["options"]
        for opt in options:
            widget.addItem(opt)

        self.treeWidget.setItemWidget(father, 1, widget)

    def create_spinbox_widget(self, father, field):
        widget = QSpinBox()
        widget.setValue(field["value"])
        self.treeWidget.setItemWidget(father, 1, widget)

    def create_list_widget(self, father, field):
        items = field["items"]
        for item in items:
            item_line = QtWidgets.QTreeWidgetItem(father)
            item_line.setText(0, item["name"])
            if item["type"] in self.functions.keys():
                self.functions[item["type"]](item_line, item)

    def create_subtree_widget(self, father, field):
        widget = QPushButton("ADD")
        widget.clicked.connect(lambda: self.on_click(father, field))
        self.treeWidget.setItemWidget(father, 1, widget)

        for value in field["value"]:
            item = QtWidgets.QTreeWidgetItem(father)
            for option in value:
                # do we want to change (only on next update), the widget title to the test name (child widget)
                if option["name"] == "Name" and option["value"] != "":
                    item.setText(0, option["value"])
                elif option["name"] == "Name" and option["value"] == "":
                    next = self.generator.gen_next()        # FIXME : always start from one , if we change the first tests, will get after that test1
                    item.setText(0, field["root name"] + f" #{next}")
                widget = QtWidgets.QTreeWidgetItem(item)
                widget.setText(0, option["name"])
                if option["type"] in self.functions.keys():
                    self.functions[option["type"]](widget, option)

    def on_click(self, father, field):
        field["value"].append(copy.deepcopy(field["template"]))
        # self.change_data(field, copy.deepcopy(field["template"]))
        next = self.generator.gen_next()
        item = QtWidgets.QTreeWidgetItem(father)
        # FIXME: think of another implementation of name generation , other than using @next object
        item.setText(0, field["root name"] + f" #{next}")
        for option in field["value"][next-1]:
            widget = QtWidgets.QTreeWidgetItem(item)
            widget.setText(0, option["name"])
            if option["type"] in self.functions.keys():
                self.functions[option["type"]](widget, option)
        self.callback(self.data)


    def change_checklist(self, field, option_text, newState):
        if newState == 0:
            field["value"].remove(option_text)
        else:
            field["value"].append(option_text)
        print(f"QDynamicDock::change_checklist::data is :{self.data}")
        self.callback(self.data)

    def change_value(self, field, value):
        # print("workflow_dynamic_dock::change_value::data changed!")
        field["value"] = value
        self.callback(self.data)


class numGenerator():

    def __init__(self):
        self.number = 0

    def gen_next(self):
        self.number += 1
        return self.number

    def reset(self):
        self.number = 0