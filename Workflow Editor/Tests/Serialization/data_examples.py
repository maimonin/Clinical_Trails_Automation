from workflow_conf_nodes import *

editor_data_examples = {
    "scene": {
        "editor empty scene": {
            "id": 2793750566176,
            "scene_width": 64000,
            "scene_height": 64000,
            "nodes": [],
            "edges": []
        },

    },
    "node": {
        "empty decision node": {"id": 1760666772672, "title": "Decision", "pos_x": 0.0,
                                "pos_y": 0.0, "inputs": [{"id": 1760666862160, "index": 0,
                                                          "multi_edges": False, "position": 7,
                                                          "socket_type": 1}], "outputs": [
                {"id": 1760666862112, "index": 0, "multi_edges": True, "position": 8, "socket_type": 4},
                {"id": 1760666862208, "index": 0, "multi_edges": True, "position": 5, "socket_type": 2}],
                                "content": {"node_details": {"title": "New Decision Node"},
                                            "condition": []}, "op_code": 3},
        "decision node with all condition types": {"id": 1760666772672, "title": "Decision", "pos_x": 0.0,
                                                   "pos_y": 0.0, "inputs": [{"id": 1760666862160, "index": 0,
                                                                             "multi_edges": False, "position": 7,
                                                                             "socket_type": 1}], "outputs": [
                {"id": 1760666862112, "index": 0, "multi_edges": True, "position": 8, "socket_type": 4},
                {"id": 1760666862208, "index": 0, "multi_edges": True, "position": 5, "socket_type": 2}],
                                                   "content": {"node_details": {"title": "New Decision Node"},
                                                               "condition": [{
                                                                   "title": "First",
                                                                   "type": "trait condition",
                                                                   "trait": "age",
                                                                   "satisfy": {
                                                                       "type": "range",
                                                                       "value": {"min": 0, "max": 10}

                                                                   }}, {
                                                                   "title": "second",
                                                                   "type": "test condition",
                                                                   "test": "blood",
                                                                   "satisfy": {
                                                                       "type": "one_choice",
                                                                       "value": "b+"

                                                                   }
                                                               }
                                                                   , {
                                                                       "title": "third",
                                                                       "type": "questionnaire condition",
                                                                       "questionnaireNumber": 1,
                                                                       "questionNumber": 2,
                                                                       "acceptedAnswers": [1, 2]
                                                                   }

                                                               ]}, "op_code": 3}
    }
}
engine_data_examples = {
    "node": {
        "decision": {
            "empty": {"id": 1760666772672, "title": "Decision",
                      "inputs": [1760666862160], "outputs": [1760666862112, 176066686220],
                      "content": {"node_details": {"title": "New Decision Node"},
                                  "condition": []}, "op_code": 3},
            "with all condition types": {"id": 1760666772672, "title": "Decision",
                                         "inputs": [1760666862160], "outputs": [1760666862112, 176066686220],
                                         "content": {"node_details": {"title": "New Decision Node"},
                                                     "condition": [{
                                                         "title": "First",
                                                         "type": "trait condition",
                                                         "trait": "age",
                                                         "satisfy": {
                                                             "type": "range",
                                                             "value": {"min": 0, "max": 10}

                                                         }}, {
                                                         "title": "second",
                                                         "type": "test condition",
                                                         "test": "blood",
                                                         "satisfy": {
                                                             "type": "one_choice",
                                                             "value": "b+"

                                                         }
                                                     }
                                                         , {
                                                             "title": "third",
                                                             "type": "questionnaire condition",
                                                             "questionnaireNumber": 1,
                                                             "questionNumber": 2,
                                                             "acceptedAnswers": [1, 2]
                                                         }

                                                     ]}, "op_code": 3}},
        "complex": {
            "empty": {
                "id": 1111,
                "title": "Sub Workflow",
                "inputs": [],
                "outputs": [],
                "op_code": 6,
                "content": {"type": "complex", "flow": {}}
            }

        },
        "simple string": {
            "empty": {
                "id": 11111,
                "title": "Simple String",
                "inputs": [],
                "outputs": [],
                "op_code": 4,
                "content": {
                    "node_details": {
                        "actors": [],
                        "title": "New Notification Node"
                    },
                    "text": ""
                }
            },
            "with_changes": {
                "id": 11111,
                "title": "Simple String",
                "inputs": [],
                "outputs": [],
                "op_code": 4,
                "content": {
                    "node_details": {
                        "actors": ["Nurse"],
                        "title": "changed title"
                    },
                    "text": "changed notification value"
                }
            },

        },
        "data entry": {
            "empty": {
                "id": 11111,
                "title": "Test",
                "inputs": [],
                "outputs": [],
                "op_code": 2,
                "content": {
                    "node_details": {
                        "title": "New Test Node",
                    },
                    "tests": []
                }
            }

        },
        "questionnaire": {
            "empty": {
                "id": 11111,
                "title": "Questionnaire",
                "inputs": [],
                "outputs": [],
                "op_code": 1,
                "content": {
                    "node_details": {
                        "title": "New Questionnaire Node",
                    },
                    "questions": [],
                    "qusetionnaire_number": 1
                }
            },
            "changed title": {
                "id": 11111,
                "title": "Questionnaire",
                "inputs": [],
                "outputs": [],
                "op_code": 1,
                "content": {
                    "node_details": {
                        "title": "changed title",
                    },
                    "questions": [],
                    "qusetionnaire_number": 1
                }
            },
            "changed questionnaire number": {
                "id": 11111,
                "title": "Questionnaire",
                "inputs": [],
                "outputs": [],
                "op_code": 1,
                "content": {
                    "node_details": {
                        "title": "New Questionnaire Node",
                    },
                    "questions": [],
                    "qusetionnaire_number": 2
                }
            },
            "one multi question": {
                "id": 11111,
                "title": "Questionnaire",
                "inputs": [],
                "outputs": [],
                "op_code": 1,
                "content": {
                    "node_details": {
                        "title": "New Questionnaire Node",
                    },
                    "questions": [{
                        "text": "multiple question",
                        "options": ["option 1", " option 2"],
                        "type": "multi"
                    }],
                    "qusetionnaire_number": 1
                }
            },
            "one open question": {
                "id": 11111,
                "title": "Questionnaire",
                "inputs": [],
                "outputs": [],
                "op_code": 1,
                "content": {
                    "node_details": {
                        "title": "New Questionnaire Node",
                    },
                    "questions": [{
                        "text": "open question",
                        "type": "open"
                    }],
                    "qusetionnaire_number": 1
                }
            },
            "one single choice question": {
                "id": 11111,
                "title": "Questionnaire",
                "inputs": [],
                "outputs": [],
                "op_code": 1,
                "content": {
                    "node_details": {
                        "title": "New Questionnaire Node",
                    },
                    "questions": [{
                        "text": "single choice question",
                        "options": ["option 1", " option 2"],
                        "type": "one choice"
                    }],
                    "qusetionnaire_number": 1
                }
            },

        },
        "start": {
            "id": 1892803102752,
            "title": "New Start Node",
            "inputs": [],
            "outputs": [
                {
                    "id": 1892803103088
                }
            ],
            "op_code": 0
        },
        "finish": {
            "id": 1892817027280,
            "title": "New Finish Node",
            "inputs": [
                {
                    "id": 1892817027520
                }
            ],
            "outputs": [],
            "op_code": 6
        },
        "node general structure": {
            "id": int,
            "title": str,
            "inputs": list,
            "outputs": list,
            "op_code": int,
            "content": dict

        },
        "node input items type": int,
        "node outputs items type": int,

    }
}
node_classes = [WorkflowNode_Decision, WorkflowNode_ComplexNode, WorkflowNode_SimpleString, WorkflowNode_DataEntry,
                WorkflowNode_Questionnaire]
