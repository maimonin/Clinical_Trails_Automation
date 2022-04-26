import copy

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIntValidator, QIcon
from PyQt5.QtWidgets import QDockWidget, QPushButton, QFormLayout, QLabel, QLineEdit, QComboBox, QSpinBox, QTimeEdit, \
    QCheckBox
from nodeeditor.utils import dumpException


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
            "combobox icons": self.create_combobox_icons_widget,
            "spinbox": self.create_spinbox_widget,
            "checklist": self.create_checklist_widget,
            "tree": self.create_tree_widget,
            "test sub tree": self.create_test_subtree_widget,
            "q sub tree": self.create_questionnaire_subtree_widget,
            "cond sub tree": self.create_condition_subtree_widget,
        }
        self.setupUi()

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
        if "placeholder" in field.keys():
            widget.setPlaceholderText(field["placeholder"])
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
        widget.currentTextChanged.connect(lambda text: self.change_combolist(field, text))
        widget.setCurrentIndex(field["options"].index(field["value"]))
        self.treeWidget.setItemWidget(father, 1, widget)

    def create_combobox_icons_widget(self, father, field):
        widget = QComboBox()
        options = field["options"]
        for i, opt in enumerate(options):
            widget.addItem(opt)
            widget.setItemIcon(i, QIcon(".\\assets\\icons\\"+opt.lower()+"_icon.png"))
        widget.currentTextChanged.connect(lambda text: self.change_combolist(field, text))
        widget.setCurrentIndex(field["options"].index(field["value"]))
        self.treeWidget.setItemWidget(father, 1, widget)

    def create_spinbox_widget(self, father, field):
        widget = QSpinBox()
        widget.setValue(field["value"])
        self.treeWidget.setItemWidget(father, 1, widget)

    def create_tree_widget(self, father, field):
        items = field["items"]
        for item in items:
            item_line = QtWidgets.QTreeWidgetItem(father)
            item_line.setText(0, item["name"])
            if item["type"] in self.functions.keys():
                self.functions[item["type"]](item_line, item)

    def change_combolist(self, field, option):
        field["value"] = option
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

    def create_test_subtree_widget(self, father, field):
        TestTree(self.treeWidget, father, field["value"], self.update_dynamic)

    def create_questionnaire_subtree_widget(self, father, field):
        QuestionnaireTree(self.treeWidget, father, field["value"], self.update_dynamic)

    def create_condition_subtree_widget(self, father, field):
        ConditionTree(self.treeWidget, father, field["value"], self.update_dynamic)

    def update_dynamic(self):
        self.callback(self.data)


class TestTree:

    def __init__(self, dock, tree_widget_item, data, update_dock):
        self.tests = data
        self.next_test_id = 0
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
            # option_title.setMinimumWidth(100)
            option_title.setWordWrap(True)
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


