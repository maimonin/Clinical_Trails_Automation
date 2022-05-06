from Database import Database
from Edges import NormalEdge, FixedTimeEdge, RelativeTimeEdge

edges = {}


def buildEdge(dal_edge):
    if dal_edge.id in edges:
        return edges[dal_edge.id]
    if dal_edge.type == 0:
        edges[dal_edge.id] = NormalEdge(dal_edge.id)
        return edges[dal_edge.id]
    elif dal_edge.type == 1:
        edges[dal_edge.id] = RelativeTimeEdge(dal_edge.id, dal_edge.min_time, dal_edge.max_time)
        return edges[dal_edge.id]
    else:
        edges[dal_edge.id] = FixedTimeEdge(dal_edge.id, dal_edge.min_time, dal_edge.max_time)
        return edges[dal_edge.id]


def getEdges(from_id):
    dal_edges = Database.getEdges(from_id)
    output = []
    for dal_edge in dal_edges:
        output.append(buildEdge(dal_edge))
    return output
