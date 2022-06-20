import pytest
from unittest.mock import patch

from Tests.Serialization.general_utils import are_similar_, equals_flows
from Tests.Serialization.node_utils import equals_nodes
from workflow_conf_nodes import *
from workflow_scene import WorkflowScene
from data_examples import *


def conv_node(scene, node: list):
    new_node = None
    if node["op_code"] == 0:
        new_node = WorkflowNode_Start(scene)
        for key in node.keys():
            setattr(new_node, key, node[key])
    elif node["op_code"] == 6:
        new_node = WorkflowNode_Finish(scene)
        for key in node.keys():
            setattr(new_node, key, node[key])
    elif node["op_code"] == 4:
        new_node = WorkflowNode_SimpleString(scene)
        for key in node.keys():
            setattr(new_node, key, node[key])
    elif node["op_code"] == 3:
        new_node = WorkflowNode_Decision(scene)
        for key in node.keys():
            setattr(new_node, key, node[key])
    elif node["op_code"] == 1:
        new_node = WorkflowNode_Questionnaire(scene)
        for key in node.keys():
            setattr(new_node, key, node[key])
    elif node["op_code"] == 2:
        new_node = WorkflowNode_DataEntry(scene)
        for key in node.keys():
            setattr(new_node, key, node[key])
    elif node["op_code"] == 5:
        new_node = WorkflowNode_ComplexNode(scene)
        for key in node.keys():
            setattr(new_node, key, node[key])

    return new_node


def conv_edge(scene, edge: list):
    new_edge = WorkflowEdge(scene)
    for key in edge.keys():
        # new_edge[key] = edge[key]
        setattr(new_edge, key, edge[key])

    return new_edge


@pytest.fixture
def empty_scene():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
    return scene


@pytest.fixture
def notification_scene():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
        nodes_list = [
            {
                "id": 1722776576688,
                "title": "New Start Node",
                "pos_x": -350.0,
                "pos_y": -250.0,
                "inputs": [],
                "outputs": [
                    {
                        "id": 1722776429520,
                        "index": 0,
                        "multi_edges": True,
                        "position": 5,
                        "socket_type": 2
                    }
                ],
                "content": "",
                "op_code": 0
            },
            {
                "id": 1722776499296,
                "title": "New Finish Node",
                "pos_x": 200.0,
                "pos_y": 0.0,
                "inputs": [
                    {
                        "id": 1722776429664,
                        "index": 0,
                        "multi_edges": True,
                        "position": 2,
                        "socket_type": 2
                    }
                ],
                "outputs": [],
                "content": "",
                "op_code": 6
            },
            {
                "id": 1722785223008,
                "title": "Notification",
                "pos_x": -142.0,
                "pos_y": -140.0,
                "inputs": [
                    {
                        "id": 1722785135200,
                        "index": 0,
                        "multi_edges": True,
                        "position": 2,
                        "socket_type": 1
                    }
                ],
                "outputs": [
                    {
                        "id": 1722785135152,
                        "index": 0,
                        "multi_edges": True,
                        "position": 5,
                        "socket_type": 1
                    }
                ],
                "content": {
                    "node_details": {
                        "actors": [
                            "Participant"
                        ],
                        "title": "Welcome",
                        "color": "Grey"
                    },
                    "text": "Hello World"
                },
                "op_code": 4
            }
        ]
        edges_list = [
            {
                "id": 1722785081424,
                "start": 1722776429520,
                "end": 1722785135200,
                "type": 0,
                "edge_type": 2
            },
            {
                "id": 1722785081952,
                "start": 1722785135152,
                "end": 1722776429664,
                "type": 0,
                "edge_type": 2
            }
        ]
        for node in nodes_list:
            scene.nodes.append(conv_node(scene, node))
        for edge in edges_list:
            scene.edges.append(conv_edge(scene, edge))

    return scene


