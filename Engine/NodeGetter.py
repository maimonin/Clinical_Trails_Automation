import Nodes
from Database import Database


def getNode(edge_id):
    return Nodes.buildNode(Database.getToNode(edge_id))
