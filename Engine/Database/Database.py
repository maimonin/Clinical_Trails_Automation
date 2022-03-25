import sqlite3

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


def execute_sql(conn, query):
    try:
        c = conn.cursor()
        c.execute(query)
        conn.commit()
    except sqlite3.Error as e:
        print(e)


def insert_to_table(conn, query, data):
    cur = conn.cursor()
    try:
        cur.execute(query, data)
        conn.commit()
        conn.close()
    except sqlite3.Error:
        return


def init_tables():
    create_Actors_To_Notify_table = """CREATE TABLE IF NOT EXISTS "Actors_To_Notify" (
            "notification_id"	INTEGER NOT NULL,
            "actor_name"	TEXT,
            PRIMARY KEY("notification_id","actor_name"),
            FOREIGN KEY("notification_id") REFERENCES "String_Nodes"("id")
            );"""

    create_Answer_Options_table = """CREATE TABLE IF NOT EXISTS "Answer_Options" (
            "form_id"	INTEGER NOT NULL,
            "number"	INTEGER NOT NULL,
            "option_num"	INTEGER NOT NULL,
            "option"	TEXT NOT NULL,
            FOREIGN KEY("form_id") REFERENCES "Questions"("form_id"),
            PRIMARY KEY("form_id","number","option_num")
            );"""

    create_Answers_table = """CREATE TABLE IF NOT EXISTS "Answers" (
            "form_id"	INTEGER NOT NULL,
            "question_num"	INTEGER NOT NULL,
            "user_id"	INTEGER NOT NULL,
            "time_taken"	DATETIME NOT NULL,
            "answer"	TEXT NOT NULL,
            PRIMARY KEY("form_id","user_id","time_taken","question_num"),
            FOREIGN KEY("form_id") REFERENCES "Questionnaires"("form_id"),
            FOREIGN KEY("question_num") REFERENCES "Questions"("number"),
            FOREIGN KEY("user_id") REFERENCES "Participants"("id")
            );"""

    create_Complex_Nodes_table = """CREATE TABLE IF NOT EXISTS "Complex_Nodes" (
            "id"	INTEGER NOT NULL UNIQUE,
            "flow"	INTEGER NOT NULL,
            PRIMARY KEY("id"),
            FOREIGN KEY("flow") REFERENCES "Workflows"("id")
            );"""

    create_Decisions_table = """CREATE TABLE IF NOT EXISTS "Decisions" (
            "id"	INTEGER NOT NULL UNIQUE,
            "min_age"	INTEGER NOT NULL,
            "max_age"	INTEGER,
            "gender"	TEXT,
            "other"	TEXT,
            PRIMARY KEY("id")
            );"""

    create_Edges_table = """CREATE TABLE IF NOT EXISTS "Edges" (
            "id"	INTEGER NOT NULL UNIQUE,
            "min_time"	INTEGER,
            "max_time"	INTEGER,
            "from_id"	INTEGER,
            "to_id"	INTEGER,
            FOREIGN KEY("from_id") REFERENCES "Nodes"("id"),
            FOREIGN KEY("to_id") REFERENCES "Nodes"("id")
            );"""

    create_Nodes_table = """CREATE TABLE IF NOT EXISTS "Nodes" (
            "title"	TEXT NOT NULL,
            "type"	INTEGER NOT NULL,
            "id"	INTEGER,
            PRIMARY KEY("id")
            );"""

    create_Participants_table = """CREATE TABLE IF NOT EXISTS "Participants" (
            "id"	INTEGER NOT NULL,
            "name"	TEXT NOT NULL,
            "gender"	TEXT NOT NULL,
            "age"	INTEGER NOT NULL,
            "workflow"	INTEGER NOT NULL,
            "node"	INTEGER NOT NULL,
            PRIMARY KEY("id")
            );"""

    create_Questionnaires_table = """CREATE TABLE IF NOT EXISTS "Questionnaires" (
            "id"	INTEGER NOT NULL UNIQUE,
            "form_id"	INTEGER NOT NULL,
            PRIMARY KEY("id"),
            FOREIGN KEY("id") REFERENCES "Nodes"("id"),
            FOREIGN KEY("form_id") REFERENCES "Questions"("form_id")
            );"""

    create_Questions_table = """CREATE TABLE IF NOT EXISTS "Questions" (
            "form_id"	INTEGER NOT NULL,
            "number"	INTEGER NOT NULL,
            "question"	TEXT NOT NULL,
            "type"	TEXT NOT NULL,
            PRIMARY KEY("form_id","number"),
            FOREIGN KEY("form_id") REFERENCES "Questionnaires"("form_id")
            );"""

    create_Staff_table = """CREATE TABLE IF NOT EXISTS "Staff" (
            "name"	TEXT NOT NULL,
            "role"	TEXT NOT NULL,
            PRIMARY KEY("name")
            );"""

    create_String_Nodes_table = """CREATE TABLE IF NOT EXISTS "String_Nodes" (
            "id"	INTEGER NOT NULL UNIQUE,
            "notification"	TEXT,
            "actors_list"	INTEGER,
            PRIMARY KEY("id")
            );"""

    create_Test_Nodes_table = """CREATE TABLE IF NOT EXISTS "Test_Nodes" (
            "id"	INTEGER NOT NULL UNIQUE,
            "test"	INTEGER NOT NULL,
            "in_charge"	INTEGER NOT NULL,
            FOREIGN KEY("id") REFERENCES "Nodes"("id"),
            PRIMARY KEY("id","test")
            );"""

    create_Test_Results_table = """CREATE TABLE IF NOT EXISTS "Test_Results" (
            "test_id"	INTEGER NOT NULL,
            "step"	INTEGER NOT NULL,
            "user_id"	INTEGER NOT NULL,
            "time_taken"	DATETIME NOT NULL,
            "result"	TEXT NOT NULL,
            FOREIGN KEY("test_id") REFERENCES "Tests"("id"),
            PRIMARY KEY("test_id","step","user_id","time_taken"),
            FOREIGN KEY("user_id") REFERENCES "Participants"("id"),
            FOREIGN KEY("step") REFERENCES "Tests"("step")
            );"""

    create_Tests_table = """CREATE TABLE IF NOT EXISTS "Tests" (
            "id"	INTEGER NOT NULL,
            "step"	INTEGER NOT NULL,
            "instruction"	TEXT NOT NULL,
            "text"	TEXT NOT NULL,
            "staff"	TEXT,
            "title"	TEXT,
            "duration"	TEXT,
            PRIMARY KEY("id","step")
            );"""

    create_Workflows_table = """CREATE TABLE IF NOT EXISTS "Workflows" (
            "id"	INTEGER NOT NULL,
            "name"	TEXT NOT NULL,
            PRIMARY KEY("id")
            );"""

    conn = create_connection()
    if conn is not None:
        execute_sql(conn, create_Actors_To_Notify_table)
        execute_sql(conn, create_Answer_Options_table)
        execute_sql(conn, create_Answers_table)
        execute_sql(conn, create_Complex_Nodes_table)
        execute_sql(conn, create_Decisions_table)
        execute_sql(conn, create_Edges_table)
        execute_sql(conn, create_Nodes_table)
        execute_sql(conn, create_Participants_table)
        execute_sql(conn, create_Questionnaires_table)
        execute_sql(conn, create_Questions_table)
        execute_sql(conn, create_Staff_table)
        execute_sql(conn, create_String_Nodes_table)
        execute_sql(conn, create_Test_Nodes_table)
        execute_sql(conn, create_Test_Results_table)
        execute_sql(conn, create_Tests_table)
        execute_sql(conn, create_Workflows_table)

    else:
        print("Error! cannot create the database connection.")
    conn.close()


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


