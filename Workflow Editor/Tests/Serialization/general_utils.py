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
