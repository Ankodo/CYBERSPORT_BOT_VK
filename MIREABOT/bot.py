from vk_api import VkApi
from datetime import datetime
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from keyboards import *


class MessageHandler:
    def __init__(self, bot, db):
        super().__init__()
        self.bot = bot
        self.db = db

        self.MessageCommands = {
            "!привет" : self.sayHi,
            "!клавиатура" : self.showExampleKeyboard
        }

        self.PendingStats = {
            "REGISTER_NAME" : self.registerName,
            "REGISTER_CODE" : self.registerCode
        }

    def checkCommand(self, event):
        request = event.obj.message['text']
        user_id = event.obj.message['from_id']
        print (f"Новый текстовый запрос: {user_id}: {request}")
        print(self.MessageCommands)
        if request in self.MessageCommands: 
            print("запрос найден")
            self.MessageCommands[request](event)
        elif "!" == request[0]:
            self.showSimilar(event)
        else:
            self.checkPending(event)

    def sayHi(self, event):
        self.bot.writeMsg(event.obj.message['from_id'], "привет!!!")

    def showSimilar(self, event):
        self.bot.writeMsg(event.obj.message['from_id'], "Похожие команды:")

    def showExampleKeyboard(self, event):
        self.db.select("Students", "user_id", f"WHERE user_id='{event.obj.message['from_id']}'")
        res = self.db.cursor.fetchone()
        if res == None:
            self.bot.sendKeyboard(event.obj.message['from_id'], """Для начала следует войти 🐉""", "login_keyboard")
        else:
            self.bot.sendKeyboard(event.obj.message['from_id'], """Держи 🐉""", "main_sub_keyboard")

    def checkPending(self, event):
        self.db.select("Pending", "act", f"WHERE user_id='{event.obj.message['from_id']}'")
        res = self.db.cursor.fetchone()
        print(res)
        if res != None:
            res = res[0]
            if res in self.PendingStats:
                print("Pending есть у юзера")
                self.PendingStats[res](event)

    #### РЕГИСТРАЦИЯ ####

    def registerName(self, event):
        # Регистрируем имя
        self.db.update("Students", "full_name", f"'{event.obj.message['text']}'", f"WHERE user_id = '{event.obj.message['from_id']}'")
        self.db.update("Pending", "act", "'REGISTER_CODE'", f"WHERE user_id = '{event.obj.message['from_id']}'")
        self.db.connection.commit()
        self.bot.writeMsg(event.obj.message['from_id'], "Рад познакомиться. 🐉 Теперь введи свою группу в формате ШИФР-ЧИСЛО-ЧИСЛО")

    def registerCode(self, event):
        # Регистрируем код
        self.db.update("Students", "code", f"'{event.obj.message['text']}'", f"WHERE user_id = '{event.obj.message['from_id']}'")
        self.db.update("Pending", "act", "'NONE'", f"WHERE user_id = '{event.obj.message['from_id']}'")
        self.db.connection.commit()
        self.bot.sendKeyboard(event.obj.message['from_id'], "Добро пожаловать. Еще раз 🐉", "main_sub_keyboard")
        self.bot.writeMsg(event.obj.message['from_id'], 
"""
Помимо меню бот может управляться с помощью команд. Перед командами ставится восклицательный знак:
!сброс - если что-то пошло не так
!клавиатура - вызов меню
"""
        )

    ####


