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
    },
    "scene": {
        "New Scene": {
            "id": 2008280264512,
            "nodes": [
                {
                    "id": 2008280241056,
                    "title": "New Start Node",
                    "inputs": [],
                    "outputs": [
                        {
                            "id": 2008280089792
                        }
                    ],
                    "op_code": 0
                },
                {
                    "id": 2008280159568,
                    "title": "New Finish Node",
                    "inputs": [
                        {
                            "id": 2008280089936
                        }
                    ],
                    "outputs": [],
                    "op_code": 6
                }
            ],
            "edges": []
        },
        "Welcome Notification": {
            "id": 2008280264512,
            "nodes": [
                {
                    "id": 2008280241056,
                    "title": "New Start Node",
                    "inputs": [],
                    "outputs": [
                        {
                            "id": 2008280089792
                        }
                    ],
                    "op_code": 0
                },
                {
                    "id": 2008280159568,
                    "title": "New Finish Node",
                    "inputs": [
                        {
                            "id": 2008280089936
                        }
                    ],
                    "outputs": [],
                    "op_code": 6
                }
            ],
            "edges": []
        },
        "Trait - One Choice": {
            "id": 1722785005728,
            "nodes": [
                {
                    "id": 1722785223056,
                    "title": "New Start Node",
                    "inputs": [],
                    "outputs": [
                        {
                            "id": 1722785243536
                        }
                    ],
                    "op_code": 0
                },
                {
                    "id": 1722785243488,
                    "title": "New Finish Node",
                    "inputs": [
                        {
                            "id": 1722785243680
                        }
                    ],
                    "outputs": [],
                    "op_code": 6
                },
                {
                    "id": 1722785243632,
                    "title": "Decision",
                    "inputs": [
                        {
                            "id": 1722785244544
                        }
                    ],
                    "outputs": [
                        {
                            "id": 1722785243248
                        },
                        {
                            "id": 1722785244592
                        }
                    ],
                    "content": {
                        "node_details": {
                            "title": "Gender split"
                        },
                        "condition": [
                            {
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
                    "inputs": [
                        {
                            "id": 1722751452112
                        }
                    ],
                    "outputs": [
                        {
                            "id": 1722751452160
                        }
                    ],
                    "content": {
                        "node_details": {
                            "actors": [
                                "Participant"
                            ],
                            "title": "Male Participant"
                        },
                        "text": "Continue trial"
                    },
                    "op_code": 4
                },
                {
                    "id": 1722785244928,
                    "title": "Notification",
                    "inputs": [
                        {
                            "id": 1722751452688
                        }
                    ],
                    "outputs": [
                        {
                            "id": 1722751452064
                        }
                    ],
                    "content": {
                        "node_details": {
                            "actors": [
                                "Participant"
                            ],
                            "title": "Female Participant"
                        },
                        "text": "This trial is for men."
                    },
                    "op_code": 4
                }
            ],
            "edges": [
                {
                    "id": 1722751452640,
                    "start": 1722785244592,
                    "end": 1722751452112,
                    "type": 0
                },
                {
                    "id": 1722751452304,
                    "start": 1722785243248,
                    "end": 1722751452688,
                    "type": 0
                },
                {
                    "id": 1722751453408,
                    "start": 1722751452064,
                    "end": 1722785243680,
                    "type": 0
                },
                {
                    "id": 1722785244112,
                    "start": 1722751452160,
                    "end": 1722785243680,
                    "type": 0
                },
                {
                    "id": 1722785244304,
                    "start": 1722785244544,
                    "end": 1722785243536,
                    "type": 0
                }
            ]
        },
        "Trait - Range": {
            "id": 1722751596480,
            "nodes": [
                {
                    "id": 1722751597872,
                    "title": "New Start Node",
                    "inputs": [],
                    "outputs": [
                        {
                            "id": 1722751598256
                        }
                    ],
                    "op_code": 0
                },
                {
                    "id": 1722751598208,
                    "title": "New Finish Node",
                    "inputs": [
                        {
                            "id": 1722751598400
                        }
                    ],
                    "outputs": [],
                    "op_code": 6
                },
                {
                    "id": 1722751454944,
                    "title": "Decision",
                    "inputs": [
                        {
                            "id": 1722776604240
                        }
                    ],
                    "outputs": [
                        {
                            "id": 1722751454896
                        },
                        {
                            "id": 1722785005680
                        }
                    ],
                    "content": {
                        "node_details": {
                            "title": "Age Split"
                        },
                        "condition": [
                            {
                                "title": "condition 1",
                                "type": "trait condition",
                                "satisfy": {
                                    "type": "range",
                                    "value": {
                                        "min": 21,
                                        "max": 30
                                    }
                                },
                                "trait": "Age"
                            }
                        ]
                    },
                    "op_code": 3
                },
                {
                    "id": 1722785243968,
                    "title": "Notification",
                    "inputs": [
                        {
                            "id": 1722751597104
                        }
                    ],
                    "outputs": [
                        {
                            "id": 1722751596576
                        }
                    ],
                    "content": {
                        "node_details": {
                            "actors": [
                                "Nurse"
                            ],
                            "title": "Young Adults"
                        },
                        "text": "Young Adult has found"
                    },
                    "op_code": 4
                },
                {
                    "id": 1722751596672,
                    "title": "Notification",
                    "inputs": [
                        {
                            "id": 1722751597344
                        }
                    ],
                    "outputs": [
                        {
                            "id": 1722751596912
                        }
                    ],
                    "content": {
                        "node_details": {
                            "actors": [
                                "Participant"
                            ],
                            "title": "Kids and adults"
                        },
                        "text": "Stop trial."
                    },
                    "op_code": 4
                }
            ],
            "edges": [
                {
                    "id": 1722785244064,
                    "start": 1722751598256,
                    "end": 1722776604240,
                    "type": 0
                },
                {
                    "id": 1722751597488,
                    "start": 1722785005680,
                    "end": 1722751597104,
                    "type": 0
                },
                {
                    "id": 1722751595808,
                    "start": 1722751596576,
                    "end": 1722751598400,
                    "type": 0
                },
                {
                    "id": 1722751596336,
                    "start": 1722751454896,
                    "end": 1722751597344,
                    "type": 0
                },
                {
                    "id": 1722751595856,
                    "start": 1722751596912,
                    "end": 1722751598400,
                    "type": 0
                }
            ]
        },
        "Questionnaire - Decision": {
            "id": 1722752045312,
            "nodes": [
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
            ],
            "edges": [
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
        },
        "Test - Decision": {
            "id": 1722752046128,
            "nodes": [
                {
                    "id": 1722752046224,
                    "title": "New Start Node",
                    "inputs": [],
                    "outputs": [
                        {
                            "id": 1722752046032
                        }
                    ],
                    "op_code": 0
                },
                {
                    "id": 1722752045456,
                    "title": "New Finish Node",
                    "inputs": [
                        {
                            "id": 1722752132240
                        }
                    ],
                    "outputs": [],
                    "op_code": 6
                },
                {
                    "id": 1722752135072,
                    "title": "Test",
                    "inputs": [
                        {
                            "id": 1722752824464
                        }
                    ],
                    "outputs": [
                        {
                            "id": 1722752824512
                        }
                    ],
                    "content": {
                        "node_details": {
                            "title": "Blood Test",
                            "actor in charge": "Lab Technician"
                        },
                        "tests": [
                            {
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
                    "inputs": [
                        {
                            "id": 1722752826432
                        }
                    ],
                    "outputs": [
                        {
                            "id": 1722752826384
                        },
                        {
                            "id": 1722752826480
                        }
                    ],
                    "content": {
                        "node_details": {
                            "title": "Iron People"
                        },
                        "condition": [
                            {
                                "title": "test condition 1",
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
                    "inputs": [
                        {
                            "id": 1722752825856
                        }
                    ],
                    "outputs": [
                        {
                            "id": 1722752826000
                        }
                    ],
                    "content": {
                        "node_details": {
                            "actors": [
                                "Participant"
                            ],
                            "title": "Normal People"
                        },
                        "text": "Youre not interesting."
                    },
                    "op_code": 4
                },
                {
                    "id": 1722752825952,
                    "title": "Notification",
                    "inputs": [
                        {
                            "id": 1722752826624
                        }
                    ],
                    "outputs": [
                        {
                            "id": 1722752826720
                        }
                    ],
                    "content": {
                        "node_details": {
                            "actors": [
                                "Lab Technician",
                                "Doctor"
                            ],
                            "title": "Aliens"
                        },
                        "text": "Alien was found."
                    },
                    "op_code": 4
                }
            ],
            "edges": [
                {
                    "id": 1722752825184,
                    "start": 1722752046032,
                    "end": 1722752824464,
                    "type": 0
                },
                {
                    "id": 1722752826192,
                    "start": 1722752824512,
                    "end": 1722752826432,
                    "type": 0
                },
                {
                    "id": 1722752825760,
                    "start": 1722752826384,
                    "end": 1722752825856,
                    "type": 0
                },
                {
                    "id": 1722752825040,
                    "start": 1722752826000,
                    "end": 1722752132240,
                    "type": 0
                },
                {
                    "id": 1722752825808,
                    "start": 1722752826480,
                    "end": 1722752826624,
                    "type": 0
                },
                {
                    "id": 1722752825328,
                    "start": 1722752826720,
                    "end": 1722752132240,
                    "type": 0
                }
            ]
        },
        "Questionnaire": {
            "id": 1722753093696,
            "nodes": [
                {
                    "id": 1722753095376,
                    "title": "New Start Node",
                    "inputs": [],
                    "outputs": [
                        {
                            "id": 1722753095760
                        }
                    ],
                    "op_code": 0
                },
                {
                    "id": 1722753095712,
                    "title": "New Finish Node",
                    "inputs": [
                        {
                            "id": 1722753095904
                        }
                    ],
                    "outputs": [],
                    "op_code": 6
                },
                {
                    "id": 1722753095856,
                    "title": "Questionnaire",
                    "inputs": [
                        {
                            "id": 1722753096240
                        }
                    ],
                    "outputs": [
                        {
                            "id": 1722753096288
                        }
                    ],
                    "content": {
                        "node_details": {
                            "title": "Philosophic question"
                        },
                        "questions": [
                            {
                                "type": "open",
                                "text": "To be or not to be?"
                            }
                        ],
                        "questionnaire_number": 1
                    },
                    "op_code": 1
                }
            ],
            "edges": [
                {
                    "id": 1722753097008,
                    "start": 1722753095760,
                    "end": 1722753096240,
                    "type": 0
                },
                {
                    "id": 1722753096720,
                    "start": 1722753096288,
                    "end": 1722753095904,
                    "type": 0
                }
            ]
        },
        "Test": {
            "id": 1722753097248,
            "nodes": [
                {
                    "id": 1722753097200,
                    "title": "New Start Node",
                    "inputs": [],
                    "outputs": [
                        {
                            "id": 1722753097680
                        }
                    ],
                    "op_code": 0
                },
                {
                    "id": 1722753097152,
                    "title": "New Finish Node",
                    "inputs": [
                        {
                            "id": 1722753096624
                        }
                    ],
                    "outputs": [],
                    "op_code": 6
                },
                {
                    "id": 1722753096576,
                    "title": "Test",
                    "inputs": [
                        {
                            "id": 1722753094176
                        }
                    ],
                    "outputs": [
                        {
                            "id": 1722753094224
                        }
                    ],
                    "content": {
                        "node_details": {
                            "title": "Migrene Test",
                            "actor in charge": "Nurse"
                        },
                        "tests": [
                            {
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
            ],
            "edges": [
                {
                    "id": 1722752826288,
                    "start": 1722753097680,
                    "end": 1722753094176,
                    "type": 0
                },
                {
                    "id": 1722752826912,
                    "start": 1722753094224,
                    "end": 1722753096624,
                    "type": 0
                }
            ]
        },
        "Sub Workflow": {
            "id": 1722753094848,
            "nodes": [
                {
                    "id": 1722753292416,
                    "title": "New Start Node",
                    "inputs": [],
                    "outputs": [
                        {
                            "id": 1722753292896
                        }
                    ],
                    "op_code": 0
                },
                {
                    "id": 1722753292848,
                    "title": "New Finish Node",
                    "inputs": [
                        {
                            "id": 1722753293040
                        }
                    ],
                    "outputs": [],
                    "op_code": 6
                },
                {
                    "id": 1722753292992,
                    "title": "Sub Workflow",
                    "inputs": [
                        {
                            "id": 1722753293376
                        }
                    ],
                    "outputs": [
                        {
                            "id": 1722753293424
                        }
                    ],
                    "content": {
                        "flow": {
                            "id": 1722753094560,
                            "nodes": [
                                {
                                    "id": 1722753094128,
                                    "title": "New Start Node",
                                    "inputs": [],
                                    "outputs": [
                                        {
                                            "id": 1722753094800
                                        }
                                    ],
                                    "op_code": 0
                                },
                                {
                                    "id": 1722753093888,
                                    "title": "New Finish Node",
                                    "inputs": [
                                        {
                                            "id": 1722752824992
                                        }
                                    ],
                                    "outputs": [],
                                    "op_code": 6
                                },
                                {
                                    "id": 1722752826528,
                                    "title": "Notification",
                                    "inputs": [
                                        {
                                            "id": 1722752825904
                                        }
                                    ],
                                    "outputs": [
                                        {
                                            "id": 1722752825376
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
                                            "title": "Greetings"
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
                                    "type": 0
                                },
                                {
                                    "id": 1722752826048,
                                    "start": 1722752825376,
                                    "end": 1722752824992,
                                    "type": 0
                                }
                            ]
                        },
                        "type": "complex"
                    },
                    "op_code": 5
                }
            ],
            "edges": [
                {
                    "id": 1722753292176,
                    "start": 1722753292896,
                    "end": 1722753293376,
                    "type": 0
                },
                {
                    "id": 1722753290496,
                    "start": 1722753293424,
                    "end": 1722753293040,
                    "type": 0
                }
            ]
        },
        "Covid Example": {
    "id": 1327000129056,
    "nodes": [
        {
            "id": 1327000097408,
            "title": "New Start Node",
            "inputs": [],
            "outputs": [
                {
                    "id": 1327000566896
                }
            ],
            "op_code": 0
        },
        {
            "id": 1327000477408,
            "title": "Questionnaire",
            "inputs": [
                {
                    "id": 1327000455824
                }
            ],
            "outputs": [
                {
                    "id": 1327000455776
                }
            ],
            "content": {
                "node_details": {
                    "title": "informed consent"
                },
                "questions": [
                    {
                        "type": "one choice",
                        "text": "If you join, you will have injections, blood draws, saliva samples, and nasal swabs of your nose.",
                        "options": [
                            "Agree",
                            "No"
                        ]
                    },
                    {
                        "type": "one choice",
                        "text": "-The most common risks are symptoms are fever, muscle aches and headaches after getting the study vaccine. \\n-There are other, less serious risks. We will tell you more about them later in this consent form. ",
                        "options": [
                            "Agree",
                            "No"
                        ]
                    },
                    {
                        "type": "open",
                        "text": "Full Name"
                    }
                ],
                "questionnaire_number": 1
            },
            "op_code": 1
        },
        {
            "id": 1327000428112,
            "title": "Decision",
            "inputs": [
                {
                    "id": 1327000637056
                }
            ],
            "outputs": [
                {
                    "id": 1327000428064
                },
                {
                    "id": 2322150955904
                }
            ],
            "content": {
                "node_details": {
                    "title": "informed consent desc"
                },
                "condition": [
                    {
                        "title": "questionnaire condition 1",
                        "type": "questionnaire condition",
                        "questionnaireNumber": 1,
                        "questionNumber": 1,
                        "acceptedAnswers": [
                            0
                        ]
                    },
                    {
                        "title": "questionnaire condition 2",
                        "type": "questionnaire condition",
                        "questionnaireNumber": 1,
                        "questionNumber": 2,
                        "acceptedAnswers": [
                            0
                        ]
                    }
                ]
            },
            "op_code": 3
        },
        {
            "id": 1327000637152,
            "title": "Notification",
            "inputs": [
                {
                    "id": 1327000741344
                }
            ],
            "outputs": [
                {
                    "id": 1327000741056
                }
            ],
            "content": {
                "node_details": {
                    "actors": [
                        "Participant"
                    ],
                    "title": "end trail"
                },
                "text": "You can't participate in this trail"
            },
            "op_code": 4
        },
        {
            "id": 1327000663424,
            "title": "Sub Workflow",
            "inputs": [
                {
                    "id": 1327000662080
                }
            ],
            "outputs": [
                {
                    "id": 1327000740384
                }
            ],
            "content": {
                "flow": {
                    "id": 1327000740432,
                    "nodes": [
                        {
                            "id": 1326978122944,
                            "title": "New Start Node",
                            "inputs": [],
                            "outputs": [
                                {
                                    "id": 1326978123328
                                }
                            ],
                            "op_code": 0
                        },
                        {
                            "id": 1326978123520,
                            "title": "Test",
                            "inputs": [
                                {
                                    "id": 1326978123808
                                }
                            ],
                            "outputs": [
                                {
                                    "id": 1326978123856
                                }
                            ],
                            "content": {
                                "node_details": {
                                    "title": "antigen test",
                                    "actor in charge": "Nurse"
                                },
                                "tests": [
                                    {
                                        "name": "Antigen Test",
                                        "instructions": "Take samples from both nostrils using a swab.\\nPut the swab in tube and squeeze. Close the tube and drop the liquid on the test cassette. \\nWait 15 minutes for the results.",
                                        "staff": [
                                            "Nurse"
                                        ],
                                        "duration": "3"
                                    }
                                ]
                            },
                            "op_code": 2
                        },
                        {
                            "id": 1327000636576,
                            "title": "Decision",
                            "inputs": [
                                {
                                    "id": 1327000636384
                                }
                            ],
                            "outputs": [
                                {
                                    "id": 1327000636768
                                },
                                {
                                    "id": 2322150612560
                                }
                            ],
                            "content": {
                                "node_details": {
                                    "title": "test antigen desc"
                                },
                                "condition": [
                                    {
                                        "title": "test condition 1",
                                        "type": "test condition",
                                        "satisfy": {
                                            "type": "one_choice",
                                            "value": "negative"
                                        },
                                        "test": "Antigen Test"
                                    }
                                ]
                            },
                            "op_code": 3
                        },
                        {
                            "id": 1326978124672,
                            "title": "Test",
                            "inputs": [
                                {
                                    "id": 1326978124096
                                }
                            ],
                            "outputs": [
                                {
                                    "id": 1326978124768
                                }
                            ],
                            "content": {
                                "node_details": {
                                    "title": "vaccine",
                                    "actor in charge": "Lab Technician"
                                },
                                "tests": [
                                    {
                                        "name": "Vaccine",
                                        "instructions": "inject 5 ml to arm",
                                        "staff": [
                                            "Nurse"
                                        ],
                                        "duration": "2"
                                    }
                                ]
                            },
                            "op_code": 2
                        },
                        {
                            "id": 1326978216576,
                            "title": "Notification",
                            "inputs": [
                                {
                                    "id": 1326978216336
                                }
                            ],
                            "outputs": [
                                {
                                    "id": 1326978216624
                                }
                            ],
                            "content": {
                                "node_details": {
                                    "actors": [
                                        "Investigator",
                                        "Nurse"
                                    ],
                                    "title": "positive for covid"
                                },
                                "text": "Participant is positive for covid"
                            },
                            "op_code": 4
                        },
                        {
                            "id": 1326978125680,
                            "title": "Questionnaire",
                            "inputs": [
                                {
                                    "id": 1326978125488
                                }
                            ],
                            "outputs": [
                                {
                                    "id": 1326978124192
                                }
                            ],
                            "content": {
                                "node_details": {
                                    "title": "question after vaccine"
                                },
                                "questions": [
                                    {
                                        "type": "multi",
                                        "text": "Choose your symptoms",
                                        "options": [
                                            "Fever",
                                            "cough and shortness of breath",
                                            "muscle pain",
                                            "sore throat"
                                        ]
                                    },
                                    {
                                        "type": "open",
                                        "text": "Any side effect not mentioned you experienced?"
                                    }
                                ],
                                "questionnaire_number": 1
                            },
                            "op_code": 1
                        },
						{
                            "id": 1326978123280,
                            "title": "New Finish Node",
                            "inputs": [
                                {
                                    "id": 1326978123472
                                }
                            ],
                            "outputs": [],
                            "op_code": 6
                        }
                    ],
                    "edges": [
                        {
                            "id": 1326978124480,
                            "start": 1326978123328,
                            "end": 1326978123808,
                            "type": 0
                        },
                        {
                            "id": 1326978125632,
                            "start": 1326978123856,
                            "end": 1327000636384,
                            "type": 0
                        },
                        {
                            "id": 1326978125728,
                            "start": 1327000636768,
                            "end": 1326978216336,
                            "type": 0
                        },
                        {
                            "id": 1326978123424,
                            "start": 1326978216624,
                            "end": 1326978123472,
                            "type": 0
                        },
                        {
                            "id": 1326978217056,
                            "type": 1,
                            "start": 1327000636768,
                            "end": 1326978124096,
                            "content": {
                                "min": {
                                    "hours": 0,
                                    "minutes": 0,
                                    "seconds": 2
                                },
                                "max": {
                                    "hours": 0,
                                    "minutes": 0,
                                    "seconds": 3
                                }
                            }
                        },
                        {
                            "id": 1326978216528,
                            "type": 1,
                            "start": 1326978124768,
                            "end": 1326978125488,
                            "content": {
                                "min": {
                                    "hours": 0,
                                    "minutes": 0,
                                    "seconds": 5
                                },
                                "max": {
                                    "hours": 0,
                                    "minutes": 0,
                                    "seconds": 10
                                }
                            }
                        },
                        {
                            "id": 1326978216720,
                            "start": 1326978124192,
                            "end": 1326978123472,
                            "type": 0
                        }
                    ]
                },
                "type": "complex"
            },
            "op_code": 5
        },
		        {
            "id": 1327000331312,
            "title": "New Finish Node",
            "inputs": [
                {
                    "id": 1327000566752
                }
            ],
            "outputs": [],
            "op_code": 6
        }
    ],
    "edges": [
        {
            "id": 1327000323456,
            "start": 1327000566896,
            "end": 1327000455824,
            "type": 0
        },
        {
            "id": 1327000637248,
            "start": 1327000455776,
            "end": 1327000637056,
            "type": 0
        },
        {
            "id": 1327000663328,
            "start": 1327000428064,
            "end": 1327000741344,
            "type": 0
        },
        {
            "id": 1327000636672,
            "start": 1327000741056,
            "end": 1327000566752,
            "type": 0
        },
        {
            "id": 1326978124528,
            "type": 1,
            "start": 1327000428064,
            "end": 1327000662080,
            "content": {
                "min": {
                    "hours": 0,
                    "minutes": 0,
                    "seconds": 5
                },
                "max": {
                    "hours": 0,
                    "minutes": 0,
                    "seconds": 6
                }
            }
        },
        {
            "id": 1326978218688,
            "start": 1327000740384,
            "end": 1327000566752,
            "type": 0
        }
    ]
},
        "relative edge": {
    "id": 2215627456080,
    "nodes": [
        {
            "id": 2215627408048,
            "title": "New Start Node",
            "inputs": [],
            "outputs": [
                {
                    "id": 2215627920336
                }
            ],
            "op_code": 0
        },
        {
            "id": 2215627945056,
            "title": "New Finish Node",
            "inputs": [
                {
                    "id": 2215627920480
                }
            ],
            "outputs": [],
            "op_code": 6
        },
        {
            "id": 2215628099936,
            "title": "Notification",
            "inputs": [
                {
                    "id": 2215628121520
                }
            ],
            "outputs": [
                {
                    "id": 2215628121568
                }
            ],
            "content": {
                "node_details": {
                    "actors": [
                        "Participant"
                    ],
                    "title": "Red Light"
                },
                "text": "Stop : Red light."
            },
            "op_code": 4
        },
        {
            "id": 2215627676352,
            "title": "Notification",
            "inputs": [
                {
                    "id": 2215627676208
                }
            ],
            "outputs": [
                {
                    "id": 2215627676256
                }
            ],
            "content": {
                "node_details": {
                    "actors": [
                        "Participant"
                    ],
                    "title": "Green Light"
                },
                "text": "Go: Green light."
            },
            "op_code": 4
        }
    ],
    "edges": [
        {
            "id": 2215627675872,
            "start": 2215627920336,
            "end": 2215628121520,
            "type": 0
        },
        {
            "id": 2215628139584,
            "type": 1,
            "start": 2215628121568,
            "end": 2215627676208,
            "content": {
                "min": {
                    "hours": 0,
                    "minutes": 0,
                    "seconds": 3
                },
                "max": {
                    "hours": 0,
                    "minutes": 0,
                    "seconds": 6
                }
            }
        },
        {
            "id": 2215627677408,
            "start": 2215627676256,
            "end": 2215627920480,
            "type": 0
        }
    ]
}
    }
}
node_classes = [WorkflowNode_Decision, WorkflowNode_ComplexNode, WorkflowNode_SimpleString, WorkflowNode_DataEntry,
                WorkflowNode_Questionnaire]
