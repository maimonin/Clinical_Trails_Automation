import copy

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDockWidget, QPushButton, QFormLayout, QLabel, QLineEdit, QComboBox, QSpinBox, QTimeEdit, \
    QCheckBox


class QDynamicDock(QDockWidget):

    def __init__(self):
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
            "test sub tree": self.create_test_subtree_widget,
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
        self.treeWidget.setGeometry(QtCore.QRect(0, 0, 400, 980))
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

    # set child dock callback.
    def set_child(self, child_update):
        self.child_update = child_update

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

        widget.timeChanged.connect(lambda time: self.change_value(field, time))

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

    # def load_subtree(self, father, field):
    #     for root in field["value"]:
    #         # left side with line edit
    #         widget = QLineEdit()
    #         widget.setPlaceholderText(field["placeholder"])
    #         widget.editingFinished.connect(
    #             lambda: self.create_subtree_widget(QtWidgets.QTreeWidgetItem(father.parent()), field, (widget, root)))
    #         widget.setText(root["text"])
    #         self.treeWidget.setItemWidget(father, 0, widget)
    #
    #         # right side with combobox
    #         widget2 = QComboBox()
    #         for opt in field["options"]:
    #             widget2.addItem(opt["name"])
    #         widget2.activated.connect(
    #             lambda index: self.handle_combobox_change(father, field, index, root))
    #         widget2.setCurrentIndex(root["type"])
    #         self.treeWidget.setItemWidget(father, 1, widget2)
    #
    #         # children
    #         if "sub" in root.keys():
    #             for sub in root["sub"]:
    #                 widget = QtWidgets.QTreeWidgetItem(father)
    #                 widget2 = QLineEdit()
    #                 widget2.setText(sub)
    #                 widget2_index = len(root["sub"])
    #                 widget2.editingFinished.connect(
    #                     lambda: self.lineedit_update(father, field, "", widget2, root, widget2_index))
    #                 self.treeWidget.setItemWidget(widget, 0, widget2)
    #
    #             widget_item = QtWidgets.QTreeWidgetItem(father)
    #             widget3 = QLineEdit()
    #             widget3.setPlaceholderText(field["placeholder"])
    #             widget_index = len(root["sub"])
    #             widget3.editingFinished.connect(
    #                 lambda: self.lineedit_update(father, field, field["placeholder"], widget3, root, widget_index))
    #             self.treeWidget.setItemWidget(widget_item, 0, widget3)
    #
    # # @field dict should have keys: value,options
    # def create_subtree_widget(self, father, field, caller=None):
    #     # check if its the first call or a callback
    #     if caller is None:
    #         self.load_subtree(father, field)
    #         father = QtWidgets.QTreeWidgetItem(father.parent())
    #     else:
    #         # update the data with the caller text
    #         caller[1]["text"] = str(caller[0].text())
    #
    #     #   create the next empty item
    #     template = {"name": "", "type": 0, "text": ""}
    #     field["value"].append(template)
    #
    #     widget = QLineEdit()
    #     widget.setPlaceholderText(field["placeholder"])
    #     widget.editingFinished.connect(
    #         lambda: self.create_subtree_widget(QtWidgets.QTreeWidgetItem(father.parent()), field, (widget, template)))
    #     self.treeWidget.setItemWidget(father, 0, widget)
    #
    #     # case of multi choose
    #     if len(field["options"]) > 0:
    #         widget2 = QComboBox()
    #         for opt in field["options"]:
    #             widget2.addItem(opt["name"])
    #         widget2.activated.connect(
    #             lambda index: self.handle_combobox_change(father, field, index, template))
    #         self.treeWidget.setItemWidget(father, 1, widget2)
    #
    #     # update node
    #     self.callback(self.data)
    #
    # # @option _index_ that is selected in the combobox
    # # @root - data variable for the option includes:[name,type,text,sub]
    # def handle_combobox_change(self, father, field, option, root):
    #     root["name"] = field["options"][option]["name"]
    #     root["type"] = option
    #
    #     if field["options"][option]["inputs"]:
    #         # in case a double click on the same combo
    #         if father.childCount() == 1:
    #             return
    #         root["sub"] = []
    #         widget = QtWidgets.QTreeWidgetItem(father)
    #         widget2 = QLineEdit()
    #         widget2.setPlaceholderText(field["options"][option]["placeholder"])
    #         widget2_index = len(root["sub"])
    #         widget2.editingFinished.connect(
    #             lambda: self.lineedit_update(father, field, field["options"][option]["placeholder"], widget2, root,
    #                                          widget2_index))
    #         self.treeWidget.setItemWidget(widget, 0, widget2)
    #     else:
    #         for i in reversed(range(father.childCount())):
    #             father.removeChild(father.child(i))
    #
    #     # update node
    #     self.callback(self.data)
    #
    # def lineedit_update(self, father, field, placeholder, caller, root, line_index):
    #     if caller.text() == "":
    #         caller.setPlaceholderText("Enter Here")
    #
    #     if caller.text() != "" and caller.text() not in root["sub"]:
    #         if line_index < len(root["sub"]):
    #             root["sub"][line_index] = caller.text()
    #         else:
    #             root["sub"].append(caller.text())
    #
    #         # max 6 childrens
    #         if father.childCount() == 6:
    #             return
    #
    #         widget_item = QtWidgets.QTreeWidgetItem(father)
    #         widget = QLineEdit()
    #         widget.setPlaceholderText(placeholder)
    #         widget_index = len(root["sub"])
    #         widget.editingFinished.connect(
    #             lambda: self.lineedit_update(father, field, placeholder, widget, root, widget_index))
    #         self.treeWidget.setItemWidget(widget_item, 0, widget)
    #
    #         # update node
    #         self.callback(self.data)

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

    # # @field of type "sub tree" must have:
    # # "root name" - the default name of a new item
    # # "template" - how to build the items
    # def create_dynamicSubTree_widget(self, father, field):
    #     widget = QPushButton("Add")
    #     widget.clicked.connect(lambda: self.on_click(father, field))
    #     self.treeWidget.setItemWidget(father, 1, widget)
    #     widget.setStyleSheet("background-color: rgba(255, 255, 255, 0);border: none;")
    #
    #     for value in field["value"]:
    #         item = QtWidgets.QTreeWidgetItem(father)
    #         next_id = self.generator.gen_next()  # FIXME : always start from one , if we change the first tests, will get after that test1
    #         for option in value:
    #             # do we want to change the widget title to the test name - child widget (happens only on next update)
    #             if option["name"] == "Name" and option["value"] != "":
    #                 item.setText(0, option["value"])
    #             elif option["name"] == "Name" and option["value"] == "":
    #                 item.setText(0, field["root name"] + f" #{next_id}")
    #             widget = QtWidgets.QTreeWidgetItem(item)
    #             widget.setText(0, option["name"])
    #             if option["type"] in self.functions.keys():
    #                 self.functions[option["type"]](widget, option)
    #
    #         remove = QtWidgets.QTreeWidgetItem(item)
    #         remove_button = QPushButton("Remove")
    #         remove_button.clicked.connect(lambda: self.on_remove_click(father, item, next_id - 1))
    #         self.treeWidget.setItemWidget(remove, 1, remove_button)
    #         remove_button.setStyleSheet("background-color: rgba(255, 255, 255, 0);border: none;")
    #
    # def on_click(self, father, field):
    #     field["value"].append(copy.deepcopy(field["template"]))
    #     # self.change_data(field, copy.deepcopy(field["template"]))
    #     next_id = self.generator.gen_next()
    #     item = QtWidgets.QTreeWidgetItem(father)
    #     # FIXME: think of another implementation of name generation - other than using @next object
    #     item.setText(0, field["root name"] + f" #{next_id}")
    #     for option in field["value"][-1]:
    #         widget = QtWidgets.QTreeWidgetItem(item)
    #         widget.setText(0, option["name"])
    #         if option["type"] in self.functions.keys():
    #             self.functions[option["type"]](widget, option)
    #
    #     remove = QtWidgets.QTreeWidgetItem(item)
    #     remove_button = QPushButton("Remove")
    #     remove_button.clicked.connect(lambda: self.on_remove_click(father, item, next_id - 1))
    #     self.treeWidget.setItemWidget(remove, 1, remove_button)
    #     remove_button.setStyleSheet("background-color: rgba(255, 255, 255, 0);border: none;")
    #
    #     self.callback(self.data)
    #
    # # removing the child item from the parent item
    # # and from @self.data, using index in the list
    # def on_remove_click(self, parent, child, child_id):
    #     parent.removeChild(child)
    #     self.data["Content"][0]["value"].pop(child_id)
    #     self.callback(self.data)

    def create_test_subtree_widget(self, father, field):
        test_tree = TestTree(self.treeWidget, father, field["value"], self.update_tests)

    def update_tests(self, tests):
        self.callback(self.data)