@pytest.fixture
def decision_trait_scene():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
        nodes_list = [
            {
                "id": 1722785223056,
                "title": "New Start Node",
                "pos_x": -350.0,
                "pos_y": -250.0,
                "inputs": [],
                "outputs": [
                    {
                        "id": 1722785243536,
                        "index": 0,
                        "multi_edges": True,
                        "position": 5,
                        "socket_type": 2
                    }
                ],
                "content": "",
                "op_code": 0
            },
            {
                "id": 1722785243488,
                "title": "New Finish Node",
                "pos_x": 353.0,
                "pos_y": 146.0,
                "inputs": [
                    {
                        "id": 1722785243680,
                        "index": 0,
                        "multi_edges": True,
                        "position": 2,
                        "socket_type": 2
                    }
                ],
                "outputs": [],
                "content": "",
                "op_code": 6
            },
            {
                "id": 1722785243632,
                "title": "Decision",
                "pos_x": -200.0,
                "pos_y": -156.0,
                "inputs": [
                    {
                        "id": 1722785244544,
                        "index": 0,
                        "multi_edges": False,
                        "position": 7,
                        "socket_type": 1
                    }
                ],
                "outputs": [
                    {
                        "id": 1722785243248,
                        "index": 0,
                        "multi_edges": True,
                        "position": 8,
                        "socket_type": 4
                    },
                    {
                        "id": 1722785244592,
                        "index": 0,
                        "multi_edges": True,
                        "position": 5,
                        "socket_type": 2
                    }
                ],
                "content": {
                    "node_details": {
                        "title": "Gender split"
                    },
                    "condition": [
                        {
                            "id": 1,
                            "title": "condition 1",
                            "type": "trait condition",
                            "satisfy": {
                                "type": "one_choice",
                                "value": "male"
                            },
                            "trait": "Gender"
                        }
                    ]
                },
                "op_code": 3
            },
            {
                "id": 1722785244640,
                "title": "Notification",
                "pos_x": 0.0,
                "pos_y": -68.0,
                "inputs": [
                    {
                        "id": 1722751452112,
                        "index": 0,
                        "multi_edges": True,
                        "position": 2,
                        "socket_type": 1
                    }
                ],
                "outputs": [
                    {
                        "id": 1722751452160,
                        "index": 0,
                        "multi_edges": True,
                        "position": 5,
                        "socket_type": 1
                    }
                ],
                "content": {
                    "node_details": {
                        "actors": [
                            "Participant"
                        ],
                        "title": "Male Participant",
                        "color": "Grey"
                    },
                    "text": "Continue trial"
                },
                "op_code": 4
            },
            {
                "id": 1722785244928,
                "title": "Notification",
                "pos_x": -75.0,
                "pos_y": 61.0,
                "inputs": [
                    {
                        "id": 1722751452688,
                        "index": 0,
                        "multi_edges": True,
                        "position": 2,
                        "socket_type": 1
                    }
                ],
                "outputs": [
                    {
                        "id": 1722751452064,
                        "index": 0,
                        "multi_edges": True,
                        "position": 5,
                        "socket_type": 1
                    }
                ],
                "content": {
                    "node_details": {
                        "actors": [
                            "Participant"
                        ],
                        "title": "Female Participant",
                        "color": "Grey"
                    },
                    "text": "This trial is for men."
                },
                "op_code": 4
            }
        ]
        edges_list = [
            {
                "id": 1722751452640,
                "start": 1722785244592,
                "end": 1722751452112,
                "type": 0,
                "edge_type": 2
            },
            {
                "id": 1722751452304,
                "start": 1722785243248,
                "end": 1722751452688,
                "type": 0,
                "edge_type": 2
            },
            {
                "id": 1722751453408,
                "start": 1722751452064,
                "end": 1722785243680,
                "type": 0,
                "edge_type": 2
            },
            {
                "id": 1722785244112,
                "start": 1722751452160,
                "end": 1722785243680,
                "type": 0,
                "edge_type": 2
            },
            {
                "id": 1722785244304,
                "start": 1722785244544,
                "end": 1722785243536,
                "type": 0,
                "edge_type": 2
            }
        ]
        for node in nodes_list:
            scene.nodes.append(conv_node(scene, node))
        for edge in edges_list:
            scene.edges.append(conv_edge(scene, edge))
    return scene


