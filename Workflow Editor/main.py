import os, sys, inspect

from PyQt5 import QtWidgets
from qtpy.QtWidgets import QApplication

from welcome_screen_py import WelcomeWindow
from workflow_window import WorkflowEditorWindow
sys.path.insert(0, os.path.join( os.path.dirname(__file__), "..", ".." ))

from nodeeditor.utils import loadStylesheet
from nodeeditor.node_editor_window import NodeEditorWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # welcome_window= WelcomeWindow()
    # widget = QtWidgets.QStackedWidget()
    # widget.addWidget(welcome_window)
    # widget.setFixedHeight(800)
    # widget.setFixedWidth(800)
    # widget.show()
    wnd = WorkflowEditorWindow()
    wnd.show()
    # wnd.nodeeditor.addNodes()
    # wnd.addCustomNode()
    module_path = os.path.dirname( inspect.getfile(wnd.__class__) )

    # loadStylesheet( os.path.join( module_path, 'qss/nodestyle.qss') )

    sys.exit(app.exec_())