class numGenerator:

    def __init__(self):
        self.number = 0

    def gen_next(self):
        self.number += 1
        return self.number

    def reset(self):
        self.number = 0


class TestTree:

    def __init__(self, dock, tree_widget_item, data, update_dock):
        self.tests = data
        self.next_test_id = 0
        self.test_template = [
            {"name": "Name", "type": "text", "value": ""},
            {"name": "Instructions", "type": "text", "value": ""},
            {"name": "Staff", "type": "checklist",
             "options": ["Nurse", "Doctor", "Participant", "Investigator", "Lab Technician"],
             "value": []},
            {"name": "Duration", "type": "text", "value": "0"},
            {"name": "Facility", "type": "text", "value": ""}, ]
        self.dock = dock
        self.call_dock = update_dock

        add_button = QPushButton("Add")
        add_button.clicked.connect(lambda: self.add_test(tree_widget_item))
        add_button.setStyleSheet("background-color: rgba(255, 255, 255, 0);border: none;")

        tree_widget_item.setText(0, "Tests")
        self.dock.setItemWidget(tree_widget_item, 1, add_button)

        if len(self.tests) > 0:
            # self.load_data()      - in case of deleting "id" key
            self.next_test_id = self.tests[-1]["id"]
            self.rebuild_tree(tree_widget_item)

    # fix input
    def load_data(self):
        self.tests = [dict(item, id=self.get_next_id()) for item in self.tests]

    def get_next_id(self):
        self.next_test_id += 1
        return self.next_test_id

    def add_test(self, root):
        test_data = {
            "id": self.get_next_id(),
            "name": "",
            "instructions": "",
            "staff": [],
            "duration": "",
            "facility": ""
        }
        self.tests.append(test_data)

        new_widget = QtWidgets.QTreeWidgetItem(root)
        new_widget.setText(0, "New Test #" + str(test_data["id"]))

        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(lambda bool, id=test_data["id"]: self.rebuild_tree(root, id))
        remove_button.setStyleSheet("background-color: rgba(255, 255, 255, 0);border: none;")
        self.dock.setItemWidget(new_widget, 1, remove_button)

        self.add_line_edit(new_widget, test_data, "Name")
        self.add_line_edit(new_widget, test_data, "Instructions")
        self.add_checklist(new_widget, test_data)
        self.add_line_edit(new_widget, test_data, "Duration")
        self.add_line_edit(new_widget, test_data, "Facility")

    # @root - the container who holds all the tests items. (Called: Tests)
    # @remove_id - remove specific item
    def rebuild_tree(self, root, remove_id=-1):
        root.takeChildren()

        if remove_id > -1:
            for i in range(len(self.tests)):
                if self.tests[i]['id'] == remove_id:
                    del self.tests[i]
                    break

        for test_data in self.tests:
            new_widget = QtWidgets.QTreeWidgetItem(root)
            new_widget.setText(0, "New Test #" + str(test_data["id"]))

            remove_button = QPushButton("Remove")
            remove_button.clicked.connect(lambda bool, id=test_data["id"]: self.rebuild_tree(root, id))
            remove_button.setStyleSheet("background-color: rgba(255, 255, 255, 0);border: none;")
            self.dock.setItemWidget(new_widget, 1, remove_button)

            self.add_line_edit(new_widget, test_data, "Name")
            self.add_line_edit(new_widget, test_data, "Instructions")
            self.add_checklist(new_widget, test_data)
            self.add_line_edit(new_widget, test_data, "Duration")
            self.add_line_edit(new_widget, test_data, "Facility")

    def add_line_edit(self, new_widget, test_data, title):
        name_item = QtWidgets.QTreeWidgetItem(new_widget)
        name_item.setText(0, title)
        name_widget = QLineEdit()
        name_widget.editingFinished.connect(lambda: self.line_changed(test_data, title.lower(), name_widget.text()))
        name_widget.setPlaceholderText("Enter " + title)

        # in rebuild, load prev data
        if test_data[title.lower()] != "":
            name_widget.setText(test_data[title.lower()])

        self.dock.setItemWidget(name_item, 1, name_widget)

    def line_changed(self, data, key, new_text):
        data[key] = new_text

        self.call_dock(self.tests)

    def add_checklist(self, parent, test_data):
        title = "Staff"
        staff_item = QtWidgets.QTreeWidgetItem(parent)
        staff_item.setText(0, title)
        staff_item.setExpanded(False)

        for option in ["Nurse", "Doctor", "Participant", "Investigator", "Lab Technician"]:
            option_item = QtWidgets.QTreeWidgetItem(staff_item)

            option_title = QLabel(option)
            option_title.setMinimumWidth(100)
            self.dock.setItemWidget(option_item, 0, option_title)

            # FIXME not aligned properly
            option_widget = QCheckBox()
            option_widget.setChecked(option in test_data[title.lower()])
            option_widget.stateChanged.connect(
                lambda checked, text=option: self.checklist_changed(checked, text, test_data))
            self.dock.setItemWidget(option_item, 1, option_widget)

    # @checked: 0 for unchecked.
    # @value:string the value that got checked.
    def checklist_changed(self, checked, value, test_data):
        if checked == 0:
            test_data["staff"].remove(value)
        else:
            test_data["staff"].append(value)

        self.call_dock(self.tests)