@pytest.fixture
def decision_questionnaire_scene():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
        nodes_list = [
            {
                "id": 1722752046704,
                "title": "New Start Node",
                "inputs": [],
                "outputs": [
                    {
                        "id": 1722752047088
                    }
                ],
                "op_code": 0
            },
            {
                "id": 1722752047040,
                "title": "New Finish Node",
                "inputs": [
                    {
                        "id": 1722752047232
                    }
                ],
                "outputs": [],
                "op_code": 6
            },
            {
                "id": 1722752047184,
                "title": "Questionnaire",
                "inputs": [
                    {
                        "id": 1722752047568
                    }
                ],
                "outputs": [
                    {
                        "id": 1722752047616
                    }
                ],
                "content": {
                    "node_details": {
                        "title": "Food preferences"
                    },
                    "questions": [
                        {
                            "type": "one choice",
                            "text": "How often do you eat sweeities?",
                            "options": [
                                "Daily",
                                "Some days in the week",
                                "Once in a week",
                                "Once in a while",
                                "Never"
                            ]
                        },
                        {
                            "type": "open",
                            "text": "ID:"
                        },
                        {
                            "type": "multi",
                            "text": "What is your daily nutrition?",
                            "options": [
                                "Meat",
                                "Salad",
                                "Dairy",
                                "Fish",
                                "Snacks"
                            ]
                        }
                    ],
                    "questionnaire_number": 1
                },
                "op_code": 1
            },
            {
                "id": 1722752048528,
                "title": "Decision",
                "inputs": [
                    {
                        "id": 1722752048000
                    }
                ],
                "outputs": [
                    {
                        "id": 1722752048912
                    },
                    {
                        "id": 1722752048864
                    }
                ],
                "content": {
                    "node_details": {
                        "title": "Junk Eaters Split"
                    },
                    "condition": [
                        {
                            "title": "condition 1",
                            "type": "trait condition",
                            "satisfy": {
                                "type": "range",
                                "value": {
                                    "min": -1,
                                    "max": -1
                                }
                            },
                            "trait": ""
                        },
                        {
                            "title": "questionnaire condition 1",
                            "type": "questionnaire condition",
                            "questionnaireNumber": 1,
                            "questionNumber": 3,
                            "acceptedAnswers": [
                                4
                            ]
                        }
                    ]
                },
                "op_code": 3
            },
            {
                "id": 1722785244400,
                "title": "Notification",
                "inputs": [
                    {
                        "id": 1722752048240
                    }
                ],
                "outputs": [
                    {
                        "id": 1722752045744
                    }
                ],
                "content": {
                    "node_details": {
                        "actors": [
                            "Doctor"
                        ],
                        "title": "Unhealthy nutrition"
                    },
                    "text": "There is Unhealthy habits in participants"
                },
                "op_code": 4
            },
            {
                "id": 1722752048480,
                "title": "Notification",
                "inputs": [
                    {
                        "id": 1722752047280
                    }
                ],
                "outputs": [
                    {
                        "id": 1722752046080
                    }
                ],
                "content": {
                    "node_details": {
                        "actors": [
                            "Participant"
                        ],
                        "title": "Others"
                    },
                    "text": "Choclate is the best."
                },
                "op_code": 4
            }
        ]
        edges_list = [
            {
                "id": 1722752048336,
                "start": 1722752047088,
                "end": 1722752047568,
                "type": 0
            },
            {
                "id": 1722752047712,
                "start": 1722752047616,
                "end": 1722752048000,
                "type": 0
            },
            {
                "id": 1722752045552,
                "start": 1722752048864,
                "end": 1722752048240,
                "type": 0
            },
            {
                "id": 1722752045504,
                "start": 1722752048912,
                "end": 1722752047280,
                "type": 0
            },
            {
                "id": 1722752048960,
                "start": 1722752046080,
                "end": 1722752047232,
                "type": 0
            },
            {
                "id": 1722752131424,
                "start": 1722752045744,
                "end": 1722752047232,
                "type": 0
            }
        ]
        for node in nodes_list:
            scene.nodes.append(conv_node(scene, node))
        for edge in edges_list:
            scene.edges.append(conv_edge(scene, edge))
    return scene


