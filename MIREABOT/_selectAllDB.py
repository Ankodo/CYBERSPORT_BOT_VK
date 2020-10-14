from db import DataBase

db = DataBase("students.db")

db.select("Students")
print(db.cursor.fetchall())

db.select("Pending")
print(db.cursor.fetchall())