import copy


def are_similar_(actual, expected):
    if type(actual) is not type(expected):
        return False
    if isinstance(actual, list):
        return are_similar_lists(actual, expected)
    if isinstance(actual, dict):
        return are_similar_dictionaries(actual, expected)
    return True


def actual_has_redundant_keys(actual, expected):
    for key in actual:
        if key not in expected:
            return False
    return True


def are_similar_dictionaries(actual, expected):
    if len(actual.keys()) != len(expected.keys()):
        return False
    for key in expected:
        if key not in actual:
            return False
        elif not are_similar_(actual[key], expected[key]):
            return False
    if actual_has_redundant_keys(actual, expected):
        return False
    return True


def are_similar_lists(actual, expected):
    if len(actual) is not len(expected):
        return False
    for i in range(len(actual)):
        if not are_similar_(actual[i], expected[i]):
            return False
    return True


def strip_id(obj):
    if isinstance(obj, dict):
        if "id" in obj:
            del obj["id"]
    if isinstance(obj, (dict, list)):
        for key in obj:
            if isinstance(obj[key], list):
                for item in obj[key]:
                    strip_id(item)
            if isinstance(obj[key], dict):
                strip_id(obj[key])
    return obj


def get_matching_socket(socket_to_match, sockets_ids_pairs):
    for first_id, second_id in sockets_ids_pairs:
        if first_id == socket_to_match:
            return second_id
        if second_id == socket_to_match:
            return first_id
    raise NonSharedElementExists  # should not happen


def get_matching_edge_from_second_flow_according_to_start_and_end_sockets(edges, start_socket_in_other_list,
                                                                          end_socket_in_other_list, sockets_ids_pairs):
    matching_start_socket = get_matching_socket(start_socket_in_other_list, sockets_ids_pairs)
    matching_end_socket = get_matching_socket(end_socket_in_other_list, sockets_ids_pairs)
    for edge in edges:
        if edge["start"] == matching_start_socket and edge["end"] == matching_end_socket:
            return edge
    raise NonSharedElementExists


def equals_edges(edge_in_first, edge_in_second):
    non_unified_keys = ["start", "end", "id"]
    values_in_first_object_without_fields_equals_second(edge_in_first, edge_in_second, non_unified_keys)


def edges_in_first_exists_in_second(first_edges, second_edges, sockets_ids_pairs):
    for edge_in_first in first_edges:
        start_socket_in_first = edge_in_first["start"]
        end_socket_in_first = edge_in_first["end"]
        edge_in_second = \
            get_matching_edge_from_second_flow_according_to_start_and_end_sockets(second_edges, start_socket_in_first,
                                                                                  end_socket_in_first,
                                                                                  sockets_ids_pairs)
        if not equals_edges(edge_in_first, edge_in_second):
            return False
    return True


def equals_edges_in_both_flows_according_to_ids(flow1, flow2, sockets_ids_pairs):
    edges1, edges2 = flow1["edges"], flow2["edges"]
    return edges_in_first_exists_in_second(edges1, edges2, sockets_ids_pairs) and edges_in_first_exists_in_second(
        edges2, edges1, sockets_ids_pairs)


def get_pairs_of_similar_sockets_ids_in_flows(flow1, flow2):
    return []


def values_in_first_object_without_fields_equals_second(first_flow, second_flow, exclude_fields=[]):
    for key in first_flow.keys() - exclude_fields:
        if key not in second_flow:
            raise NonSharedElementExists
        if first_flow[key] != second_flow[key]:
            return False
    return True


def equals_flows_metadata(flow1, flow2):
    non_meta_fields = ["edges", "nodes", "id"]
    return values_in_first_object_without_fields_equals_second(flow1, flow2, non_meta_fields) and \
           values_in_first_object_without_fields_equals_second(flow2, flow1, non_meta_fields)


def equals_flows(flow1, flow2):
    try:
        sockets_ids_pairs = get_pairs_of_similar_sockets_ids_in_flows(flow1, flow2)
        return equals_flows_metadata(flow1, flow2) and equals_edges_in_both_flows_according_to_ids(flow1,
                                                                                                   flow2,
                                                                                                   sockets_ids_pairs)
    except (NonSharedElementExists, KeyError) as e:
        raise e


class NonSharedElementExists(Exception):
    pass