@pytest.fixture
def decision_test_scene():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
        nodes_list = [
            {
                "id": 1722752046224,
                "title": "New Start Node",
                "pos_x": -488.0,
                "pos_y": -339.0,
                "inputs": [],
                "outputs": [
                    {
                        "id": 1722752046032,
                        "index": 0,
                        "multi_edges": True,
                        "position": 5,
                        "socket_type": 2
                    }
                ],
                "content": "",
                "op_code": 0
            },
            {
                "id": 1722752045456,
                "title": "New Finish Node",
                "pos_x": 426.0,
                "pos_y": 153.0,
                "inputs": [
                    {
                        "id": 1722752132240,
                        "index": 0,
                        "multi_edges": True,
                        "position": 2,
                        "socket_type": 2
                    }
                ],
                "outputs": [],
                "content": "",
                "op_code": 6
            },
            {
                "id": 1722752135072,
                "title": "Test",
                "pos_x": -362.0,
                "pos_y": -278.0,
                "inputs": [
                    {
                        "id": 1722752824464,
                        "index": 0,
                        "multi_edges": True,
                        "position": 2,
                        "socket_type": 1
                    }
                ],
                "outputs": [
                    {
                        "id": 1722752824512,
                        "index": 0,
                        "multi_edges": True,
                        "position": 5,
                        "socket_type": 1
                    }
                ],
                "content": {
                    "node_details": {
                        "title": "Blood Test",
                        "actor in charge": "Lab Technician",
                        "color": "Grey"
                    },
                    "tests": [
                        {
                            "id": 1,
                            "name": "Iron In Blood",
                            "instructions": "Use Magnets  to search for iron",
                            "staff": [
                                "Nurse",
                                "Lab Technician",
                                "Participant"
                            ],
                            "duration": "15"
                        }
                    ]
                },
                "op_code": 2
            },
            {
                "id": 1722752826144,
                "title": "Decision",
                "pos_x": -62.0,
                "pos_y": -191.0,
                "inputs": [
                    {
                        "id": 1722752826432,
                        "index": 0,
                        "multi_edges": False,
                        "position": 7,
                        "socket_type": 1
                    }
                ],
                "outputs": [
                    {
                        "id": 1722752826384,
                        "index": 0,
                        "multi_edges": True,
                        "position": 8,
                        "socket_type": 4
                    },
                    {
                        "id": 1722752826480,
                        "index": 0,
                        "multi_edges": True,
                        "position": 5,
                        "socket_type": 2
                    }
                ],
                "content": {
                    "node_details": {
                        "title": "Iron People"
                    },
                    "condition": [
                        {
                            "id": 1,
                            "title": "condition 1",
                            "type": "test condition",
                            "satisfy": {
                                "type": "one_choice",
                                "value": "positive"
                            },
                            "test": "Iron In Blood"
                        }
                    ]
                },
                "op_code": 3
            },
            {
                "id": 1722752134832,
                "title": "Notification",
                "pos_x": -108.0,
                "pos_y": 39.0,
                "inputs": [
                    {
                        "id": 1722752825856,
                        "index": 0,
                        "multi_edges": True,
                        "position": 2,
                        "socket_type": 1
                    }
                ],
                "outputs": [
                    {
                        "id": 1722752826000,
                        "index": 0,
                        "multi_edges": True,
                        "position": 5,
                        "socket_type": 1
                    }
                ],
                "content": {
                    "node_details": {
                        "actors": [
                            "Participant"
                        ],
                        "title": "Normal People",
                        "color": "Grey"
                    },
                    "text": "Youre not interesting."
                },
                "op_code": 4
            },
            {
                "id": 1722752825952,
                "title": "Notification",
                "pos_x": 84.0,
                "pos_y": -132.0,
                "inputs": [
                    {
                        "id": 1722752826624,
                        "index": 0,
                        "multi_edges": True,
                        "position": 2,
                        "socket_type": 1
                    }
                ],
                "outputs": [
                    {
                        "id": 1722752826720,
                        "index": 0,
                        "multi_edges": True,
                        "position": 5,
                        "socket_type": 1
                    }
                ],
                "content": {
                    "node_details": {
                        "actors": [
                            "Lab Technician",
                            "Doctor"
                        ],
                        "title": "Aliens",
                        "color": "Grey"
                    },
                    "text": "Alien was found."
                },
                "op_code": 4
            }
        ]
        edges_list = [
            {
                "id": 1722752825184,
                "start": 1722752046032,
                "end": 1722752824464,
                "type": 0,
                "edge_type": 2
            },
            {
                "id": 1722752826192,
                "start": 1722752824512,
                "end": 1722752826432,
                "type": 0,
                "edge_type": 2
            },
            {
                "id": 1722752825760,
                "start": 1722752826384,
                "end": 1722752825856,
                "type": 0,
                "edge_type": 2
            },
            {
                "id": 1722752825040,
                "start": 1722752826000,
                "end": 1722752132240,
                "type": 0,
                "edge_type": 2
            },
            {
                "id": 1722752825808,
                "start": 1722752826480,
                "end": 1722752826624,
                "type": 0,
                "edge_type": 2
            },
            {
                "id": 1722752825328,
                "start": 1722752826720,
                "end": 1722752132240,
                "type": 0,
                "edge_type": 2
            }
        ]
        for node in nodes_list:
            scene.nodes.append(conv_node(scene, node))
        for edge in edges_list:
            scene.edges.append(conv_edge(scene, edge))
    return scene


