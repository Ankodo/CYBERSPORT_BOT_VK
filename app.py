#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

from flask import Flask, request
from threading import Thread

from bot import *
from db import DataBase
from game import Game
from keyboards import *
from group_events import Group

from tools.getpostconstructor import json2obj

from identification import *

db = DataBase("students.db")
vk_test_id = "412536100"

bot = Bot(token, id, db)
game = Game(bot, db)

group = Group(bot, db, miniapps_token)
msgHandler = MessageHandler(bot, db)
buttHandler = ButtonHandler(bot, db)

Events = {
        "message_new" : msgHandler.checkCommand,
        "message_event" : buttHandler.checkCommand,
        "message_allow" : bot.newUser,
        #MESSAGE_DENY : bot.userExit,
        "wall_post_new" : group.postEvent
}

Keyboards = {
        "main_login_keyboard": KeyboardLogin(bot, db),
        "main_keyboard": KeyboardMainMenu(bot, db),
        "main_info_edit_keyboard" : KeyboardMainEditProfile(bot, db),
        "main_game_start" : GameKeyboardMenu(bot, db, game),
        "main_game" : GameKeyboard(bot, db, game),
        "main_tags_keyboard" : KeyboardMainTagsManager(bot, db),
        "inforamtion_edit_keyboard": KeyboardEditProfile(bot, db),
        "cancel_keyboard": CancelLastInput(bot, db)
}

bot.setKeyboards(Keyboards)

def checkEvent(event):
        # print("НОВЫЙ ЭВЕНТ")
        # print(event)
        print(event.type)
        if event.type in Events:
            Events[event.type](event)

# Основной цикл
app = Flask(__name__)
secret = "dnwv8y423bkjbqhbdwhorsehorsehorsehorsewtfwhoishorse"

kostil = []

# flask shit
@app.route(f'/')
def main():
    global kostil
    main_text = """
    <h1>Server is up!</h1>
    <img src="http://cdn.funnyisms.com/d3540090-1765-4633-99ff-1bb3ba7e40ec.gif">
    <br>
    """
    for lol in kostil:
        main_text += "<br>" + lol + "<br>"
    return main_text

@app.route(f'/database')
def databasewatcher():
    main_text = """
    <h1>Server is up!</h1>
    <img src="http://cdn.funnyisms.com/d3540090-1765-4633-99ff-1bb3ba7e40ec.gif">
    <br>
    <h2>Database:</h2>
    """
    db.select("Students")
    studs = db.cursor.fetchall()
    db.select("Pending")
    pen = db.cursor.fetchall()
    db.select("Tags")
    tags = db.cursor.fetchall()
    main_text += "<br><h3>Students:</h3><br>"
    for stud in studs:
        main_text += str(stud) + "<br>"
    main_text += "<br><h3>Pending:</h3><br>"
    for stud in pen:
        main_text += str(stud) + "<br>"
    main_text += "<br><h3>Tags::</h3><br>"
    for stud in tags:
        main_text += str(stud) + "<br>"
    return main_text

@app.route(f'/{secret}', methods=['POST'])
def post():
    global kostil
    kostil.append("#")
    #test2()
    #data = request.get_json(force=True, silent=True)
    #data = request.get() #force=True, silent=True
    data = request.get_data()
    kostil.append(str(data))
    data = json2obj(data)
    kostil.append(str(data))
    if data.type == "confirmation":
        return "32bd1368"
    checkEvent(data)
    return 'ok'

"""
for event in bot.longpoll.listen():
    try:
        thread = Thread(target=checkEvent, args=(event,) )
        thread.start()
        thread.join()
    except:
        print ("Error: unable to start thread:", err)
"""

if __name__ == '__main__':
    app.run()