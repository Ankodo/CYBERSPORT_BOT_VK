from db import DataBase

db = DataBase("students.db")
db.execute("DROP TABLE IF EXISTS STUDENTS")
db.execute("DROP TABLE IF EXISTS PENDING")
db.execute("DROP TABLE IF EXISTS GAMEMAZE")
db.execute("""
CREATE TABLE Students (user_id INTEGER NOT NULL PRIMARY KEY UNIQUE, full_name TEXT, code TEXT, current_keyboard TEXT, subscribed TEXT);
""")
db.execute("""
CREATE TABLE Pending (user_id INTEGER NOT NULL PRIMARY KEY UNIQUE, act TEXT, FOREIGN KEY(user_id) REFERENCES students(user_id));
""")

db.execute("""
CREATE TABLE GameMaze (user_id INTEGER NOT NULL PRIMARY KEY UNIQUE,
 p_coords TEXT, m_coords TEXT, FOREIGN KEY(user_id) REFERENCES students(user_id));
""")
db.connection.commit()