def addForm(form):
    conn = create_connection()
    cur = conn.cursor()
    for question in form.questions:
        query = """INSERT INTO Questions (form_id, number, question, type)
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


def addQuestionnaire(id, form_id, node):
    conn = create_connection()
    query = """INSERT INTO Questionnaires (id, form_id)
                VALUES 
                   (?, ?);"""
    node_data = (id, form_id)
    insert_to_table(conn, query, node_data)
    questionnaires[id] = node


def addWorkflow(id, name):
    conn = create_connection()
    query = """INSERT INTO Workflows (id, name)
                VALUES 
                   (?, ?);"""
    data = (id, name)
    insert_to_table(conn, query, data)
    workflows[id] = [id, name]


def addParticipant(id, name, gender, age, workflow):
    conn = create_connection()
    query = """INSERT INTO Participants (id, name, gender, age, workflow)
                VALUES 
                   (?, ?, ?, ?, ?);"""
    participant_data = (id, name, gender, age, workflow)
    insert_to_table(conn, query, participant_data)


def addStaff(name, role):
    conn = create_connection()
    query = """INSERT INTO Staff (name, role)
                VALUES 
                   (?, ?);"""
    staff_data = (name, role)
    insert_to_table(conn, query, staff_data)


def addAnswer(form_id, question_num, user_id, time_taken, answer):
    conn = create_connection()
    query = """INSERT INTO Answers (form_id, question_num, user_id, time_taken, answer)
                    VALUES 
                       (?, ?, ?, ?, ?);"""
    answer_data = (form_id, question_num, user_id, time_taken, answer)
    insert_to_table(conn, query, answer_data)
