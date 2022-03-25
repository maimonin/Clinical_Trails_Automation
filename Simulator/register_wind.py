# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'register_wind.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import asyncio
from syncer import sync
import json
import socket
import threading

import websockets
from PyQt5 import QtCore, QtGui, QtWidgets
from nodeeditor.utils import dumpException

from CMDSimulator import actor_simulation, register_user, users


class Ui_RegisterScreen(object):
    def setupUi(self, RegisterScreen):
        RegisterScreen.setObjectName("RegisterScreen")
        RegisterScreen.resize(469, 412)
        self.widget = QtWidgets.QWidget(RegisterScreen)
        self.widget.setGeometry(QtCore.QRect(-1, -1, 471, 411))
        self.widget.setObjectName("widget")
        self.textEditId = QtWidgets.QTextEdit(self.widget)
        self.textEditId.setGeometry(QtCore.QRect(40, 40, 181, 41))
        self.textEditId.setObjectName("textEditId")
        self.textEditage = QtWidgets.QTextEdit(self.widget)
        self.textEditage.setGeometry(QtCore.QRect(40, 110, 181, 41))
        self.textEditage.setObjectName("textEditage")
        self.comboBox = QtWidgets.QComboBox(self.widget)
        self.comboBox.setGeometry(QtCore.QRect(40, 180, 69, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(40, 230, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.add_line)
        self.startButton = QtWidgets.QPushButton(self.widget)
        self.startButton.setGeometry(QtCore.QRect(40, 230, 75, 23))
        self.startButton.setObjectName("startButton")
        self.startButton.clicked.connect(self.start_json)

        self.retranslateUi(RegisterScreen)
        QtCore.QMetaObject.connectSlotsByName(RegisterScreen)

    async def start_json(self):
        threads = []
        url = "ws://127.0.0.1:7890"
        loop = asyncio.get_event_loop()
        for user in users:
            s = await websockets.connect(url)
            await register_user(user, s)
            user['s'] = s
        for user in users:
            asyncio.create_task(actor_simulation(user, user['s']))
        path = input("workflow path:")
        try:
            f = open(path)
            data = json.load(f)
            print(data)
            data['sender'] = "editor"
            data['workflow_id'] = 0
            s = await websockets.connect(url)
            await s.send(json.dumps(data))
        except Exception as e:
            dumpException(e)

    @sync
    async def add_line(self):
        url = "ws://127.0.0.1:7890"
        s = await websockets.connect(url)
        user = {"name": "participant " + self.textEditId.toPlainText(), "role": "participant", "workflow": 0,
                "sex": self.comboBox.currentText(), "age": int(self.textEditage.toPlainText()),
                "id": int(self.textEditId.toPlainText())}
        await register_user(user, s)
        user['s'] = s
        asyncio.create_task(actor_simulation(user, user['s']))

    def retranslateUi(self, RegisterScreen):
        _translate = QtCore.QCoreApplication.translate
        RegisterScreen.setWindowTitle(_translate("RegisterScreen", "Dialog"))
        self.textEditId.setPlaceholderText(_translate("RegisterScreen", "id"))
        self.textEditage.setPlaceholderText(_translate("RegisterScreen", "age"))
        self.comboBox.setItemText(0, _translate("RegisterScreen", "male"))
        self.comboBox.setItemText(1, _translate("RegisterScreen", "female"))
        self.comboBox.setItemText(2, _translate("RegisterScreen", "other"))
        self.pushButton.setText(_translate("RegisterScreen", "register"))
        self.startButton.setText(_translate("RegisterScreen", "start"))


async def main():
    import sys
    url = "ws://127.0.0.1:7890"
    app = QtWidgets.QApplication(sys.argv)
    RegisterScreen = QtWidgets.QDialog()
    ui = Ui_RegisterScreen()
    ui.setupUi(RegisterScreen)
    RegisterScreen.show()
    sys.exit(app.exec_())


asyncio.run(main())