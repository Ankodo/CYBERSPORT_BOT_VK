#�������
#0 - � ����� ����
#1 - ������ ������
#2 - ������ ���
#G0 - игра меню
#G1 - игра выбор сложности
#G2 - В игре
#G3 - отметка

import sqlite3
 
conn = sqlite3.connect("botdb.db") # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()
 
try:
    cursor.execute("""CREATE TABLE users_info
                    (status text,
                    vk_id text,
                    STUD text, 
                    FIO text,
                    PARTY text)""")
    print('db cleated')
except:
    print('db downloaded')

def getUserStatus(userId):
    try:
        sql = "SELECT status FROM users_info WHERE vk_id=?"
        cursor.execute(sql, [str(userId)])
        return cursor.fetchone()[0]
    except:
        return '-1'

def addUser(userId):
    cursor.execute("""INSERT INTO users_info
                  VALUES ('0', ?,'0','0','0')""", [str(userId)])
    conn.commit()

def getUserSTUD(userId):
    sql = "SELECT STUD FROM users_info WHERE vk_id=?"
    cursor.execute(sql, [str(userId)])
    return cursor.fetchone()[0]

def getUserFIO(userId):
    sql = "SELECT FIO FROM users_info WHERE vk_id=?"
    cursor.execute(sql, [str(userId)])
    return cursor.fetchone()[0]
    return out

def getUserGROUP(userId):
    sql = "SELECT PARTY FROM users_info WHERE vk_id=?"
    cursor.execute(sql, [str(userId)])
    return cursor.fetchone()[0]
    return out

def setUserStatus(userId, status):
    sql = "UPDATE users_info SET status=? WHERE vk_id=?"
    cursor.execute(sql, [status, str(userId)])
    conn.commit()

def setUserSTUD(userId, STUD):
    sql = """UPDATE users_info SET STUD=? WHERE vk_id=?"""
    cursor.execute(sql, [STUD, str(userId)])
    conn.commit()
    setUserStatus(userId, '0')

def setUserFIO(userId, FIO):
    sql = "UPDATE users_info SET FIO=? WHERE vk_id=?"
    cursor.execute(sql, [FIO, str(userId)])
    conn.commit()
    setUserStatus(userId, '0')

def setUserGROUP(userId, GROUP):
    sql = "UPDATE users_info SET PARTY=? WHERE vk_id=?"
    cursor.execute(sql, [GROUP, str(userId)])
    conn.commit()
    setUserStatus(userId, '0')