import json
import os
import sqlite3

from Database.DALEdges import buildDALEdge
from Database.DALNodes import buildDALNodes
from Form import Form
from Test import Test
from Users import User


def set_name(name):
    # noinspection PyGlobalUndefined
    global db_name
    db_name = name


def delete_db():
    if os.path.exists(read_config()):
        os.remove(read_config())
    else:
        print("The file does not exist")


def create_connection():
    db_name = read_config()
    conn = None
    try:
        conn = sqlite3.connect(db_name)
        return conn
    except sqlite3.Error as e:
        print(e)

    return conn


def read_config():
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    f = open(ROOT_DIR+'\\config.json')
    data = json.load(f)
    return ROOT_DIR+'\\'+data['db_name']


def create_table(conn, query):
    try:
        c = conn.cursor()
        c.execute(query)
        conn.commit()
    except sqlite3.Error as e:
        print(e)


def change_table(query, data):
    conn = create_connection()
    cur = conn.cursor()
    try:
        cur.execute(query, data)
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(e)


def extract_one_from_table(query, data):
    conn = create_connection()
    cur = conn.cursor()
    try:
        cur.execute(query, data)
        result = cur.fetchone()
        conn.close()
        return result
    except sqlite3.Error as e:
        print(e)


def extract_many_from_table(query, data):
    conn = create_connection()
    cur = conn.cursor()
    try:
        cur.execute(query, data)
        result = cur.fetchall()
        conn.close()
        return result
    except sqlite3.Error as e:
        print(e)


def fetch_all(query):
    conn = create_connection()
    cur = conn.cursor()
    try:
        cur.execute(query)
        result = cur.fetchall()
        conn.close()
        return result
    except sqlite3.Error as e:
        print(e)


