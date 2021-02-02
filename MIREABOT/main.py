from threading import Thread

from bot import *
from db import DataBase
from game import Game
from keyboards import *
from group_events import Group

from identification import *

db = DataBase("students.db")

bot = Bot(token, id, db)
game = Game(bot, db)

group = Group(bot, db, miniapps_token)
msgHandler = MessageHandler(bot, db)
buttHandler = ButtonHandler(bot, db)

Events = {
        VkBotEventType.MESSAGE_NEW : msgHandler.checkCommand,
        VkBotEventType.MESSAGE_EVENT : buttHandler.checkCommand,
        VkBotEventType.MESSAGE_ALLOW : bot.newUser,
        VkBotEventType.MESSAGE_DENY : bot.userExit,
        VkBotEventType.WALL_POST_NEW : group.postEvent
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
print("Бот запущен")
for event in bot.longpoll.listen():
    try:
        thread = Thread(target=checkEvent, args=(event,) )
        thread.start()
        thread.join()
    except:
        print ("Error: unable to start thread:", err)