@pytest.fixture
def questionnaire_scene():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
        nodes_list = [
            {
                "id": 1722753095376,
                "title": "New Start Node",
                "pos_x": -488.0,
                "pos_y": -266.0,
                "inputs": [],
                "outputs": [
                    {
                        "id": 1722753095760,
                        "index": 0,
                        "multi_edges": True,
                        "position": 5,
                        "socket_type": 2
                    }
                ],
                "content": "",
                "op_code": 0
            },
            {
                "id": 1722753095712,
                "title": "New Finish Node",
                "pos_x": 200.0,
                "pos_y": 0.0,
                "inputs": [
                    {
                        "id": 1722753095904,
                        "index": 0,
                        "multi_edges": True,
                        "position": 2,
                        "socket_type": 2
                    }
                ],
                "outputs": [],
                "content": "",
                "op_code": 6
            },
            {
                "id": 1722753095856,
                "title": "Questionnaire",
                "pos_x": -241.0,
                "pos_y": -142.0,
                "inputs": [
                    {
                        "id": 1722753096240,
                        "index": 0,
                        "multi_edges": True,
                        "position": 2,
                        "socket_type": 1
                    }
                ],
                "outputs": [
                    {
                        "id": 1722753096288,
                        "index": 0,
                        "multi_edges": True,
                        "position": 5,
                        "socket_type": 1
                    }
                ],
                "content": {
                    "node_details": {
                        "title": "Philosophic question",
                        "color": "Grey"
                    },
                    "questions": [
                        {
                            "id": 1,
                            "type": "open",
                            "text": "To be or not to be?"
                        }
                    ],
                    "questionnaire_number": "1"
                },
                "op_code": 1
            }
        ]
        edges_list = [
            {
                "id": 1722753097008,
                "start": 1722753095760,
                "end": 1722753096240,
                "type": 0,
                "edge_type": 2
            },
            {
                "id": 1722753096720,
                "start": 1722753096288,
                "end": 1722753095904,
                "type": 0,
                "edge_type": 2
            }
        ]
        for node in nodes_list:
            scene.nodes.append(conv_node(scene, node))
        for edge in edges_list:
            scene.edges.append(conv_edge(scene, edge))
    return scene


@pytest.fixture
def test_scene():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
        nodes_list = [
            {
                "id": 1722753097200,
                "title": "New Start Node",
                "pos_x": -350.0,
                "pos_y": -250.0,
                "inputs": [],
                "outputs": [
                    {
                        "id": 1722753097680,
                        "index": 0,
                        "multi_edges": True,
                        "position": 5,
                        "socket_type": 2
                    }
                ],
                "content": "",
                "op_code": 0
            },
            {
                "id": 1722753097152,
                "title": "New Finish Node",
                "pos_x": 200.0,
                "pos_y": 0.0,
                "inputs": [
                    {
                        "id": 1722753096624,
                        "index": 0,
                        "multi_edges": True,
                        "position": 2,
                        "socket_type": 2
                    }
                ],
                "outputs": [],
                "content": "",
                "op_code": 6
            },
            {
                "id": 1722753096576,
                "title": "Test",
                "pos_x": -177.0,
                "pos_y": -155.0,
                "inputs": [
                    {
                        "id": 1722753094176,
                        "index": 0,
                        "multi_edges": True,
                        "position": 2,
                        "socket_type": 1
                    }
                ],
                "outputs": [
                    {
                        "id": 1722753094224,
                        "index": 0,
                        "multi_edges": True,
                        "position": 5,
                        "socket_type": 1
                    }
                ],
                "content": {
                    "node_details": {
                        "title": "Migrene Test",
                        "actor in charge": "Nurse",
                        "color": "Grey"
                    },
                    "tests": [
                        {
                            "id": 1,
                            "name": "Migrene Test",
                            "instructions": "Insert Patient to CT machine",
                            "staff": [
                                "Nurse",
                                "Doctor",
                                "Participant"
                            ],
                            "duration": "120"
                        }
                    ]
                },
                "op_code": 2
            }
        ]
        edges_list = [
            {
                "id": 1722752826288,
                "start": 1722753097680,
                "end": 1722753094176,
                "type": 0,
                "edge_type": 2
            },
            {
                "id": 1722752826912,
                "start": 1722753094224,
                "end": 1722753096624,
                "type": 0,
                "edge_type": 2
            }
        ]
        for node in nodes_list:
            scene.nodes.append(conv_node(scene, node))
        for edge in edges_list:
            scene.edges.append(conv_edge(scene, edge))
    return scene


