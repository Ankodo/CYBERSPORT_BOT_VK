from db import DataBase

db = DataBase("students.db")
db.execute("DROP TABLE IF EXISTS STUDENTS")
db.execute("DROP TABLE IF EXISTS PENDING")
db.execute("DROP TABLE IF EXISTS GAMEMAZE")
db.execute("DROP TABLE IF EXISTS TAGS")
db.execute("DROP TABLE IF EXISTS SUBSCRIBES")
db.execute("""
CREATE TABLE Students (user_id INTEGER NOT NULL PRIMARY KEY UNIQUE, full_name TEXT, code TEXT, current_keyboard TEXT);
""")
db.execute("""
CREATE TABLE Pending (user_id INTEGER NOT NULL PRIMARY KEY UNIQUE, act TEXT, FOREIGN KEY(user_id) REFERENCES students(user_id));
""")

db.execute("""
CREATE TABLE GameMaze (user_id INTEGER NOT NULL PRIMARY KEY UNIQUE,
 p_coords TEXT, m_coords TEXT, FOREIGN KEY(user_id) REFERENCES students(user_id));
""")

# Tags
db.execute("""
CREATE TABLE Tags (tag_id TEXT NOT NULL PRIMARY KEY UNIQUE);
""")

# Таблица с подписками
db.execute(
    """
CREATE TABLE Subscribes
( 
    user_id INTEGER NOT NULL,
    tag_id TEXT  NOT NULL,
    PRIMARY KEY (user_id, tag_id),
    FOREIGN KEY (user_id) REFERENCES Students
    FOREIGN KEY (tag_id) REFERENCES Tags
)
    """
)

db.execute("INSERT INTO TAGS VALUES ('#важное'), ('#новости'), ('#конкурс')")
#db.execute("INSERT INTO Students VALUES (412536100, 'Шашков Александр Андреевич', 'КМБО-03-20', 'main_sub_keyboard')")

db.connection.commit()