def init_tables():
    queries = {"create_actors_to_notify_table": """CREATE TABLE IF NOT EXISTS "Actors_To_Notify" (
            "notification_id"	INTEGER NOT NULL,
            "actor_name"	TEXT,
            PRIMARY KEY("notification_id","actor_name"),
            FOREIGN KEY("notification_id") REFERENCES "String_Nodes"("id")
            );""",
               "create_answer_options_table": """CREATE TABLE IF NOT EXISTS "Answer_Options" (
            "form_id"	INTEGER NOT NULL,
            "number"	INTEGER NOT NULL,
            "option_num"	INTEGER NOT NULL,
            "option"	TEXT NOT NULL,
            FOREIGN KEY("form_id") REFERENCES "Questions"("form_id"),
            PRIMARY KEY("form_id","number","option_num")
            );""",
               "create_answers_table": """CREATE TABLE IF NOT EXISTS "Answers" (
            "form_id"	INTEGER NOT NULL,
            "question_num"	INTEGER NOT NULL,
            "user_id"	INTEGER NOT NULL,
            "time_taken"	DATETIME NOT NULL,
            "answer"	TEXT NOT NULL,
            PRIMARY KEY("form_id","user_id","time_taken","question_num"),
            FOREIGN KEY("form_id") REFERENCES "Questionnaires"("form_id"),
            FOREIGN KEY("question_num") REFERENCES "Questions"("number"),
            FOREIGN KEY("user_id") REFERENCES "Participants"("id")
            );""",
               "create_complex_nodes_table": """CREATE TABLE IF NOT EXISTS "Complex_Nodes" (
            "id"	INTEGER NOT NULL UNIQUE,
            "first_id"	INTEGER NOT NULL,
            PRIMARY KEY("id"),
            FOREIGN KEY("first_id") REFERENCES "Nodes"("id")
            );""",
               "create_conditions_questionnaire_table": """CREATE TABLE IF NOT EXISTS "Conditions_Questionnaire" (
            "decision_id"	INTEGER NOT NULL,
            "title"	INTEGER NOT NULL,
            "form_id"	INTEGER NOT NULL,
            "question_num"	INTEGER NOT NULL,
            "answers"	TEXT NOT NULL,
            FOREIGN KEY("form_id") REFERENCES "Questionnaires"("form_id"),
            FOREIGN KEY("decision_id") REFERENCES "Nodes"("id"),
            FOREIGN KEY("question_num") REFERENCES "Questions"("number")
            PRIMARY KEY("title","decision_id")
            );""",
               "create_conditions_test_table": """CREATE TABLE IF NOT EXISTS "Conditions_Test" (
            "decision_id"	INTEGER NOT NULL,
            "title"	TEXT NOT NULL,
            "test"	TEXT NOT NULL,
            "type"	TEXT NOT NULL,
            "value"	TEXT,
            "min"   INTEGER,
            "max"   INTEGER,
            FOREIGN KEY("decision_id") REFERENCES "Nodes"("id"),
            FOREIGN KEY("test") REFERENCES "Tests"("title")
            PRIMARY KEY("decision_id","title")
            );""",
               "create_conditions_trait_table": """CREATE TABLE IF NOT EXISTS "Conditions_Trait" (
            "decision_id"	INTEGER NOT NULL,
            "title"	TEXT NOT NULL,
            "test"	TEXT NOT NULL,
            "type"	TEXT NOT NULL,
            "gender" TEXT,
            "min"	INTEGER,
            "max"	INTEGER,
            PRIMARY KEY("decision_id","title"),
            FOREIGN KEY("decision_id") REFERENCES "Nodes"("id"),
            FOREIGN KEY("test") REFERENCES "Tests"("title")
            );""",
               "create_current_position_table": """CREATE TABLE IF NOT EXISTS "Current_Position" (
            "participant_id"	INTEGER NOT NULL,
            "position_id"	    INTEGER,
            "type"	            TEXT,
            "start_time"	    DATETIME,
            "active"            TEXT,
            PRIMARY KEY("participant_id","position_id","type"),
            FOREIGN KEY("participant_id") REFERENCES "Participants"("id")
            );""",
               "create_edges_table": """CREATE TABLE IF NOT EXISTS "Edges" (
            "id"	INTEGER NOT NULL UNIQUE,
            "from_id"	INTEGER,
            "to_id"	INTEGER,
            "min_time"	INTEGER,
            "max_time"	INTEGER,
            "min_fixed"	DATETIME,
            "max_fixed"	DATETIME,
            FOREIGN KEY("to_id") REFERENCES "Nodes"("id"),
            FOREIGN KEY("from_id") REFERENCES "Nodes"("id"),
            PRIMARY KEY("id")
            );""",
               "create_nodes_table": """CREATE TABLE IF NOT EXISTS "Nodes" (
            "title"	TEXT NOT NULL,
            "type"	INTEGER NOT NULL,
            "id"	INTEGER,
            PRIMARY KEY("id")
            );""",
               "create_participants_table": """CREATE TABLE IF NOT EXISTS "Participants" (
            "id"	INTEGER NOT NULL,
            "name"	TEXT NOT NULL,
            "gender"	TEXT NOT NULL,
            "age"	INTEGER NOT NULL,
            "workflow"	INTEGER NOT NULL,
            PRIMARY KEY("id")
            );""",
               "create_questionnaires_table": """CREATE TABLE IF NOT EXISTS "Questionnaires" (
            "id"	INTEGER NOT NULL UNIQUE,
            "form_id"	INTEGER NOT NULL,
            PRIMARY KEY("id"),
            FOREIGN KEY("id") REFERENCES "Nodes"("id"),
            FOREIGN KEY("form_id") REFERENCES "Questions"("form_id")
            );""",
               "create_questions_table": """CREATE TABLE IF NOT EXISTS "Questions" (
            "form_id"	INTEGER NOT NULL,
            "number"	INTEGER NOT NULL,
            "question"	TEXT NOT NULL,
            "type"	TEXT NOT NULL,
            PRIMARY KEY("form_id","number"),
            FOREIGN KEY("form_id") REFERENCES "Questionnaires"("form_id")
            );""",
               "create_staff_table": """CREATE TABLE IF NOT EXISTS "Staff" (
            "id"    INTEGER NOT NULL,
            "name"	TEXT NOT NULL,
            "role"	TEXT NOT NULL,
            "gender" TEXT NOT NULL,
            "age" INTEGER NOT NULL,
            "available"  TEXT NOT NULL,
            PRIMARY KEY("id")
            );""",
               "create_string_nodes_table": """CREATE TABLE IF NOT EXISTS "String_Nodes" (
            "id"	INTEGER NOT NULL UNIQUE,
            "notification"	TEXT,
            PRIMARY KEY("id")
            );""",
               "create_test_nodes_table": """CREATE TABLE IF NOT EXISTS "Test_Nodes" (
            "id"	INTEGER NOT NULL UNIQUE,
            "title"	TEXT NOT NULL,
            "in_charge"	TEXT NOT NULL,
            FOREIGN KEY("id") REFERENCES "Nodes"("id"),
            PRIMARY KEY("id")
            );""",
               "create_test_results_table": """CREATE TABLE IF NOT EXISTS "Test_Results" (
            "test_name"	INTEGER NOT NULL,
            "user_id"	INTEGER NOT NULL,
            "time_taken"	DATETIME NOT NULL,
            "result"	TEXT NOT NULL,
            FOREIGN KEY("test_name") REFERENCES "Tests"("title"),
            FOREIGN KEY("user_id") REFERENCES "Participants"("id"),
            PRIMARY KEY("test_name","user_id","time_taken")
            );""",
               "create_tests_table": """CREATE TABLE IF NOT EXISTS "Tests" (
            "node_id"	INTEGER NOT NULL,
            "title"	TEXT NOT NULL,
            "instructions"	TEXT NOT NULL,
            "staff"	TEXT,
            "duration"	INTEGER,
            FOREIGN KEY("node_id") REFERENCES "Nodes"("id"),
            PRIMARY KEY("title","node_id")
            );""",
               "create_wait_list_table": """CREATE TABLE IF NOT EXISTS "Wait_List" (
            "node_id"	        INTEGER NOT NULL,
            "wait"	            INTEGER NOT NULL,
            "participant_id"    INTEGER NOT NULL,
            FOREIGN KEY("node_id") REFERENCES "Nodes"("id"),
            FOREIGN KEY("wait") REFERENCES "Edges"("id"),
            FOREIGN KEY("participant_id") REFERENCES "Participants"("id"),
            PRIMARY KEY("node_id", "wait", "participant_id")
            );""",
               "create_workflows_table": """CREATE TABLE IF NOT EXISTS "Workflows" (
            "id"	INTEGER NOT NULL,
            "first_node"	INTEGER NOT NULL,
            PRIMARY KEY("id")
            );"""}

    conn = create_connection()
    if conn is not None:
        for query in queries:
            create_table(conn, queries[query])
    else:
        print("Error! cannot create the database connection.")
    conn.close()


