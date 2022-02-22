from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from nodeeditor.node_editor_window import NodeEditorWindow
from nodeeditor.utils import dumpException
from workflow_sub_window import WorkflowSubWindow
from workflow_drag_listbox import QDMDragListbox
from nodeeditor.utils import pp
from workflow_conf import WORKFLOW_NODES
from workflow_conf_nodes import *

DEBUG = False


class WorkflowEditorWindow(NodeEditorWindow):
    def __init__(self):
        super().__init__()

    def initUI(self):
        self.name_company = 'NAME HERE'
        self.name_product = 'Clinical Trial Workflow Editor'
        self.mdiArea = QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setCentralWidget(self.mdiArea)

        if DEBUG:
            print("Registered nodes:")
            pp(WORKFLOW_NODES)

        self.mdiArea.setViewMode(QMdiArea.TabbedView)
        self.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped[QWidget].connect(self.setActiveSubWindow)

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.updateMenus()

        self.createNodesDock()

        self.readSettings()

        self.setWindowTitle("Workflow Editor")

    def updateWindowMenu(self):
        self.windowMenu.clear()

        toolbar_nodes = self.windowMenu.addAction("Nodes Toolbar")
        toolbar_nodes.setCheckable(True)
        toolbar_nodes.triggered.connect(self.onWindowNodesToolbar)
        toolbar_nodes.setChecked(self.nodesDock.isVisible())

        self.windowMenu.addSeparator()

        self.windowMenu.addAction(self.actClose)
        self.windowMenu.addAction(self.actCloseAll)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actTile)
        self.windowMenu.addAction(self.actCascade)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actNext)
        self.windowMenu.addAction(self.actPrevious)
        self.windowMenu.addAction(self.actSeparator)

        windows = self.mdiArea.subWindowList()
        self.actSeparator.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()

            text = "%d %s" % (i + 1, child.getUserFriendlyFilename())
            if i < 9:
                text = '&' + text

            action = self.windowMenu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.getCurrentNodeEditorWidget())
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, window)

    def onWindowNodesToolbar(self):
        if self.nodesDock.isVisible():
            self.nodesDock.hide()
        else:
            self.nodesDock.show()

    def onFileNew(self):
        try:
            subwnd = self.createMdiChild()
            subwnd.show()
        except Exception as e:
            dumpException(e)

    def createMdiChild(self, child_widget=None):
        nodeeditor = child_widget if child_widget is not None else WorkflowSubWindow()
        subwnd = self.mdiArea.addSubWindow(nodeeditor)
        # nodeeditor.scene.history.addHistoryModifiedListener(self.updateEditMenu)
        # nodeeditor.addCloseEventListener(self.onSubWndClose)
        return subwnd

    def closeEvent(self, event):
        self.mdiArea.closeAllSubWindows()
        if self.mdiArea.currentSubWindow():
            event.ignore()
        else:
            self.writeSettings()
            event.accept()

    def getCurrentNodeEditorWidget(self):
        """ we're returning NodeEditorWidget here... """
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None

    def updateMenus(self):
        pass

    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)

    def createToolBars(self):
        pass

    def onFileOpen(self):
        fnames, filter = QFileDialog.getOpenFileNames(self, 'Open graph from file', self.getFileDialogDirectory(),
                                                      self.getFileDialogFilter())

        try:
            for fname in fnames:
                if fname:
                    existing = self.findMdiChild(fname)
                    if existing:
                        self.mdiArea.setActiveSubWindow(existing)
                    else:
                        # we need to create new subWindow and open the file
                        nodeeditor = WorkflowSubWindow()
                        if nodeeditor.fileLoad(fname):
                            self.statusBar().showMessage("File %s loaded" % fname, 5000)
                            nodeeditor.setTitle()
                            subwnd = self.createMdiChild(nodeeditor)
                            subwnd.show()
                        else:
                            nodeeditor.close()
        except Exception as e:
            dumpException(e)

    def findMdiChild(self, filename):
        for window in self.mdiArea.subWindowList():
            if window.widget().filename == filename:
                return window
        return None

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createNodesDock(self):
        self.nodesListWidget = QDMDragListbox()

        self.items = QDockWidget("Nodes")
        self.items.setWidget(self.nodesListWidget)
        self.items.setFloating(False)
        # change the title background color of the dock
        # self.items.setStyleSheet("""
        #         QDockWidget::title
        #        {
        #        background : #f1c40f;
        #        }
        # """)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.items)

    def activeMdiChild(self):
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None