class ButtonHandler:
    def __init__(self, bot, db):
        #TODO: Привязать действия к клавиатуре, а не к одному обработчику
        super().__init__()
        self.ButtonCommands = {
            "login_call":               self.loginCall,
            "information_call":         self.infoCall,
            "information_edit_call":    self.infoEditCall,
            "sub_call":                 self.subCall,
            "unsub_call":               self.unSubCall,
            "notes_call":               lambda x: self.bot.writeMsg(x.obj.user_id, "Тут что-то будет про записи 🤔🤔🤔"),
            "game_call":                self.gameCall,
            "exit_call":                self.exitCall
        }

        self.bot = bot
        self.db = db

    def checkCommand(self, event):
        print("Нажата кнопка")
        if event.obj.payload.get('type') in self.ButtonCommands:
            self.ButtonCommands[event.obj.payload.get('type')](event)

    def loginCall(self, event):
        # ВХОД
        # NOTE: Лучше стоит заменить на MINI APPS
        self.bot.writeMsg(event.obj.user_id, "Поиск в базе")
        self.db.select("Students", "user_id", f"WHERE user_id='{event.obj.user_id}'")
        res = self.db.cursor.fetchone()
        if res == None:
            self.bot.writeMsg(event.obj.user_id, "Для начала введи свое полное имя")
            self.db.insert("Students", "user_id", f"'{event.obj.user_id}'")
            self.db.insert("Pending", "user_id, act", f"'{event.obj.user_id}', 'REGISTER_NAME'")
            self.db.connection.commit()
        else:
            self.bot.sendKeyboard(event.obj.user_id, "Вы успешно авторизовались!", "main_sub_keyboard")

    def infoCall(self, event):
        self.db.select("Students", "user_id", f"WHERE user_id='{event.obj.user_id}'")
        res1 = self.db.cursor.fetchone()
        self.db.select("Students", "full_name", f"WHERE user_id='{event.obj.user_id}'")
        res2 = self.db.cursor.fetchone()
        self.db.select("Students", "code", f"WHERE user_id='{event.obj.user_id}'")
        res3 = self.db.cursor.fetchone()

        if res1 != None and res2 != None and res3 != None:
            text = f"""
id = {res1[0]}
Имя - {res2[0]}
Группа - {res3[0]}
"""
        print(text)
        self.bot.sendKeyboard(event.obj.user_id, text, "inforamtion_edit_keyboard")

    def infoEditCall(self, event):
        self.bot.writeMsg(event.obj.user_id, "Введи свое полное имя")
        self.db.update("Pending", "act", "'REGISTER_NAME'", f"WHERE user_id = '{event.obj.user_id}'")
        self.db.connection.commit()

    def subCall(self, event):
        self.bot.sendKeyboard(event.obj.user_id, "Вы подписались на новости группы", "main_uns_keyboard")

    def unSubCall(self, event):
        self.bot.sendKeyboard(event.obj.user_id, "Вы отписались от новостей группы", "main_sub_keyboard")

    def gameCall(self, event):
        self.bot.writeMsg(event.obj.user_id, "К сожалению, из-за спагетти кода было решено провести рефакторинг, поэтому игры пока-что нету")


    def exitCall(self, event):
        self.bot.sendKeyboard(event.obj.user_id, "Удачи! 🐉", "login_keyboard")


class Bot:
    def __init__(self, token, id):
        super().__init__()
        self.token = token
        self.id = id

        self.session = VkApi(token=token, api_version="5.124")
        self.vk = self.session.get_api()
        self.longpoll = VkBotLongPoll(self.session, group_id=id)

        self.keyboards = {
            "login_keyboard": KeyboardLogin().keyboard,
            "main_sub_keyboard": KeyboardMainNoSub().keyboard,
            "main_uns_keyboard": KeyboardMainWithSub().keyboard,

            "inforamtion_edit_keyboard": EditProfile().keyboard
        }

    def newUser(self, event):
        self.sendKeyboard(event.obj.user_id, 
"""Добро пожаловать! 🐉
Прежде чем начать, давай познакомимся 👀
Для этого, пожалуйста, заполни свой профиль ниже ☺"""
        ,"login_keyboard")

    def userExit(self, event):
        print(f"Пользователь {event.obj.user_id} запретил сообщения.")

    def writeMsg(self, user_id, message):
        self.session.method('messages.send', {'user_id': user_id, 'message': message, "random_id":get_random_id()})

    def attachmentMsg(self, user_id, attachment_type, attachment_id):
        ownid = "-199323686"
        self.session.method('messages.send', {'user_id': user_id, "random_id":get_random_id(), "attachment":f"{attachment_type}{ownid}_{attachment_id}"})

    def sendKeyboard(self, from_id, text, keyboard):
        if keyboard in self.keyboards:
            self.vk.messages.send(
                        user_id=from_id,
                        random_id=get_random_id(),
                        peer_id=from_id,
                        keyboard=self.keyboards[keyboard].get_keyboard(),
                        message=text)