def addActorToNotify(notification_id, actor_name):
    query = """INSERT OR IGNORE INTO Actors_To_Notify (notification_id, actor_name)
                        VALUES 
                           (?, ?);"""
    answer_data = (notification_id, actor_name)
    change_table(query, answer_data)


def addAnswer(form_id, question_num, user_id, time_taken, answer):
    query = """INSERT OR IGNORE INTO Answers (form_id, question_num, user_id, time_taken, answer)
                    VALUES 
                       (?, ?, ?, ?, ?);"""
    answer_data = (form_id, question_num, user_id, time_taken, answer)
    change_table(query, answer_data)


def addComplexNode(node_id, first_id):
    query = """INSERT OR IGNORE INTO Complex_Nodes (id, first_id)
                        VALUES 
                           (?, ?);"""
    node_data = (node_id, first_id)
    change_table(query, node_data)


def addEdge(edge_id, from_id, to_id, min_time, max_time, min_fixed, max_fixed):
    query = """INSERT OR IGNORE INTO Edges (id, from_id, to_id, min_time, max_time, min_fixed, max_fixed)
                    VALUES 
                       (?, ?, ?, ?, ?, ?, ?);"""
    edge_data = (edge_id, from_id, to_id, min_time, max_time, min_fixed, max_fixed)
    change_table(query, edge_data)


def addEdgePosition(participant_id, edge_id, start_time):
    query = """INSERT OR IGNORE INTO Current_Position (participant_id, position_id, type, start_time, active)
                VALUES (?, ?, ?, ?, ?)"""
    ids = (participant_id, edge_id, "edge", start_time, "yes")
    change_table(query, ids)