@pytest.fixture
def subworkflow_scene():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
        nodes_list = [
            {
                "id": 1722753292416,
                "title": "New Start Node",
                "pos_x": -350.0,
                "pos_y": -250.0,
                "inputs": [],
                "outputs": [
                    {
                        "id": 1722753292896,
                        "index": 0,
                        "multi_edges": True,
                        "position": 5,
                        "socket_type": 2
                    }
                ],
                "content": "",
                "op_code": 0
            },
            {
                "id": 1722753292848,
                "title": "New Finish Node",
                "pos_x": 200.0,
                "pos_y": 0.0,
                "inputs": [
                    {
                        "id": 1722753293040,
                        "index": 0,
                        "multi_edges": True,
                        "position": 2,
                        "socket_type": 2
                    }
                ],
                "outputs": [],
                "content": "",
                "op_code": 6
            },
            {
                "id": 1722753292992,
                "title": "Sub Workflow",
                "pos_x": -217.0,
                "pos_y": -134.0,
                "inputs": [
                    {
                        "id": 1722753293376,
                        "index": 0,
                        "multi_edges": True,
                        "position": 2,
                        "socket_type": 1
                    }
                ],
                "outputs": [
                    {
                        "id": 1722753293424,
                        "index": 0,
                        "multi_edges": True,
                        "position": 5,
                        "socket_type": 1
                    }
                ],
                "content": {
                    "node_details": {
                        "title": "Sub-Workflow",
                        "color": "Grey"
                    },
                    "flow": {
                        "id": 1722753094560,
                        "scene_width": 64000,
                        "scene_height": 64000,
                        "nodes": [
                            {
                                "id": 1722753094128,
                                "title": "New Start Node",
                                "pos_x": -350.0,
                                "pos_y": -250.0,
                                "inputs": [],
                                "outputs": [
                                    {
                                        "id": 1722753094800,
                                        "index": 0,
                                        "multi_edges": True,
                                        "position": 5,
                                        "socket_type": 2
                                    }
                                ],
                                "content": "",
                                "op_code": 0
                            },
                            {
                                "id": 1722753093888,
                                "title": "New Finish Node",
                                "pos_x": 200.0,
                                "pos_y": 0.0,
                                "inputs": [
                                    {
                                        "id": 1722752824992,
                                        "index": 0,
                                        "multi_edges": True,
                                        "position": 2,
                                        "socket_type": 2
                                    }
                                ],
                                "outputs": [],
                                "content": "",
                                "op_code": 6
                            },
                            {
                                "id": 1722752826528,
                                "title": "Notification",
                                "pos_x": -179.0,
                                "pos_y": -120.0,
                                "inputs": [
                                    {
                                        "id": 1722752825904,
                                        "index": 0,
                                        "multi_edges": True,
                                        "position": 2,
                                        "socket_type": 1
                                    }
                                ],
                                "outputs": [
                                    {
                                        "id": 1722752825376,
                                        "index": 0,
                                        "multi_edges": True,
                                        "position": 5,
                                        "socket_type": 1
                                    }
                                ],
                                "content": {
                                    "node_details": {
                                        "actors": [
                                            "Nurse",
                                            "Doctor",
                                            "Participant",
                                            "Investigator",
                                            "Lab Technician"
                                        ],
                                        "title": "Greetings",
                                        "color": "Grey"
                                    },
                                    "text": "Have a nice day."
                                },
                                "op_code": 4
                            }
                        ],
                        "edges": [
                            {
                                "id": 1722753291744,
                                "start": 1722753094800,
                                "end": 1722752825904,
                                "type": 0,
                                "edge_type": 2
                            },
                            {
                                "id": 1722752826048,
                                "start": 1722752825376,
                                "end": 1722752824992,
                                "type": 0,
                                "edge_type": 2
                            }
                        ]
                    },
                    "type": "complex"
                },
                "op_code": 5
            }
        ]
        edges_list = [
            {
                "id": 1722753292176,
                "start": 1722753292896,
                "end": 1722753293376,
                "type": 0,
                "edge_type": 2
            },
            {
                "id": 1722753290496,
                "start": 1722753293424,
                "end": 1722753293040,
                "type": 0,
                "edge_type": 2
            }
        ]
        for node in nodes_list:
            scene.nodes.append(conv_node(scene, node))
        for edge in edges_list:
            scene.edges.append(conv_edge(scene, edge))
    return scene


