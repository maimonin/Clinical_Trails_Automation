LISTBOX_MIMETYPE = "application/x-item"

OP_NODE_STRING = 1

WORKFLOW_NODES={

}

class ConfException(Exception):pass
class InvalidNodeRegistration(ConfException): pass
class OpCodeNotRegistered(ConfException): pass

def register_node_now(op_code,class_reference):
    if op_code in WORKFLOW_NODES:
        raise InvalidNodeRegistration("Duplicate node registration of '%s'. There is already %s" % (
            op_code, WORKFLOW_NODES[op_code]
        ))
    WORKFLOW_NODES[op_code] = class_reference

def register_node(op_code):
    def decorator(original_class):
        register_node_now(op_code,original_class)
        return original_class
    return decorator

def get_class_from_opcode(op_code):
    if op_code not in WORKFLOW_NODES: raise OpCodeNotRegistered("OpCode '%d' is not registered" % op_code)
    return WORKFLOW_NODES[op_code]