def addForm(form):
    conn = create_connection()
    cur = conn.cursor()
    for question in form.questions:
        query = """INSERT OR IGNORE INTO Questions (form_id, number, question, type)
        VALUES 
           (?, ?, ?, ?);"""
        question_data = (form.questionnaire_number, question["number"], question["text"], question["type"])
        try:
            cur.execute(query, question_data)
        except sqlite3.Error:
            continue
        if question["type"] != 'open':
            i = 0
            for option in question["options"]:
                query = """INSERT INTO Answer_Options (form_id, number, option_num, option)
                        VALUES 
                           (?, ?, ?, ?);"""
                option_data = (form.questionnaire_number, question["number"], i, option)
                i = i + 1
                try:
                    cur.execute(query, option_data)
                except sqlite3.Error:
                    continue
        conn.commit()
    conn.close()


def addNode(node, op_code):
    query = """INSERT OR IGNORE INTO Nodes (title, type, id)
                    VALUES (?, ?, ?);"""
    node_data = (node.title, op_code, node.id)
    change_table(query, node_data)


def addNodePosition(participant_id, node_id, start_time):
    query = """INSERT OR IGNORE INTO Current_Position (participant_id, position_id, type, start_time, active)
                VALUES (?, ?, ?, ?, ?)"""
    ids = (participant_id, node_id, "node", start_time, "yes")
    change_table(query, ids)


def addParticipant(user_id, name, gender, age, workflow):
    query = """INSERT OR IGNORE INTO Participants (id, name, gender, age, workflow)
                VALUES 
                   (?, ?, ?, ?, ?);"""
    participant_data = (user_id, name, gender, age, workflow)
    change_table(query, participant_data)


def addQuestionnaire(node_id, form_id, node):
    query = """INSERT OR IGNORE INTO Questionnaires (id, form_id)
                VALUES 
                   (?, ?);"""
    node_data = (node_id, form_id)
    change_table(query, node_data)


def addQuestionnaireCond(decision_id, title, form_id, question_num, answers):
    query = """INSERT OR IGNORE INTO Conditions_Questionnaire (decision_id, title, form_id, question_num, answers)
                    VALUES 
                       (?, ?, ?, ?, ?);"""
    cond_data = (decision_id, title, form_id, question_num, answers)
    change_table(query, cond_data)


def addStaff(user_id, name, role, gender, age, available):
    query = """INSERT OR IGNORE INTO Staff (id, name, role, gender, age, available)
                VALUES 
                   (?, ?, ?, ?, ?, ?);"""
    staff_data = (user_id, name, role, gender, age, available)
    change_table(query, staff_data)


def addStringNode(notification_id, notification):
    query = """INSERT OR IGNORE INTO String_Nodes (id, notification)
                    VALUES 
                       (?, ?);"""
    node_data = (notification_id, notification)
    change_table(query, node_data)


def addTest(node_id, title, instructions, staff, duration):
    query = """INSERT OR IGNORE INTO Tests (node_id, title, instructions, staff, duration)
                    VALUES 
                       (?, ?, ?, ?, ?);"""
    test_data = (node_id, title, instructions, staff, duration)
    change_table(query, test_data)


def addTestCond(decision_id, title, test, sat_type, value, min_time, max_time):
    query = """INSERT OR IGNORE INTO Conditions_Test (decision_id, title, test, type, value, min, max)
                    VALUES 
                       (?, ?, ?, ?, ?, ?, ?);"""
    cond_data = (decision_id, title, test, sat_type, value, min_time, max_time)
    change_table(query, cond_data)


def addTestNode(node):
    query = """INSERT OR IGNORE INTO Test_Nodes (id, title, in_charge)
                VALUES (?, ?, ?);"""
    node_data = (node.id, node.title, node.in_charge)
    change_table(query, node_data)


def addTestResults(test_name, user_id, time_taken, result):
    change_table("""INSERT OR IGNORE INTO Test_Results (test_name, user_id, time_taken, result)
                 VALUES (?, ?, ?, ?)""", (test_name, user_id, time_taken, result))


