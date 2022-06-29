from nodeeditor.node_editor_window import NodeEditorWindow
from nodeeditor.utils import pp

from workflow_conf_nodes import *
from workflow_drag_listbox import QDMDragListbox
from workflow_sub_window import WorkflowSubWindow

from workflow_window import WorkflowEditorWindow

DEBUG = False


class Workflow_Complex_Window(WorkflowEditorWindow):
    def __init__(self, complex_callback=None, data=None, name="Sub flow"):
        self.name = name
        self.complex_callback = complex_callback
        self.data = data
        super().__init__()
        self.exit = False
        self.saved = False
        if self.data is not None:
            self.load_data()

    def initUI(self):
        super().initUI()

    # create grid(middle window) section
    def createMdiChild(self, child_widget=None):
        nodeeditor = child_widget if child_widget is not None else WorkflowSubWindow(self.attributes.change_data)
        subwnd = self.mdiArea.addSubWindow(nodeeditor)
        # nodeeditor.scene.history.addHistoryModifiedListener(self.updateEditMenu)
        # nodeeditor.addCloseEventListener(self.onSubWndClose)
        return subwnd

    def createActions(self):
        """Create basic `File` and `Edit` actions"""
        self.actNew = QAction('&New\load existing', self, shortcut='Ctrl+N', statusTip="Create new graph", triggered=self.onFileNew)
        self.actSave = QAction('&Save', self, shortcut='Ctrl+S', statusTip="Save Complex Node",
                               triggered=self.onFileSave)
        self.actDiscard = QAction('&Exit', self, shortcut='Ctrl+W', statusTip="Discard", triggered=self.OnClose)
        self.actDelete = QAction('&Delete', self, shortcut='Del', statusTip="Delete selected items", triggered=self.onEditDelete)



    def onFileNew(self):
        if self.getCurrentNodeEditorWidget() is None:
            try:
                if self.data is not None:
                    nodeeditor = WorkflowSubWindow(self.attributes.change_data)        # grid window
                    nodeeditor.data_load(self.data, name=self.name)
                    subwnd = self.createMdiChild(nodeeditor)
                    subwnd.show()
                else:
                    subwnd = self.createMdiChild()
                    subwnd.show()

            except Exception as e:
                dumpException(e)

    def createMenus(self):
        self.create_complex_menu()

    def create_complex_menu(self):
        menubar = self.menuBar()
        self.fileMenu = menubar.addMenu('&Complex')
        self.fileMenu.addAction(self.actSave)
        self.fileMenu.addAction(self.actDiscard)
        self.fileMenu.addAction(self.actNew)
        self.fileMenu.addAction(self.actDelete)
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

    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)

    def createToolBars(self):
        pass

    def findMdiChild(self, filename):
        for window in self.mdiArea.subWindowList():
            if window.widget().filename == filename:
                return window
        return None

    def createStatusBar(self):
        self.statusBar().showMessage("To load existing press CTRL+N (or COMPLEX->New/Load Existing), To discard press exit.")

    # def createNodesDock(self):
    #     self.nodesListWidget = QDMDragListbox()
    #
    #     self.items = QDockWidget("Nodes")
    #     self.items.setWidget(self.nodesListWidget)
    #     self.items.setFloating(False)
    #
    #     self.addDockWidget(Qt.RightDockWidgetArea, self.items)

    def activeMdiChild(self):
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None

    def onFileSave(self):
        if self.complex_callback is None:  # means that this window is not a complex node, proceed as usual
            print("problem: no callback provided for this window!")
            return False
        else:
            current_nodeeditor = self.getCurrentNodeEditorWidget()
            if current_nodeeditor is None:
                print("problem: no active window is available!")
                return False
            self.saved = True
            self.complex_callback(current_nodeeditor.scene.serialize())

            return True

    def OnClose(self):
        self.exit = True
        self.complex_callback(self.data)

    def closeEvent(self, event):  # used when pressing the X button
        if not self.saved and not self.exit:
            self.complex_callback(self.data)


    def load_data(self):
        window = self.getCurrentNodeEditorWidget()
        if window is not None:  # means that subwindow is open
            window.data_load

        # else:
            # nodeeditor = WorkflowSubWindow()
            # nodeeditor.data_load(self.data, name=self.name)
            # subwnd = self.createMdiChild(nodeeditor)
            # subwnd.show()

        # try:
        #     for fname in fnames:
        #         if fname:
        #             existing = self.findMdiChild(fname)
        #             if existing:
        #                 self.mdiArea.setActiveSubWindow(existing)
        #             else:
        #                 # we need to create new subWindow and open the file
        #                 nodeeditor = WorkflowSubWindow()
        #                 if nodeeditor.fileLoad(fname):
        #                     self.statusBar().showMessage("File %s loaded" % fname, 5000)
        #                     nodeeditor.setTitle()
        #                     subwnd = self.createMdiChild(nodeeditor)
        #                     subwnd.show()
        #                 else:
        #                     nodeeditor.close()
        # except Exception as e:
        #     dumpException(e)
