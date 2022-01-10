import json
import socket

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from nodeeditor.node_editor_widget import NodeEditorWidget
from nodeeditor.node_scene import InvalidFile
from qtpy import QtWidgets, QtCore
from nodeeditor.node_edge import EDGE_TYPE_DIRECT, EDGE_TYPE_BEZIER, EDGE_TYPE_SQUARE
from workflow_conf import *
from workflow_node_base import *
from nodeeditor.utils import dumpException
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import pyqtSlot
import time
import threading

DEBUG = False


class WorkflowSubWindow(NodeEditorWidget):
    def initUI(self):
        super().initUI()

    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setTitle()
        self.scene.addDragEnterListener(self.onDragEnter)
        self.scene.addDropListener(self.onDrop)
        self.scene.setNodeClassSelector(self.getNodeClassFromData)

    def getNodeClassFromData(self, data):
        if 'op_code' not in data: return Node
        return get_class_from_opcode(data['op_code'])

    def setTitle(self):
        self.setWindowTitle(self.getUserFriendlyFilename())

    def onDragEnter(self, event):
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            event.acceptProposedAction()
        else:
            event.setAccepted(False)
    def contextMenuEvent(self, event):
        try:
            item = self.scene.getItemAt(event.pos())

            if type(item) == QGraphicsProxyWidget:
                item = item.widget()

            if hasattr(item, 'edge'):
                self.handleEdgeContextMenu(event)

            return super().contextMenuEvent(event)
        except Exception as e: dumpException(e)
    def handleEdgeContextMenu(self, event):
        context_menu = QMenu(self)
        bezierAct = context_menu.addAction("Bezier Edge")
        directAct = context_menu.addAction("Direct Edge")
        squareAct = context_menu.addAction("Square Edge")
        action = context_menu.exec_(self.mapToGlobal(event.pos()))

        selected = None
        item = self.scene.getItemAt(event.pos())
        if hasattr(item, 'edge'):
            selected = item.edge

        if selected and action == bezierAct: selected.edge_type = EDGE_TYPE_BEZIER
        if selected and action == directAct: selected.edge_type = EDGE_TYPE_DIRECT
        if selected and action == squareAct: selected.edge_type = EDGE_TYPE_SQUARE

    def onDrop(self, event):
        self.scene.serialize()
        print("On drop")
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            eventData = event.mimeData().data(LISTBOX_MIMETYPE)
            dataStream = QDataStream(eventData, QIODevice.ReadOnly)
            pixmap = QPixmap()
            dataStream >> pixmap
            op_code = dataStream.readInt()
            text = dataStream.readQString()

            mouse_position = event.pos()
            scene_position = self.scene.grScene.views()[0].mapToScene(mouse_position)
            try:
                node = get_class_from_opcode(op_code)(self.scene)
                node.setPos(scene_position.x(), scene_position.y())
                node.drop_action()
            except Exception as e:
                dumpException(e)

            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def fileLoad(self, filename):
        return super().fileLoad(filename)

    def data_load(self, json_data, name):  # used to load data from complex node data
        try:
            self.filename = name
            self.scene.deserialize(json_data)
            self.has_been_modified = False
        except json.JSONDecodeError:
            raise InvalidFile("%s is not a valid JSON data" % name)
        except Exception as e:
            dumpException(e)

    # TODO serialize, and send the json to server

    # def get_node_by_socket(self,socket):
    #     for node in self.scene.nodes:
    #         if len(node.inputs[0].edges) > 0 and node.inputs[0].edges[0].end_socket == socket:
    #             return node
    #     return None
    # def all_logic(self):
    #     try:
    #         current_node = None
    #
    #         for node in self.scene.nodes:
    #             if len(node.inputs[0].edges) == 0:
    #                 current_node = node
    #                 break
    #         x=current_node.content.edit.text().split('/')
    #         print(x[0])
    #         time.sleep(int(x[1]))
    #         while current_node is not None and len(current_node.outputs[0].edges) != 0:
    #             current_node = self.get_node_by_socket(current_node.outputs[0].edges[0].end_socket)
    #             x = current_node.content.edit.text().split('/')
    #             print(x[0])
    #             time.sleep(int(x[1]))
    #         # while (len(current_node.outputs[0]) != 0 ):
    #         #     print(current_node.outputs[0].edges)
    #         #     print('PyQt5 button click')
    #     except Exception as e:
    #         dumpException(e)
    #     # doing something........
    # @pyqtSlot()
    def on_click(self):
        print("clicked")
        try:

            f = open('data.json')
            data = json.load(f)
            print(data)
            data['sender'] = "editor"
            data['workflow_id'] = 0
            host = '127.0.0.1'
            port = 8000
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.send((json.dumps(data) + '$').encode('ascii'))
        except Exception as e:
            dumpException(e)
