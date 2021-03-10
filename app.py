#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

from flask import Flask, request
from threading import Thread

import logger

from bot import *
from db import DataBase
from game import Game
from keyboards import *
from group_events import Group

from tools.getpostconstructor import json2obj

from identification import *

db = DataBase("students.db")

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
        print(event.type)
        if event.type in Events:
            Events[event.type](event)

# Основной цикл
app = Flask(__name__)

# flask shit
@app.route(f'/')
def main():
    main_text = """
    <h1>Server is up!</h1>
    <img src="http://cdn.funnyisms.com/d3540090-1765-4633-99ff-1bb3ba7e40ec.gif">
    <br>
    """
    main_text += logger.all()
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

@app.route(f'/{link}', methods=['POST'])
def post():
    #data = request.get_json(force=True, silent=True)
    data = request.get_data()
    log = f"#<br>{str(data)}"
    data = json2obj(data)
    log += f" : {str(data)}"
    logger.log(log)
    if data.type == "confirmation":
        return confirmation
    checkEvent(data)
    return 'ok'

if __name__ == '__main__':
    app.run()