from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDockWidget, QPushButton, QFormLayout, QLabel, QLineEdit, QComboBox, QSpinBox, QTimeEdit, QCheckBox


class QDynamicDock(QDockWidget):
    def __init__(self, parent=None):
        super().__init__(None)
        self.data = None
        self.callback = None
        self.content = None

        self.functions = {
            "Text": self.create_text_input_widget,
            "time": self.create_time_input_widget,
            "combobox": self.create_combobox_input_widget,
            "list": self.create_list_widget,
            "spinbox": self.create_spinbox_widget,
            "checklist" : self.create_checklist_widget
        }
        self.setupUi()

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
        if data is not None:
            self.callback = data["callback"]
            self.build_tree()

        return self.callback

    def build_tree(self):
        for section in self.data["sections"]:
            self.create_section(section)
        self.treeWidget.expandAll()

    def create_section(self, section):
        main_section_widget = QtWidgets.QTreeWidgetItem(self.treeWidget)
        print(f"section name: {section['name']}")
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

    def create_text_input_widget(self, father, field):
        widget = QLineEdit()
        widget.setText(field["value"])
        widget.setPlaceholderText("Enter Text Here")
        field["value"] = "fds"
        widget.textChanged.connect(lambda text : self.change_value(field,text))
        # widget.editingFinished.connect(lambda: self.handleItemChanged(widget))
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
            option_widget.stateChanged.connect(lambda newState,text=option:self.change_checklist(field,text,newState)) # text= option so it will capture option value
            self.treeWidget.setItemWidget(option_line,1,option_widget)



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

    def handleItemChanged(self, item):
        # TODO: full implement items change(all type of items).
        # current only the notification text is saved (to self.data)

        print("***************************Item Has Changed")
        self.data["sections"][1]["fields"][0]["value"] = item.text()
        print(self.data)

    def change_checklist(self,field,option_text,newState):
        if newState == 0:
            field["value"].remove(option_text)
        else:
            field["value"].append(option_text)
        print(f"QDynamicDock::change_checklist::data is :{self.data}")
        self.callback(self.data)

    def change_value(self,field,value):
        # print("workflow_dynamic_dock::change_value::data changed!")
        field["value"] = value
        self.callback(self.data)
