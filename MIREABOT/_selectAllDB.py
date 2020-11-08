from db import DataBase

db = DataBase("students.db")

db.select("Students")
print(db.cursor.fetchall())

db.select("Pending")
print(db.cursor.fetchall())

db.select("GameMaze")
print(db.cursor.fetchall())

db.select("Subscribes")
print(db.cursor.fetchall())

db.select("Tags")
print(list(map(lambda x: x[0], db.cursor.fetchall())))