@pytest.fixture
def covid_scene():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
        nodes_list = [
            {
                "id": 2215627408048,
                "title": "New Start Node",
                "pos_x": -350.0,
                "pos_y": -250.0,
                "inputs": [],
                "outputs": [
                    {
                        "id": 2215627920336,
                        "index": 0,
                        "multi_edges": True,
                        "position": 5,
                        "socket_type": 2
                    }
                ],
                "content": "",
                "op_code": 0
            },
            {
                "id": 2215627945056,
                "title": "New Finish Node",
                "pos_x": 200.0,
                "pos_y": 0.0,
                "inputs": [
                    {
                        "id": 2215627920480,
                        "index": 0,
                        "multi_edges": True,
                        "position": 2,
                        "socket_type": 2
                    }
                ],
                "outputs": [],
                "content": "",
                "op_code": 6
            },
            {
                "id": 2215628099936,
                "title": "Notification",
                "pos_x": -448.0,
                "pos_y": -30.0,
                "inputs": [
                    {
                        "id": 2215628121520,
                        "index": 0,
                        "multi_edges": True,
                        "position": 2,
                        "socket_type": 1
                    }
                ],
                "outputs": [
                    {
                        "id": 2215628121568,
                        "index": 0,
                        "multi_edges": True,
                        "position": 5,
                        "socket_type": 1
                    }
                ],
                "content": {
                    "node_details": {
                        "actors": [
                            "Participant"
                        ],
                        "title": "Red Light",
                        "color": "Red"
                    },
                    "text": "Stop : Red light."
                },
                "op_code": 4
            },
            {
                "id": 2215627676352,
                "title": "Notification",
                "pos_x": 40.0,
                "pos_y": -201.0,
                "inputs": [
                    {
                        "id": 2215627676208,
                        "index": 0,
                        "multi_edges": True,
                        "position": 2,
                        "socket_type": 1
                    }
                ],
                "outputs": [
                    {
                        "id": 2215627676256,
                        "index": 0,
                        "multi_edges": True,
                        "position": 5,
                        "socket_type": 1
                    }
                ],
                "content": {
                    "node_details": {
                        "actors": [
                            "Participant"
                        ],
                        "title": "Green Light",
                        "color": "Green"
                    },
                    "text": "Go: Green light."
                },
                "op_code": 4
            }
        ]
        edges_list = [
            {
                "id": 2215627675872,
                "start": 2215627920336,
                "end": 2215628121520,
                "type": 0,
                "edge_type": 2
            },
            {
                "id": 2215628139584,
                "type": 1,
                "start": 2215628121568,
                "end": 2215627676208,
                "content": {
                    "title": "",
                    "min": {
                        "hours": "00",
                        "minutes": "00",
                        "seconds": "03"
                    },
                    "max": {
                        "hours": "00",
                        "minutes": "00",
                        "seconds": "06"
                    }
                },
                "edge_type": 2
            },
            {
                "id": 2215627677408,
                "start": 2215627676256,
                "end": 2215627920480,
                "type": 0,
                "edge_type": 2
            }
        ]
        for node in nodes_list:
            scene.nodes.append(conv_node(scene, node))
        for edge in edges_list:
            scene.edges.append(conv_edge(scene, edge))
    return scene


