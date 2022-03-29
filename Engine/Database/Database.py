import sqlite3
from Database.DALNodes import buildDALNodes, buildDALNodesFromNode
from Form import Form

workflows = {}
questionnaires = {}
forms = {}


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('Database/data.db')
        return conn
    except sqlite3.Error as e:
        print(e)

    return conn


def create_table(conn, query):
    try:
        c = conn.cursor()
        c.execute(query)
        conn.commit()
    except sqlite3.Error as e:
        print(e)


def insert_to_table(query, data):
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
            "flow"	INTEGER NOT NULL,
            PRIMARY KEY("id"),
            FOREIGN KEY("flow") REFERENCES "Workflows"("id")
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
            FOREIGN KEY("decision_id") REFERENCES "Nodes"("id"),
            FOREIGN KEY("test") REFERENCES "Tests"("title")
            PRIMARY KEY("decision_id","title")
            );""",
               "create_conditions_trait_table": """CREATE TABLE IF NOT EXISTS "Conditions_Trait" (
            "decision_id"	INTEGER NOT NULL,
            "title"	TEXT NOT NULL,
            "test"	TEXT NOT NULL,
            "type"	TEXT NOT NULL,
            "min"	INTEGER,
            "max"	INTEGER,
            PRIMARY KEY("decision_id","title"),
            FOREIGN KEY("decision_id") REFERENCES "Nodes"("id"),
            FOREIGN KEY("test") REFERENCES "Tests"("title")
            );""",
               "create_edges_table": """CREATE TABLE IF NOT EXISTS "Edges" (
            "id"	INTEGER NOT NULL UNIQUE,
            "from_id"	INTEGER,
            "to_id"	INTEGER,
            "min_time"	INTEGER,
            "max_time"	INTEGER,
            "min_fixed"	DATETIME,
            "max_fixed"	DATETIME,
            "start_time"	DATETIME,
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
            "node"	INTEGER NOT NULL,
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
            "name"	TEXT NOT NULL,
            "role"	TEXT NOT NULL,
            PRIMARY KEY("name")
            );""",
               "create_string_nodes_table": """CREATE TABLE IF NOT EXISTS "String_Nodes" (
            "id"	INTEGER NOT NULL UNIQUE,
            "notification"	TEXT,
            PRIMARY KEY("id")
            );""",
               "create_test_nodes_table": """CREATE TABLE IF NOT EXISTS "Test_Nodes" (
            "id"	INTEGER NOT NULL UNIQUE,
            "actors"	TEXT,
            "title"	TEXT NOT NULL,
            "in_charge"	TEXT NOT NULL,
            "time"	INTEGER,
            FOREIGN KEY("id") REFERENCES "Nodes"("id"),
            PRIMARY KEY("id")
            );""",
               "create_test_results_table": """CREATE TABLE IF NOT EXISTS "Test_Results" (
            "test_id"	INTEGER NOT NULL,
            "step"	INTEGER NOT NULL,
            "user_id"	INTEGER NOT NULL,
            "time_taken"	DATETIME NOT NULL,
            "result"	TEXT NOT NULL,
            FOREIGN KEY("test_id") REFERENCES "Tests"("id"),
            PRIMARY KEY("test_id","step","user_id","time_taken"),
            FOREIGN KEY("user_id") REFERENCES "Participants"("id"),
            FOREIGN KEY("step") REFERENCES "Tests"("step")
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
    insert_to_table(query, answer_data)


def addAnswer(form_id, question_num, user_id, time_taken, answer):
    query = """INSERT OR IGNORE INTO Answers (form_id, question_num, user_id, time_taken, answer)
                    VALUES 
                       (?, ?, ?, ?, ?);"""
    answer_data = (form_id, question_num, user_id, time_taken, answer)
    insert_to_table(query, answer_data)


def addComplexNode(node_id, flow_id):
    query = """INSERT OR IGNORE INTO Complex_Nodes (id, flow)
                        VALUES 
                           (?, ?);"""
    node_data = (node_id, flow_id)
    insert_to_table(query, node_data)


def addEdge(edge_id, from_id, to_id, min_time, max_time, fixed_min, fixed_max, start_time):
    query = """INSERT OR IGNORE INTO Edges (id, from_id, to_id, min_time, max_time, fixed_time, start_time)
                    VALUES 
                       (?, ?, ?, ?, ?, ?, ?, ?);"""
    edge_data = (edge_id, from_id, to_id, min_time, max_time, fixed_min, fixed_max, start_time)
    insert_to_table(query, edge_data)


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
    forms[form.questionnaire_number] = form


def addNode(node, op_code):
    query = """INSERT OR IGNORE INTO Nodes (title, type, id)
                    VALUES 
                       (?, ?, ?);"""
    node_data = (node.title, op_code, node.id)
    insert_to_table(query, node_data)


def addParticipant(user_id, name, gender, age, workflow, node):
    query = """INSERT OR IGNORE INTO Participants (id, name, gender, age, workflow, node)
                VALUES 
                   (?, ?, ?, ?, ?, ?);"""
    participant_data = (user_id, name, gender, age, workflow, node)
    insert_to_table(query, participant_data)


def addQuestionnaire(node_id, form_id, node):
    query = """INSERT OR IGNORE INTO Questionnaires (id, form_id)
                VALUES 
                   (?, ?);"""
    node_data = (node_id, form_id)
    insert_to_table(query, node_data)
    questionnaires[node_id] = node


def addQuestionnaireCond(decision_id, title, form_id, question_num, answers):
    query = """INSERT OR IGNORE INTO Conditions_Questionnaire (decision_id, title, form_id, question_num, answers)
                    VALUES 
                       (?, ?, ?, ?, ?);"""
    cond_data = (decision_id, title, form_id, question_num, answers)
    insert_to_table(query, cond_data)


def addStaff(name, role):
    query = """INSERT OR IGNORE INTO Staff (name, role)
                VALUES 
                   (?, ?);"""
    staff_data = (name, role)
    insert_to_table(query, staff_data)


def addStringNode(notification_id, notification):
    query = """INSERT OR IGNORE INTO String_Nodes (notification_id, notification)
                    VALUES 
                       (?, ?);"""
    node_data = (notification_id, notification)
    insert_to_table(query, node_data)


def addTest(node_id, title, instructions, staff, duration):
    query = """INSERT OR IGNORE INTO Tests (node_id, title, instructions, staff, duration)
                    VALUES 
                       (?, ?, ?, ?, ?);"""
    test_data = (node_id, title, instructions, staff, duration)
    insert_to_table(query, test_data)


def addTestNode(node_id, actors, title, in_charge, time):
    query = """INSERT OR IGNORE INTO Test_Nodes (id, actors, title, in_charge, time)
                    VALUES 
                       (?, ?, ?, ?, ?);"""
    node_data = (node_id, actors, title, in_charge, time)
    insert_to_table(query, node_data)


def addTestCond(decision_id, title, test, sat_type, value):
    query = """INSERT OR IGNORE INTO Conditions_Test (decision_id, title, test, type, value)
                    VALUES 
                       (?, ?, ?, ?, ?);"""
    cond_data = (decision_id, title, test, sat_type, value)
    insert_to_table(query, cond_data)


def addTraitCond(decision_id, title, test, sat_type, min_val, max_val):
    query = """INSERT OR IGNORE INTO Conditions_Trait (decision_id, title, test, type, min, max)
                    VALUES 
                       (?, ?, ?, ?, ?, ?);"""
    cond_data = (decision_id, title, test, sat_type, min_val, max_val)
    insert_to_table(query, cond_data)


def addWorkflow(workflow_id, first):
    query = """INSERT OR IGNORE INTO Workflows (id, first_node)
                VALUES 
                   (?, ?);"""
    data = (workflow_id, first)
    insert_to_table(query, data)
    workflows[workflow_id] = first


def getAnswer(form_id, question_number, participant_id):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT answer FROM Answers WHERE form_id=? AND question_num=? AND user_id=? ORDER BY time_taken DESC",
                (form_id, question_number, participant_id))
    rows = cur.fetchall()
    conn.close()
    return rows[0]


