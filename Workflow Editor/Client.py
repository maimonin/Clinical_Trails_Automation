import socket
import networkx as nx
import json
from networkx.readwrite import json_graph


def Main():
    host = '127.0.0.1'
    port = 8000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    nodes = [{'type': 'data entering', 'id': 1, 'title': 'questionnaire',
                     'role': 'participant', 'form': {'1': ['how are you?', 'good', 'bad']}, 'next': 'decision'},
             {'type': 'decision', 'id': 2, 'title': 'decision', 'actors': ['participant', 'nurse'],
              'form': {'blood type': ['A', 'B']}, 'next options': [3, 4], 'condition': lambda x: 3 if x == 'A' else 4},
             {'type': 'string', 'actors': ['investigator'], 'text': 'A'},
             {'type': 'string', 'actors': ['investigator'], 'text': 'B'}
             ]
    labels = {12: {'type': 'time', 'max': '0:10', 'min': '0:02'},
              23: {'type': 'decision', 'decision': 'A'},
              24: {'type': 'decision', 'decision': 'B'}}
    # workflow = nx.DiGraph()
    # workflow.add_edge(questionnaire, decision, label=labels[12])
    # workflow.add_edge(decision, a, label=labels[23])
    # workflow.add_edge(decision, b, label=labels[24])
   # graph_json = json_graph.
   #  print(graph_json)
   #  graph_json["sender"] = 'editor'
   #  print(graph_json)

    while True:
        for node in nodes:
            s.send(json.dumps(node).encode('ascii'))

        # data = int(s.recv(1024))

        # ask the client whether he wants to continue
        ans = input('\nDo you want to continue(y/n) :')
        if ans == 'y':
            continue
        else:
            break

    s.close()


if __name__ == '__main__':
    Main()