@pytest.fixture
def relative_edge_scene():
    with patch("workflow_graphics_scene.WFGraphicsScene"):
        scene = WorkflowScene()
        nodes_list = [
            {
                "id": 2215627408048,
                "title": "New Start Node",
                "pos_x": -350.0,
                "pos_y": -250.0,
                "inputs": [],
                "outputs": [
                    {
                        "id": 2215627920336,
                        "index": 0,
                        "multi_edges": True,
                        "position": 5,
                        "socket_type": 2
                    }
                ],
                "content": "",
                "op_code": 0
            },
            {
                "id": 2215627945056,
                "title": "New Finish Node",
                "pos_x": 200.0,
                "pos_y": 0.0,
                "inputs": [
                    {
                        "id": 2215627920480,
                        "index": 0,
                        "multi_edges": True,
                        "position": 2,
                        "socket_type": 2
                    }
                ],
                "outputs": [],
                "content": "",
                "op_code": 6
            },
            {
                "id": 2215628099936,
                "title": "Notification",
                "pos_x": -448.0,
                "pos_y": -30.0,
                "inputs": [
                    {
                        "id": 2215628121520,
                        "index": 0,
                        "multi_edges": True,
                        "position": 2,
                        "socket_type": 1
                    }
                ],
                "outputs": [
                    {
                        "id": 2215628121568,
                        "index": 0,
                        "multi_edges": True,
                        "position": 5,
                        "socket_type": 1
                    }
                ],
                "content": {
                    "node_details": {
                        "actors": [
                            "Participant"
                        ],
                        "title": "Red Light",
                        "color": "Red"
                    },
                    "text": "Stop : Red light."
                },
                "op_code": 4
            },
            {
                "id": 2215627676352,
                "title": "Notification",
                "pos_x": 40.0,
                "pos_y": -201.0,
                "inputs": [
                    {
                        "id": 2215627676208,
                        "index": 0,
                        "multi_edges": True,
                        "position": 2,
                        "socket_type": 1
                    }
                ],
                "outputs": [
                    {
                        "id": 2215627676256,
                        "index": 0,
                        "multi_edges": True,
                        "position": 5,
                        "socket_type": 1
                    }
                ],
                "content": {
                    "node_details": {
                        "actors": [
                            "Participant"
                        ],
                        "title": "Green Light",
                        "color": "Green"
                    },
                    "text": "Go: Green light."
                },
                "op_code": 4
            }
        ]
        edges_list = [
            {
                "id": 2215627675872,
                "start": 2215627920336,
                "end": 2215628121520,
                "type": 0,
                "edge_type": 2
            },
            {
                "id": 2215628139584,
                "type": 1,
                "start": 2215628121568,
                "end": 2215627676208,
                "content": {
                    "title": "",
                    "min": {
                        "hours": "00",
                        "minutes": "00",
                        "seconds": "03"
                    },
                    "max": {
                        "hours": "00",
                        "minutes": "00",
                        "seconds": "06"
                    }
                },
                "edge_type": 2
            },
            {
                "id": 2215627677408,
                "start": 2215627676256,
                "end": 2215627920480,
                "type": 0,
                "edge_type": 2
            }
        ]
        for node in nodes_list:
            scene.nodes.append(conv_node(scene, node))
        for edge in edges_list:
            scene.edges.append(conv_edge(scene, edge))
    return scene


def test_empty_scene_serialization(empty_scene):
    assert equals_flows(empty_scene.serialize(engine_save=True), engine_data_examples["scene"]["editor empty scene"])


def test_notification(notification_scene):
    assert equals_flows(notification_scene.serialize(engine_save=True),
                        engine_data_examples["scene"]["Welcome Notification"])


def test_decision_trait(decision_trait_scene):
    assert equals_flows(decision_trait_scene.serialize(engine_save=True),
                        engine_data_examples["scene"]["Trait - One Choice"])


def test_decision_questionnaire(decision_questionnaire_scene):
    assert equals_flows(decision_questionnaire_scene.serialize(engine_save=True),
                        engine_data_examples["scene"]["Questionnaire - Decision"])


def test_decision_test(decision_test_scene):
    assert equals_flows(decision_test_scene.serialize(engine_save=True),
                        engine_data_examples["scene"]["Test - Decision"])


def test_questionnaire(questionnaire_scene):
    assert equals_flows(questionnaire_scene.serialize(engine_save=True),
                        engine_data_examples["scene"]["Questionnaire"])


def test_test(test_scene):
    assert equals_flows(test_scene.serialize(engine_save=True),
                        engine_data_examples["scene"]["Test"])


def test_complex(subworkflow_scene):
    assert equals_flows(subworkflow_scene.serialize(engine_save=True),
                        engine_data_examples["scene"]["Sub Workflow"])


def test_covid(covid_scene):
    assert equals_flows(covid_scene.serialize(engine_save=True),
                        engine_data_examples["scene"]["Covid Example"])


def test_relative_edge(relative_edge_scene):
    assert equals_flows(relative_edge_scene.serialize(engine_save=True),
                        engine_data_examples["scene"]["relative edge"])