def addTraitCond(decision_id, title, test, sat_type, gender, min_val, max_val):
    query = """INSERT OR IGNORE INTO Conditions_Trait (decision_id, title, test, type, gender, min, max)
                VALUES (?, ?, ?, ?, ?, ?, ?);"""
    cond_data = (decision_id, title, test, sat_type, gender, min_val, max_val)
    change_table(query, cond_data)


def addWaiter(node_id, wait, participant_id):
    change_table("""INSERT OR IGNORE INTO Wait_List (node_id, wait, participant_id)
                VALUES (?, ?, ?);""", (node_id, wait, participant_id))


def addWorkflow(workflow_id, first):
    query = """INSERT OR IGNORE INTO Workflows (id, first_node)
                VALUES (?, ?);"""
    data = (workflow_id, first)
    change_table(query, data)


def getAllActives(participant_id):
    return extract_many_from_table("""SELECT position_id FROM Current_Position 
                                        WHERE participant_id=? AND active ="yes" """, (participant_id,))


def getActorsToNofity():
    return fetch_all("""SELECT * FROM Actors_To_Notify""")


def getAnswer(form_id, question_number, participant_id):
    rows = extract_one_from_table("""SELECT answer FROM Answers WHERE form_id=? AND question_num=? AND user_id=? """,
                                  (form_id, question_number, participant_id))[0]
    q_type = extract_one_from_table("""SELECT type FROM Questions WHERE form_id=? AND number=?""",
                                    (form_id, question_number))[0]
    if q_type == "open":
        return rows
    rows = rows[1:-1].split(', ')
    rows = [int(i) for i in rows]
    return rows


def getAnswerOptions():
    return fetch_all("""SELECT * FROM Answer_Options""")


def getComplexNodes():
    return fetch_all("""SELECT * FROM Complex_Nodes""")


def getCurrentPositions(participant_id):
    positions = extract_many_from_table("SELECT position_id, type FROM Current_Position WHERE participant_id=?",
                                        (participant_id,))
    output = []
    for position in positions:
        if position[1] == "edge":
            output.append(("edge", getEdge(position[0])))
        else:
            output.append(("node", getNode(position[0])))
    return output


def getEdge(edge_id):
    edge = extract_one_from_table("SELECT * FROM Edges WHERE id=?", (edge_id,))
    return buildDALEdge(edge)


def getEdges(from_id):
    edges = []
    edges_data = extract_many_from_table("SELECT * FROM Edges WHERE from_id=?", (from_id,))
    for edge_data in edges_data:
        edges.append(buildDALEdge(edge_data))
    return edges


def getForm(form_id):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Questions WHERE form_id=?", (form_id,))
    rows = cur.fetchall()
    questions = []
    # row format: [form_id, number, question, type]
    for row in rows:
        if row[3] != "open":
            cur.execute("SELECT * FROM Answer_Options WHERE form_id=? AND number=?", (form_id, row[1]))
            option_rows = cur.fetchall()
            options = []
            # option format: [form_id, number, option_num, option]
            for option in option_rows:
                options.append(option[3])
            questions.append({"number": row[1],
                              "text": row[2],
                              "type": row[3],
                              "options": options})
        questions.append({"number": row[1],
                          "text": row[2],
                          "type": "open"})
    conn.close()
    form = Form(form_id, questions)

    return form


