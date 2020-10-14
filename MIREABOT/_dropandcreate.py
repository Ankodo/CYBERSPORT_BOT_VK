from db import DataBase

db = DataBase("students.db")
db.execute("DROP TABLE STUDENTS")
db.execute("DROP TABLE PENDING")
db.execute("""
CREATE TABLE Students (user_id INTEGER NOT NULL PRIMARY KEY UNIQUE, full_name TEXT, code TEXT);
""")
db.execute("""
CREATE TABLE Pending (user_id INTEGER NOT NULL PRIMARY KEY UNIQUE, act TEXT, FOREIGN KEY(user_id) REFERENCES students(user_id));
""")
db.connection.commit()