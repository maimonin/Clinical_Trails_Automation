from nodeeditor.node_edge import Edge, EDGE_TYPE_DIRECT

from workflow_graphics_edge import WFGraphicsEdgeText


class WorkflowEdge(Edge):
    def __init__(self, scene:'Scene', start_socket:'Socket'=None, end_socket:'Socket'=None, edge_type=EDGE_TYPE_DIRECT,text="No Node"):

        super().__init__(scene,start_socket,end_socket,edge_type)
        self._text = text



        if self.end_socket is not None:
            self.grTextEdge = self.createTextEdgeClassInstance()
            self.text = text
            self.updatePositions()
    @property
    def text(self):
        """title of this `Node`

        :getter: current Graphics Node title
        :setter: stores and make visible the new title
        :type: str
        """
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.grTextEdge.text = self._text
    def createEdgeClassInstance(self):
        """
        Create instance of grEdge class
        :return: Instance of `grEdge` class representing the Graphics Edge in the grScene
        """
        self.grEdge = self.getGraphicsEdgeClass()(self)
        if self.start_socket is not None:
            self.updatePositionsNoText()
        self.scene.grScene.addItem(self.grEdge)
        return self.grEdge
    def createTextEdgeClassInstance(self):
        """
        Create instance of grEdge class
        :return: Instance of `grEdge` class representing the Graphics Edge in the grScene
        """
        self.grTextEdge = self.getTextGraphicsEdgeClass()(self)
        self.scene.grScene.addItem(self.grTextEdge)

        return self.grTextEdge
    def getTextGraphicsEdgeClass(self):
        return WFGraphicsEdgeText

    def updatePositions(self):
        """
        Updates the internal `Graphics Edge` positions according to the start and end :class:`~nodeeditor.node_socket.Socket`.
        This should be called if you update ``Edge`` positions.
        """
        source_pos = self.start_socket.getSocketPosition()
        source_pos[0] += self.start_socket.node.grNode.pos().x()
        source_pos[1] += self.start_socket.node.grNode.pos().y()
        self.grEdge.setSource(*source_pos)

        self.grTextEdge.setSource(*source_pos)
        if self.end_socket is not None:
            end_pos = self.end_socket.getSocketPosition()
            end_pos[0] += self.end_socket.node.grNode.pos().x()
            end_pos[1] += self.end_socket.node.grNode.pos().y()
            self.grEdge.setDestination(*end_pos)
            self.grTextEdge.setDestination(*end_pos)

        else:
            self.grEdge.setDestination(*source_pos)
        self.grEdge.update()
        self.grTextEdge.update()

    def updatePositionsNoText(self):
        super().updatePositions()