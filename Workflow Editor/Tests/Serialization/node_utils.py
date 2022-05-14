import copy

from Tests.Serialization.general_utils import are_similar_, strip_id


def equals_nodes(actual,expected):
    return are_similar_(actual, expected) and \
           strip_id(copy.deepcopy(actual)) == strip_id(copy.deepcopy(expected))

