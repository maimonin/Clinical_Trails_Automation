def buildDALEdge(edge_data):
    if edge_data[3] is None and edge_data[5]:
        return DALNormalEdge(edge_data[0])
    if edge_data[3] is not None and edge_data[5] is None:
        return DALRelativeTimeEdge(edge_data[0], edge_data[3], edge_data[4])
    return DALFixedTimeEdge(edge_data[0], edge_data[5], edge_data[6])


class DALNormalEdge:
    def __init__(self, edge_id):
        self.id = edge_id


class DALRelativeTimeEdge:
    def __init__(self, edge_id, min_time, max_time):
        self.id = edge_id
        self.min_time = min_time
        self.max_time = max_time


class DALFixedTimeEdge:
    def __init__(self, edge_id, min_time, max_time):
        self.id = edge_id
        self.min_time = min_time
        self.max_time = max_time