class QuestionnaireTree:

    def __init__(self, dock, tree_widget_item, data, update_dock):
        self.questions = data
        self.next_question_id = 0
        self.dock = dock
        self.call_dock = update_dock

        add_button = QPushButton("Add")
        add_button.clicked.connect(lambda: self.add_question(tree_widget_item))
        add_button.setStyleSheet("background-color: rgba(255, 255, 255, 0);border: none;")

        tree_widget_item.setText(0, "Questions")
        self.dock.setItemWidget(tree_widget_item, 1, add_button)

        if len(self.questions) > 0:
            # self.load_data()      - in case of deleting "id" key
            self.next_question_id = self.questions[-1]["id"]
            self.rebuild_tree(tree_widget_item)

    def rebuild_tree(self, root, remove_id=-1):
        root.takeChildren()

        if remove_id > -1:
            for i in range(len(self.questions)):
                if self.questions[i]['id'] == remove_id:
                    del self.questions[i]
                    break

        for question_data in self.questions:
            new_widget = QtWidgets.QTreeWidgetItem(root)
            # new_widget.setText(0, "New Question #" + str(question_data["id"]))
            new_widget_label = QLabel("New Question #" + str(question_data["id"]))
            new_widget_label.setWordWrap(True)
            self.dock.setItemWidget(new_widget, 0, new_widget_label)

            remove_button = QPushButton("Remove")
            remove_button.clicked.connect(lambda bool, id=question_data["id"]: self.rebuild_tree(root, id))
            remove_button.setStyleSheet("background-color: rgba(255, 255, 255, 0);border: none;")
            self.dock.setItemWidget(new_widget, 1, remove_button)

            question_item = QtWidgets.QTreeWidgetItem(new_widget)

            question_widget = QLineEdit()
            question_widget.setPlaceholderText("Enter Question")
            question_widget.setMinimumWidth(100)
            question_widget.setText(question_data["text"])
            question_widget.editingFinished.connect(
                lambda widget=question_widget: self.line_changed(question_data, "text", widget))
            self.dock.setItemWidget(question_item, 0, question_widget)

            combo_widget = QComboBox()
            options = ["Open", "Multiple Choice", "One Choice"]
            for opt in options:
                combo_widget.addItem(opt)
            if question_data["type"] == "multi":
                combo_widget.setCurrentIndex(1)
                self.combo_changed(options, 1, question_data, new_widget)
            elif question_data["type"] == "one choice":
                combo_widget.setCurrentIndex(2)
                self.combo_changed(options, 2, question_data, new_widget)

            combo_widget.activated.connect(
                lambda index: self.combo_changed(options, index, question_data, new_widget))
            self.dock.setItemWidget(question_item, 1, combo_widget)

    def add_question(self, root):
        question_data = {
            "id": self.get_next_id(),
            "type": "open",  # default
            "text": "",
            # "options": [],
        }
        self.questions.append(question_data)

        new_widget = QtWidgets.QTreeWidgetItem(root)
        # new_widget.setText(0, "New Question #" + str(question_data["id"]))
        new_widget_label = QLabel("New Question #" + str(question_data["id"]))
        new_widget_label.setWordWrap(True)
        self.dock.setItemWidget(new_widget, 0, new_widget_label)

        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(lambda bool, id=question_data["id"]: self.rebuild_tree(root, id))
        remove_button.setStyleSheet("background-color: rgba(255, 255, 255, 0);border: none;")
        self.dock.setItemWidget(new_widget, 1, remove_button)

        question_item = QtWidgets.QTreeWidgetItem(new_widget)
        question_widget = QLineEdit()
        question_widget.setPlaceholderText("Enter Question")
        question_widget.setMinimumWidth(100)
        question_widget.editingFinished.connect(
            lambda widget=question_widget: self.line_changed(question_data, "text", widget))
        self.dock.setItemWidget(question_item, 0, question_widget)

        combo_widget = QComboBox()
        options = ["Open", "Multiple Choice", "One Choice"]
        for opt in options:
            combo_widget.addItem(opt)
        combo_widget.activated.connect(
            lambda index: self.combo_changed(options, index, question_data, new_widget))

        self.dock.setItemWidget(question_item, 1, combo_widget)

    def line_changed(self, data, key, questionnaire_widget):
        data[key] = questionnaire_widget.text()

        self.call_dock()

    def combo_changed(self, options, index_changed, data, parent):
        if options[index_changed] == "Open":
            if parent.childCount() == 2:
                parent.removeChild(parent.child(1))
            data["type"] = "open"
            self.call_dock(self.questions)

        else:
            if options[index_changed] == "Multiple Choice":
                data["type"] = "multi"
            elif options[index_changed] == "One Choice":
                data["type"] = "once choice"

            if parent.childCount() == 2:
                parent.removeChild(parent.child(1))

            if "options" not in data.keys():
                data["options"] = [None] * 6

            answers_item = QtWidgets.QTreeWidgetItem(parent)
            answers_item.setText(0, "Answers")

            for i in range(6):
                answer_item = QtWidgets.QTreeWidgetItem(answers_item)
                answer_widget = QLineEdit()
                answer_widget.setPlaceholderText("Answer #" + str(i + 1))
                if data["options"][i] is not None:
                    answer_widget.setText(data["options"][i])
                # answer_item.setMinimumWidth(100)
                answer_widget.editingFinished.connect(
                    lambda index=i, widget=answer_widget: self.answer_changed(widget, index, data))
                self.dock.setItemWidget(answer_item, 0, answer_widget)

    def answer_changed(self, text_widget, answer_index, data):
        data["options"][answer_index] = text_widget.text()

        self.call_dock(self.questions)

    def get_next_id(self):
        self.next_question_id += 1
        return self.next_question_id