def getForm(form_id):
    if form_id in forms:
        return forms.get(form_id)

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
    forms[form_id] = form

    return form


def getWorkflow(workflow_id):
    if workflow_id in workflows:
        return [workflow_id, workflows[workflow_id]]
    query = """SELECT * FROM Workflows WHERE id=?"""
    workflow = extract_one_from_table(query, (workflow_id,))
    if workflow is not None:
        workflows[workflow_id] = [workflow[1]]
    return workflow


def getNode(node_id):
    conn = create_connection()
    curr = conn.cursor()
    curr.execute("SELECT * FROM Nodes WHERE id=?", (node_id,))
    node_data = curr.fetchone()
    conn.close()
    if len(node_data) == 0:
        return None
    if node_data[1] == 1:
        query = """SELECT * FROM Questionnaires WHERE id=?"""
        questionnaire_data = extract_one_from_table(query, (node_id,))
        form = getForm(questionnaire_data[1])
        return buildDALNodes([node_data[1], node_id, node_data[0], form, questionnaire_data[1]])
    # elif node_data[1] == 1:
#         TestNode(node_dict['id'], node_details['title'], tests, node_details['actor in charge'])
#         return [node_id, node_data[0],]


def updateNode(participant_id, node_id):
    query = """UPDATE Participants SET node = ? WHERE id = ?"""
    ids = (node_id, participant_id)
    insert_to_table(query, ids)