def getNode(node_id):
    node_data = extract_one_from_table("SELECT * FROM Nodes WHERE id=?", (node_id,))
    if len(node_data) == 0:
        return None
    op_code = node_data[1]
    title = node_data[0]
    if op_code == 0:
        return buildDALNodes([op_code, node_id, "New Start Node"])
    elif op_code == 1:
        form_id = extract_one_from_table("""SELECT form_id FROM Questionnaires WHERE id=?""", (node_id,))[0]
        form = getForm(form_id)
        return buildDALNodes([op_code, node_id, title, form, form_id])
    elif op_code == 2:
        in_charge = extract_one_from_table("""SELECT in_charge FROM Test_Nodes WHERE id=?""", (node_id,))[0]
        tests = getTests(node_id)
        return buildDALNodes([op_code, node_id, title, tests, in_charge])
    elif op_code == 3:
        quest_conditions = extract_many_from_table("""SELECT * FROM Conditions_Questionnaire WHERE decision_id=?""",
                                                   (node_id,))
        test_conditions = extract_many_from_table("""SELECT * FROM Conditions_Test WHERE decision_id=?""", (node_id,))
        trait_conditions = extract_many_from_table("""SELECT * FROM Conditions_Trait WHERE decision_id=?""", (node_id,))
        return buildDALNodes([op_code, node_id, title, quest_conditions, test_conditions, trait_conditions])
    elif op_code == 4:
        text = extract_one_from_table("""SELECT notification FROM String_Nodes WHERE id=?""", (node_id,))[0]
        actors = []
        actors_mashed = extract_many_from_table("""SELECT actor_name FROM Actors_To_Notify WHERE notification_id=?""",
                                                (node_id,))
        for actor in actors_mashed:
            actors.append(actor[0])
        return buildDALNodes([op_code, node_id, title, text, actors])
    elif op_code == 5:
        first_id = extract_one_from_table("""SELECT first_id FROM Complex_Nodes WHERE id=?""", (node_id,))[0]
        flow_node = getNode(first_id)
        return buildDALNodes([op_code, node_id, title, flow_node])
    elif op_code == 6:
        return buildDALNodes([op_code, node_id, "New Finish Node"])


def getQuestionnaires():
    return fetch_all("""SELECT * FROM Questionnaires""")


def getQuestions():
    return fetch_all("""SELECT * FROM Questions""")


def getStaff(role):
    user_data = extract_one_from_table("""SELECT * FROM Staff WHERE role=? AND available="yes" """, (role.lower(),))
    if len(user_data) == 0:
        return None
    # change_table("""UPDATE Staff SET available = "no" WHERE id=?""", (user_data[0],))
    return User(user_data[2], user_data[3], user_data[4], user_data[0])


def getStringNodes():
    return fetch_all("""SELECT * FROM String_Nodes""")


def getTestResult(user_id, test_name):
    result_data = extract_one_from_table("""SELECT result FROM Test_Results WHERE user_id=? AND test_name=? 
                                            ORDER BY time_taken DESC""", (user_id, test_name))
    return result_data[0]


def getTests(node_id):
    tests = []
    tests_data = extract_many_from_table("""SELECT * FROM Tests WHERE node_id=?""", (node_id,))
    for test in tests_data:
        actors = test[3].split(', ')
        tests.append(Test(test[1], test[4], test[2], actors))
    return tests


def getTimeStarted(participant_id, edge_id):
    return extract_one_from_table("""SELECT start_time FROM Current_Position 
                                  WHERE participant_id=? AND position_id=? AND type = "edge" """,
                                  (participant_id, edge_id))[0]


def getToNode(edge_id):
    return getNode(extract_one_from_table("SELECT to_id FROM Edges WHERE id=?", (edge_id,))[0])


def getUser(user_id):
    user_data = extract_one_from_table("SELECT * FROM Participants WHERE id=?", (user_id,))
    return User('participant', user_data[2], user_data[3], user_id)


def getWaitList(node_id, participant_id):
    visited = extract_many_from_table("""SELECT wait FROM Wait_List WHERE node_id=? AND participant_id=?""",
                                      (node_id, participant_id))
    wait_list = extract_many_from_table("""SELECT id FROM Edges WHERE to_id=?""", (node_id,))
    return set(wait_list) - set(visited)


def getWorkflow(workflow_id):
    query = """SELECT * FROM Workflows WHERE id=?"""
    workflow = extract_one_from_table(query, (workflow_id,))
    return workflow


def getWorkflowsIds():
    ids = fetch_all("""SELECT id FROM Workflows""")
    ids = list(map(unpack, ids))
    return ids


def releasePosition(participant_id, position_id, position_type):
    change_table("""UPDATE current_position SET active = "no" WHERE participant_id=? AND position_id=? AND type=?""",
                 (participant_id, position_id, position_type))


def releaseStaff(user_id):
    change_table("""UPDATE Staff SET available = "yes" WHERE id=?""", (user_id,))


def releaseWaiter(node_id, participant_id):
    change_table("""DELETE FROM Wait_List WHERE node_id=? AND participant_id=?""", (node_id, participant_id))


def unpack(tup):
    (x,) = tup
    return x