class ConditionTree:

    def __init__(self, dock, tree_widget_item, data, update_dock):
        self.conditions = data
        self.next_question_id = 0
        self.dock = dock
        self.call_dock = update_dock

        add_button = QPushButton("Add")
        add_button.clicked.connect(lambda: self.add_condition(tree_widget_item))
        add_button.setStyleSheet("background-color: rgba(255, 255, 255, 0);border: none;")

        tree_widget_item.setText(0, "Conditions")
        self.dock.setItemWidget(tree_widget_item, 1, add_button)

        if len(self.conditions) > 0:
            # self.load_data()      - in case of deleting "id" key
            self.next_condition_id = self.conditions[-1]["id"]
            self.rebuild_tree(tree_widget_item)

    def add_condition(self, root):
        id = self.get_next_id()
        condition_data = {
            "id": id,
            "title": "condition_" + str(id),
            "type": "trait condition",  # default
            "satisfy": {
                "type": "range",
                "value": {"min": "-1", "max": "-1"},
            },
        }
        self.conditions.append(condition_data)

        new_widget = QtWidgets.QTreeWidgetItem(root)
        # new_widget.setText(0, "New Condition #" + str(id))
        new_widget_label = QLabel("New Condition #" + str(id))
        new_widget_label.setWordWrap(True)
        self.dock.setItemWidget(new_widget, 0, new_widget_label)

        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(lambda bool, id=condition_data["id"]: self.rebuild_tree(root, id))
        remove_button.setStyleSheet("background-color: rgba(255, 255, 255, 0);border: none;")
        self.dock.setItemWidget(new_widget, 1, remove_button)

        self.build_trait_type(new_widget, condition_data)

    def rebuild_tree(self, root, remove_id=-1):
        root.takeChildren()

        if remove_id > -1:
            for i in range(len(self.conditions)):
                if self.conditions[i]['id'] == remove_id:
                    del self.conditions[i]
                    break

        for condition_data in self.conditions:
            new_widget = QtWidgets.QTreeWidgetItem(root)
            new_widget.setText(0, "New Condition #" + str(condition_data["id"]))

            remove_button = QPushButton("Remove")
            remove_button.clicked.connect(lambda bool, id=condition_data["id"]: self.rebuild_tree(root, id))
            remove_button.setStyleSheet("background-color: rgba(255, 255, 255, 0);border: none;")
            self.dock.setItemWidget(new_widget, 1, remove_button)

            if condition_data["type"].lower() == "trait condition":
                self.build_trait_type(new_widget, condition_data)
            elif condition_data["type"].lower() == "test condition":
                self.build_test_type(new_widget, condition_data)
            else:
                self.build_questionnaire_type(new_widget, condition_data)

    def build_trait_type(self, parent, data):
        if "trait" not in data.keys():
            data["trait"] = ""

        combo_item = QtWidgets.QTreeWidgetItem(parent)
        combo_item.setText(0, "Type")
        combo_widget = QComboBox()
        options = ["Trait", "Test", "Questionnaire"]
        for opt in options:
            combo_widget.addItem(opt)
        combo_widget.activated.connect(
            lambda index: self.combo_changed(options, index, data, parent))

        self.dock.setItemWidget(combo_item, 1, combo_widget)
        condition_item = QtWidgets.QTreeWidgetItem(parent)
        condition_item.setText(0, "Trait:")
        condition_widget = QLineEdit()
        condition_widget.setPlaceholderText("Enter Trait")
        condition_widget.setMinimumWidth(100)
        if data["trait"] != "":
            condition_widget.setText(data["trait"])
        condition_widget.editingFinished.connect(
            lambda widget=condition_widget: self.line_changed(widget, data, "trait"))
        self.dock.setItemWidget(condition_item, 1, condition_widget)

        satisfy_type_item = QtWidgets.QTreeWidgetItem(parent)
        satisfy_type_item.setText(0, "Satisfy Type:")
        satisfy_type_widget = QComboBox()
        satisfy_type_widget.addItem("Range")
        satisfy_type_widget.addItem("One Choice")
        satisfy_type_widget.activated.connect(
            lambda index: self.combo2_changed(["Range", "One Choice"], index, data, parent))
        self.dock.setItemWidget(satisfy_type_item, 1, satisfy_type_widget)

        if data["satisfy"]["type"] == "one_choice":
            satisfy_type_widget.setCurrentIndex(1)

            satisfy_value_item = QtWidgets.QTreeWidgetItem(parent)
            satisfy_value_item.setText(0, "Satisfy Value:")
            value_widget = QLineEdit()
            value_widget.setPlaceholderText("Enter Value")
            value_widget.setText(data["satisfy"]["value"])
            value_widget.editingFinished.connect(
                lambda widget=value_widget: self.line_changed(widget, data["satisfy"], "value"))
            self.dock.setItemWidget(satisfy_value_item, 1, value_widget)
            return

        satisfy_value_item = QtWidgets.QTreeWidgetItem(parent)
        # satisfy_value_item.setText(0, "Satisfy Value:")
        satisfy_value_label = QLabel("Satisfy Value:")
        satisfy_value_label.setWordWrap(True)
        self.dock.setItemWidget(satisfy_value_item, 0, satisfy_value_label)

        min_value_widget = QLineEdit()
        min_value_widget.setPlaceholderText("Min")
        min_value_widget.editingFinished.connect(
            lambda widget=min_value_widget: self.line_changed(widget, data["satisfy"], "value", "min"))
        onlyInt = QIntValidator()
        min_value_widget.setValidator(onlyInt)
        if data["satisfy"]["value"]["min"] != "-1":
            min_value_widget.setText(data["satisfy"]["value"]["min"])
        self.dock.setItemWidget(satisfy_value_item, 1, min_value_widget)

        satisfy_value_item2 = QtWidgets.QTreeWidgetItem(parent)
        max_value_widget = QLineEdit()
        max_value_widget.setPlaceholderText("Max")
        max_value_widget.editingFinished.connect(
            lambda widget=max_value_widget: self.line_changed(widget, data["satisfy"], "value", "max"))
        max_value_widget.setValidator(onlyInt)
        if data["satisfy"]["value"]["max"] != "-1":
            max_value_widget.setText(data["satisfy"]["value"]["max"])
        self.dock.setItemWidget(satisfy_value_item2, 1, max_value_widget)

    def build_test_type(self, parent, data):
        combo_item = QtWidgets.QTreeWidgetItem(parent)
        combo_item.setText(0, "Type")
        combo_widget = QComboBox()
        options = ["Trait", "Test", "Questionnaire"]
        for opt in options:
            combo_widget.addItem(opt)
        combo_widget.activated.connect(
            lambda index: self.combo_changed(options, index, data, parent))
        combo_widget.setCurrentIndex(1)
        self.dock.setItemWidget(combo_item, 1, combo_widget)

        condition_item = QtWidgets.QTreeWidgetItem(parent)
        condition_item.setText(0, "Test:")
        condition_widget = QLineEdit()
        condition_widget.setPlaceholderText("Enter Test")
        condition_widget.setMinimumWidth(100)
        if "condition" not in data["test"]:
            condition_widget.setText(data["test"])
        condition_widget.editingFinished.connect(
            lambda widget=condition_widget: self.line_changed(widget, data, "test"))
        self.dock.setItemWidget(condition_item, 1, condition_widget)

        satisfy_type_item = QtWidgets.QTreeWidgetItem(parent)
        satisfy_type_item.setText(0, "Satisfy Type:")
        satisfy_type_widget = QComboBox()
        satisfy_type_widget.addItem("Range")
        satisfy_type_widget.addItem("One Choice")
        satisfy_type_widget.activated.connect(
            lambda index: self.combo2_changed(["Range", "One Choice"], index, data, parent))
        self.dock.setItemWidget(satisfy_type_item, 1, satisfy_type_widget)

        if data["satisfy"]["type"] == "one_choice":
            satisfy_type_widget.setCurrentIndex(1)

            satisfy_value_item = QtWidgets.QTreeWidgetItem(parent)
            satisfy_value_item.setText(0, "Satisfy Value:")
            value_widget = QLineEdit()
            value_widget.setPlaceholderText("Enter Value")
            value_widget.setText(data["satisfy"]["value"])
            value_widget.editingFinished.connect(
                lambda widget=value_widget: self.line_changed(widget, data["satisfy"], "value"))
            self.dock.setItemWidget(satisfy_value_item, 1, value_widget)
            return

        satisfy_value_item = QtWidgets.QTreeWidgetItem(parent)
        # satisfy_value_item.setText(0, "Satisfy Value:")
        satisfy_value_label = QLabel("Satisfy Value:")
        satisfy_value_label.setWordWrap(True)
        self.dock.setItemWidget(satisfy_value_item, 0, satisfy_value_label)
        min_value_widget = QLineEdit()
        min_value_widget.setPlaceholderText("Min")
        min_value_widget.editingFinished.connect(
            lambda widget=min_value_widget: self.line_changed(widget, data["satisfy"], "value", "min"))
        onlyInt = QIntValidator()
        min_value_widget.setValidator(onlyInt)
        if data["satisfy"]["value"]["min"] != "-1":
            min_value_widget.setText(data["satisfy"]["value"]["min"])
        self.dock.setItemWidget(satisfy_value_item, 1, min_value_widget)

        satisfy_value_item2 = QtWidgets.QTreeWidgetItem(parent)
        max_value_widget = QLineEdit()
        max_value_widget.setPlaceholderText("Max")
        max_value_widget.editingFinished.connect(
            lambda widget=max_value_widget: self.line_changed(widget, data["satisfy"], "value", "max"))
        max_value_widget.setValidator(onlyInt)
        if data["satisfy"]["value"]["max"] != "-1":
            max_value_widget.setText(data["satisfy"]["value"]["max"])
        self.dock.setItemWidget(satisfy_value_item2, 1, max_value_widget)

    def build_questionnaire_type(self, parent, data):
        combo_item = QtWidgets.QTreeWidgetItem(parent)
        combo_item.setText(0, "Type")
        combo_widget = QComboBox()
        options = ["Trait", "Test", "Questionnaire"]
        for opt in options:
            combo_widget.addItem(opt)
        combo_widget.activated.connect(
            lambda index: self.combo_changed(options, index, data, parent))
        combo_widget.setCurrentIndex(2)
        self.dock.setItemWidget(combo_item, 1, combo_widget)

        id_item = QtWidgets.QTreeWidgetItem(parent)
        # id_item.setText(0, "Questionnaire ID:")
        id_label = QLabel("Questionnaire ID:")
        id_label.setWordWrap(True)
        self.dock.setItemWidget(id_item, 0, id_label)

        id_widget = QLineEdit()
        id_widget.setPlaceholderText("Enter Questionnaire ID")
        id_widget.editingFinished.connect(
            lambda widget=id_widget: self.line_changed(widget, data, "questionnaireNumber"))
        if data["questionnaireNumber"] != "0":
            id_widget.setText(data["questionnaireNumber"])
        self.dock.setItemWidget(id_item, 1, id_widget)

        question_item = QtWidgets.QTreeWidgetItem(parent)
        # question_item.setText(0, "Question Number:")
        question_label = QLabel("Question Number:")
        question_label.setWordWrap(True)
        self.dock.setItemWidget(question_item, 0, question_label)

        question_widget = QLineEdit()
        question_widget.setPlaceholderText("Enter Question #")
        question_widget.editingFinished.connect(
            lambda widget=question_widget: self.line_changed(widget, data, "questionNumber"))
        if data["questionNumber"] != "0":
            id_widget.setText(data["questionNumber"])
        self.dock.setItemWidget(question_item, 1, question_widget)

        answers_item = QtWidgets.QTreeWidgetItem(parent)
        # answers_item.setText(0, "Accepted Answers:")
        answers_label = QLabel("Accepted Answers:")
        answers_label.setWordWrap(True)
        self.dock.setItemWidget(answers_item, 0, answers_label)

        answers_widget = QLineEdit()
        answers_widget.setPlaceholderText("Enter Accepted Answers")
        answers_widget.editingFinished.connect(
            lambda widget=answers_widget: self.line_changed(widget, data, "acceptedAnswers"))
        if data["acceptedAnswers"] == "":
            id_widget.setText(data["acceptedAnswers"])
        self.dock.setItemWidget(answers_item, 1, answers_widget)

    def combo_changed(self, options, index_changed, data, parent):
        old_type = data["type"]
        if options[index_changed].lower() in old_type.lower():  # same
            return

        old_id = data["id"]
        old_title = data["title"]
        self.remove_condition(old_id)

        if options[index_changed] == "Trait":
            data = {
                "id": old_id,
                "title": old_title,
                "type": "trait condition",
                "satisfy": {
                    "type": "range",
                    "value": {"min": "-1", "max": "-1"},
                },
                "trait": "",
            }
            self.conditions.append(data)

            parent.takeChildren()
            self.build_trait_type(parent, data)

        elif options[index_changed] == "Test":
            data = {
                "id": old_id,
                "title": old_title,
                "type": "test condition",
                "satisfy": {
                    "type": "range",
                    "value": {"min": "-1", "max": "-1"},
                },
                "test": "",
            }
            self.conditions.append(data)

            parent.takeChildren()
            self.build_test_type(parent, data)

        elif options[index_changed] == "Questionnaire":
            data = {
                "id": old_id,
                "title": old_title,
                "type": "questionnaire condition",
                "questionnaireNumber": "0",
                "questionNumber": "0",
                "acceptedAnswers": "",
            }
            self.conditions.append(data)

            parent.takeChildren()
            self.build_questionnaire_type(parent, data)

        self.call_dock()

    def combo2_changed(self, options, index_changed, data, parent):
        state = parent.childCount()  # know state by children number, 4 = one choice, 5 = range
        if (options[index_changed] == "Range" and state == 5) or (
                options[index_changed] == "One Choice" and state == 4):
            return
        else:
            if options[index_changed] == "Range":
                data["satisfy"]["type"] = "range"
                data["satisfy"]["value"] = {"min": "-1", "max": "-1"}

                parent.takeChild(state - 1)  # pop last children
                satisfy_value_item = QtWidgets.QTreeWidgetItem(parent)
                # satisfy_value_item.setText(0, "Satisfy Value:")
                satisfy_value_label = QLabel("Satisfy Value:")
                satisfy_value_label.setWordWrap(True)
                self.dock.setItemWidget(satisfy_value_item, 0, satisfy_value_label)

                min_value_widget = QLineEdit()
                min_value_widget.setPlaceholderText("Min")
                min_value_widget.editingFinished.connect(
                    lambda widget=min_value_widget: self.line_changed(widget, data["satisfy"], "value", "min"))
                self.dock.setItemWidget(satisfy_value_item, 1, min_value_widget)

                satisfy_value_item2 = QtWidgets.QTreeWidgetItem(parent)
                max_value_widget = QLineEdit()
                max_value_widget.setPlaceholderText("Max")
                max_value_widget.editingFinished.connect(
                    lambda widget=max_value_widget: self.line_changed(widget, data["satisfy"], "value", "max"))
                self.dock.setItemWidget(satisfy_value_item2, 1, max_value_widget)

            else:
                parent.takeChild(state - 1)
                parent.takeChild(state - 2)

                satisfy_value_item = QtWidgets.QTreeWidgetItem(parent)
                # satisfy_value_item.setText(0, "Satisfy Value:")
                satisfy_value_label = QLabel("Satisfy Value:")
                satisfy_value_label.setWordWrap(True)
                self.dock.setItemWidget(satisfy_value_item, 0, satisfy_value_label)

                value_widget = QLineEdit()
                value_widget.setPlaceholderText("Enter Value")
                value_widget.editingFinished.connect(
                    lambda widget=value_widget: self.line_changed(widget, data["satisfy"], "value"))
                self.dock.setItemWidget(satisfy_value_item, 1, value_widget)

                data["satisfy"]["type"] = "one_choice"
                data["satisfy"]["value"] = "0"
            self.call_dock()

    def line_changed(self, widget, data, field, field2=None):
        if field2 is None:
            data[field] = widget.text()
        else:
            data[field][field2] = widget.text()

        self.call_dock()

    def remove_condition(self, id):
        idx = 0

        for condition in self.conditions:
            if condition["id"] == id:
                break
            idx += 1

        del self.conditions[idx]

    def get_next_id(self):
        self.next_question_id += 1
        return self.next_question_id