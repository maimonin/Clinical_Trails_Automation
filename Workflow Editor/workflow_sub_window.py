from PyQt5.QtGui import *
from PyQt5.QtCore import *
from nodeeditor.node_editor_widget import  NodeEditorWidget
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
        button = QPushButton('Start', self)
        button.setToolTip('This is an example button')
        button.move(100, 70)
        button.clicked.connect(self.on_click)

    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setTitle()
        self.scene.addDragEnterListener(self.onDragEnter)
        self.scene.addDropListener(self.  onDrop)

    def setTitle(self):
        self.setWindowTitle(self.getUserFriendlyFilename())

    def onDragEnter(self,event):
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            event.acceptProposedAction()
        else:
            event.setAccepted(False)
    def onDrop(self,event):
        print("On drop")
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            eventData= event.mimeData().data(LISTBOX_MIMETYPE)
            dataStream = QDataStream(eventData,QIODevice.ReadOnly)
            pixmap = QPixmap()
            dataStream >> pixmap
            op_code = dataStream.readInt()
            text = dataStream.readQString()

            mouse_position = event.pos()
            scene_position = self.scene.grScene.views()[0].mapToScene(mouse_position)
            try:
                node=get_class_from_opcode(op_code)(self.scene)
                node.setPos(scene_position.x(),scene_position.y())
                self.scene.history.storeHistory("Created Node %s" % node.__class__.__name__)
            except Exception as e : dumpException(e)


            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def get_node_by_socket(self,socket):
        for node in self.scene.nodes:
            if len(node.inputs[0].edges) > 0 and node.inputs[0].edges[0].end_socket == socket:
                return node
        return None
    def all_logic(self):
        try:
            current_node = None

            for node in self.scene.nodes:
                if len(node.inputs[0].edges) == 0:
                    current_node = node
                    break
            x=current_node.content.edit.text().split('/')
            print(x[0])
            time.sleep(int(x[1]))
            while current_node is not None and len(current_node.outputs[0].edges) != 0:
                current_node = self.get_node_by_socket(current_node.outputs[0].edges[0].end_socket)
                x = current_node.content.edit.text().split('/')
                print(x[0])
                time.sleep(int(x[1]))
            # while (len(current_node.outputs[0]) != 0 ):
            #     print(current_node.outputs[0].edges)
            #     print('PyQt5 button click')
        except Exception as e:
            dumpException(e)
        # doing something........
    @pyqtSlot()
    def on_click(self):
        x=threading.Thread(target=self.all_logic)
        x.start()