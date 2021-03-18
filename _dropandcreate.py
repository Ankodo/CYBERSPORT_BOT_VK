#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

# СОЗДАТЬ БД ДЛЯ БОТА

from db import DataBase

db = DataBase("students.db")
db.execute("DROP TABLE IF EXISTS STUDENTS")
db.execute("DROP TABLE IF EXISTS PENDING")
db.execute("DROP TABLE IF EXISTS GAMEMAZE")
db.execute("DROP TABLE IF EXISTS TAGS")
db.execute("DROP TABLE IF EXISTS SUBSCRIBES")

# Students
# current_keyboard устарел, надо избавиться
db.execute("""
    CREATE TABLE Students (
        user_id INTEGER NOT NULL PRIMARY KEY UNIQUE,
        full_name TEXT,
        code TEXT,
        current_keyboard TEXT);
""")

# Pending
db.execute("""
    CREATE TABLE Pending (
        user_id INTEGER NOT NULL PRIMARY KEY UNIQUE,
        act TEXT,
        FOREIGN KEY(user_id) REFERENCES students(user_id));
""")

# Maze shit
db.execute("""
    CREATE TABLE GameMaze (
        user_id INTEGER NOT NULL PRIMARY KEY UNIQUE,
        p_coords TEXT,
        m_coords TEXT,
        FOREIGN KEY(user_id) REFERENCES students(user_id));
""")

# Tags
db.execute("""
    CREATE TABLE Tags (tag_id TEXT NOT NULL PRIMARY KEY UNIQUE,
        app_id INTEGER NOT NULL UNIQUE
        );
""")

# Таблица с подписками
# УСТАРЕЛО, ЮЗАЕМ ПРИЛОЖЕНИЕ ДЛЯ РАССЫЛКИ
# db.execute("""
#     CREATE TABLE Subscribes
#     (
#         user_id INTEGER NOT NULL,
#         tag_id TEXT  NOT NULL,
#         PRIMARY KEY (user_id, tag_id),
#         FOREIGN KEY (user_id) REFERENCES Students
#         FOREIGN KEY (tag_id) REFERENCES Tags
#     )
# """)

db.execute("""
    INSERT INTO TAGS VALUES ('#тест', 1076800), ('#киберfire', 1030787), ('#конкурс', 1017367), ('#новости', 1020555), ('#киберsale', 1017366), ('#анонс', 1017119), ('#киберnews', 1016793), ('#турниры', 1016042)
""")

db.connection.commit()

print("БД очищена!")
