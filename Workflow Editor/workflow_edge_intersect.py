from nodeeditor.node_edge_intersect import EdgeIntersect

from workflow_edge import WorkflowEdge


class WorkflowEdgeIntersect(EdgeIntersect):
    def dropNode(self, node: "Node", scene_pos_x: float, scene_pos_y: float):
        """
        Code handling the dropping of a node on an existing edge.

        :param scene_pos_x: scene position x
        :type scene_pos_x: `float`
        :param scene_pos_y: scene position y
        :type scene_pos_y: `float`
        """

        node_box = self.hotZoneRect(node)

        # check if the node is dropped on an existing edge
        edge = self.intersect(node_box)
        if edge is None: return

        if self.isConnected(node): return

        # determine the order of start and end
        if edge.start_socket.is_output:
            socket_start = edge.start_socket
            socket_end = edge.end_socket
        else:
            socket_start = edge.end_socket
            socket_end = edge.start_socket

        # The new edges will have the same edge_type as the intersected edge
        edge_type = edge.edge_type

        edge.remove()
        self.grView.grScene.scene.history.storeHistory('Delete existing edge', setModified=True)

        new_node_socket_in = node.inputs[0]
        WorkflowEdge(self.grScene.scene, socket_start, new_node_socket_in, edge_type=edge_type)
        new_node_socket_out = node.outputs[0]
        WorkflowEdge(self.grScene.scene, new_node_socket_out, socket_end, edge_type=edge_type)

        self.grView.grScene.scene.history.storeHistory('Created new edges by dropping node', setModified=True)


