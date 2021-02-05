from db import DataBase

db = DataBase("students.db")

print("Students:")
db.select("Students")
print(db.cursor.fetchall())

print("Pending:")
db.select("Pending")
print(db.cursor.fetchall())

print("Maze:")
db.select("GameMaze")
print(db.cursor.fetchall())

#print("Subscribes:")
#db.select("Subscribes")
#print(db.cursor.fetchall())

print("Tags:")
db.select("Tags")
print(db.cursor.fetchall())
#print(list(map(lambda x: x[0], db.cursor.fetchall())))