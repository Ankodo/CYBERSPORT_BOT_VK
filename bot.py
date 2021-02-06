#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

from vk_api import VkApi
from datetime import datetime
from vk_api.utils import get_random_id
#from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

class MessageHandler:
    """Обработчик сообщений"""
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
            "REGISTER_CODE" : self.registerCode,
            "EDIT_NAME" : self.editName,
            "EDIT_CODE" : self.editCode
        }

    def checkCommand(self, event):
        """Обработка текстовых сообщений"""
        # NOTE: Давай по новой, Саша, рефакторинг херня
        request = event.object.body
        user_id = event.object.user_id

        self.db.select("Students", "user_id", f"WHERE user_id='{user_id}'")
        res = self.db.cursor.fetchone()

        if res != None:
            if request != None and request != "":
                if not self.checkPending(event):
                    if request in self.MessageCommands.keys():
                        self.MessageCommands[request](event)
                    else:
                        self.bot.writeMsg(event.object.user_id, f"Команда не распознана. Напиши !Команды для списка всех команд.")
            else:
                self.bot.writeMsg(event.object.user_id, f"Круто, а что это?")
        else:
            #self.bot.sendKeyboard(user_id, "main_login_keyboard", """Привет, давай познакомимся! 🐉""")
            self.bot.sendKeyboard(user_id, "main_keyboard", """Привет 🐉""")
            self.db.insert("Students", "user_id, current_keyboard", f"'{user_id}', 'main_login_keyboard'")
            self.db.connection.commit()

    def checkPending(self, event):
        """Проверка на ожидание ввода от пользователя"""
        self.db.select("Pending", "act", f"WHERE user_id='{event.object.user_id}'")
        res = self.db.cursor.fetchone()
        print("Checking pending:", res)
        #прости господи
        if res != None:
            res = res[0]
        #
        if res != None:
            if res in self.PendingStats:
                self.PendingStats[res](event)
            else:
                self.bot.writeMsg(event.object.user_id, f"Ошибка: {event.object.body} не найден. Отправьте это сообщение администраторам группы")
            return True
        else:
            return False

    ####    КОМАНДЫ    ####

    def sayHi(self, event):
        self.bot.writeMsg(event.object.user_id, "привет!!!")

    def showSimilar(self, event):
        self.bot.writeMsg(event.object.user_id, "Похожие команды:")

    def showExampleKeyboard(self, event):
        user_id = event.object.user_id
        self.db.select("Students", "user_id", f"WHERE user_id='{user_id}'")
        res = self.db.cursor.fetchone()
        self.bot.sendKeyboard(user_id, "main_keyboard", """Держи 🐉""", True)

    ####    РЕГИСТРАЦИЯ    ####

    def registerName(self, event):
        # Регистрируем имя
        self.db.update("Students", "full_name", f"'{event.object.body}'", f"WHERE user_id = '{event.object.user_id}'")
        self.db.update("Pending", "act", "'REGISTER_CODE'", f"WHERE user_id = '{event.object.user_id}'")
        self.db.connection.commit()
        self.bot.writeMsg(event.object.user_id, "Рад познакомиться. 🐉 Теперь введи шифр своей группы")

    def registerCode(self, event):
        # Регистрируем код
        self.db.update("Students", "code", f"'{event.object.body}'", f"WHERE user_id = '{event.object.user_id}'")
        self.db.update("Pending", "act", "NULL", f"WHERE user_id = '{event.object.user_id}'")
        self.db.connection.commit()
        self.bot.sendKeyboard(event.object.user_id, "main_keyboard", "Я запомнил 🐉", True)

    ####    РЕДАКТИРОВАНИЕ    ####
    def editName(self, event):
        # Редактируем имя
        user_id = event.object.user_id
        self.db.update("Students", "full_name", f"'{event.object.body}'", f"WHERE user_id = '{user_id}'")
        self.db.update("Pending", "act", "NULL", f"WHERE user_id = '{user_id}'")
        self.db.connection.commit()
        self.bot.sendKeyboard(user_id, "main_info_edit_keyboard", "Имя успешно обновлено")

    def editCode(self, event):
        # Редактируем код
        user_id = event.object.user_id
        self.db.update("Students", "code", f"'{event.object.body}'", f"WHERE user_id = '{user_id}'")
        self.db.update("Pending", "act", "NULL", f"WHERE user_id = '{user_id}'")
        self.db.connection.commit()
        self.bot.sendKeyboard(user_id, "main_info_edit_keyboard", "Группа успешно обновлена")


class ButtonHandler:
    """Обработчик нажатий на кнопки"""
    def __init__(self, bot, db):
        super().__init__()
        self.ButtonCommands = {
            #   Кнопки-сообщения
            "info_edit_call":    self.infoEditCall,
            "cancel_call":       self.cancellCall
        }

        self.bot = bot
        self.db = db

    #
    #   Кнопки-сообщения
    #

    def infoEditCall(self, event):
        """Пользователь нажал на кнопку редактирования профиля"""
        user_id = event.object.user_id
        #self.bot.sendKeyboard(user_id, "main_info_edit_keyboard", "Меню редактирования профиля", True)
        self.bot.sendKeyboard(user_id, "main_keyboard", "Uh uh uh! You didn't say the magic word!", True)

    def cancellCall(self, event):
        """Пользователь отменил ввод данных"""
        user_id = event.object.user_id
        self.db.update("Pending", "act", "NULL", f"WHERE user_id = '{user_id}'")
        self.db.connection.commit()
        # keyboard = event.object.payload.get('keyboard')
        self.bot.sendKeyboard(user_id, "main_keyboard", "Отменяем ввод", True)
        #self.bot.sendKeyboard(user_id, self.getCurrentKeyboard(user_id), "Отменяем ввод")

    #
    #   Обработчик
    #

    def checkCommand(self, event):
        user_id = event.object.user_id
        call = event.object.payload.type
        exception = None
        if hasattr(event.object.payload, 'exception'):
            exception = event.object.payload.exception
        keyboard = event.object.payload.keyboard

        def runEvent():
            if keyboard == None:
                self.bot.writeMsg(event.object.user_id, "Пожалуйста, отправьте скриншот адмнистраторам.\nОшибка: эвент не привязан к клавиатуре")
            elif keyboard == "oneline":
                # Если это кнопка-сообщение
                self.ButtonCommands[call](event)
            elif self.bot.keyboards[keyboard].checkCommand(event):
                # Если функция была найдена и выполнена
                pass
            else:
                # Такого эвента нет
                self.bot.writeMsg(event.object.user_id, "Пожалуйста, отправьте скриншот адмнистраторам.\nОшибка: эвент не найден")
                print(f"FATAL - {call}")

        self.db.select("Students", "user_id", f"WHERE user_id='{user_id}'")
        res = self.db.cursor.fetchone()

        if res == None:
            self.db.insert("Students", "user_id, current_keyboard", f"'{user_id}', 'main_login_keyboard'")
            self.db.connection.commit()

        if not self.checkPending(user_id):
            runEvent()
        elif exception != None:
            runEvent()
        else:
            self.bot.writeMsg(user_id, "От Вас ожидается ввод данных.")

    def checkPending(self, user_id):
        self.db.select("Pending", "act", f"WHERE user_id='{user_id}'")
        res = self.db.cursor.fetchone()
        if res == None:
            return False
        elif res[0] != None:
            return True
        else: return False

    def getCurrentKeyboard(self, user_id):
        keyboard = None
        self.db.select("Students", "current_keyboard", f"WHERE user_id='{user_id}'")
        res = self.db.cursor.fetchone()
        if res != None:
            keyboard = res[0]

        return keyboard

class Bot:
    """Бот"""
    def __init__(self, token, id, db):
        super().__init__()
        self.token = token
        self.id = id
        self.db = db

        self.session = VkApi(token=token, api_version="5.124")
        self.vk = self.session.get_api()
        #self.longpoll = VkBotLongPoll(self.session, group_id=id)

        self.keyboards = None

    def setKeyboards(self, keyboards):
        self.keyboards = keyboards

    def newUser(self, event):
        self.sendKeyboard(event.object.user_id, "main_login_keyboard", "Добро пожаловать!\n Давай заполним твой профиль")

    def userExit(self, event):
        #print(f"Пользователь {event.object.user_id} запретил сообщения.")
        pass

    def writeMsg(self, user_id, message):
        """Отправить пользователю сообщение"""
        self.session.method('messages.send', {'user_id': user_id, 'message': message, "random_id":get_random_id()})

    def attachmentMsg(self, user_id, attachment_type, attachment_id):
        """Отправить пользователю изображение"""
        ownid = f"-{self.id}"
        self.session.method('messages.send', {'user_id': user_id, "random_id":get_random_id(), "attachment":f"{attachment_type}{ownid}_{attachment_id}"})

    def repostPost(self, user_id, id):
        """Отправить пользователю запись"""
        self.attachmentMsg(user_id, "wall", id)

    def setCurrentKeyboard(self, id, keyboard):
        """Установить клавиатуру в бд"""
        self.db.update("Students", "current_keyboard", f"'{keyboard}'", f"WHERE user_id='{id}'")
        self.db.connection.commit()

    def sendKeyboard(self, from_id, keyboard, text="", set_as_current=False, static=False):
        """Отправить пользователю клавиатуру"""
        if keyboard in self.keyboards:
            if text == "": text = "Выполнено"
            if set_as_current:
                self.setCurrentKeyboard(from_id, keyboard)
            if static:
                keyboard=self.keyboards[keyboard].build(from_id)
                keyboard = keyboard.get_keyboard()
            else:
                keyboard = self.keyboards[keyboard].keyboard.get_keyboard()
            self.vk.messages.send(
                user_id=from_id,
                random_id=get_random_id(),
                peer_id=from_id,
                keyboard=keyboard,
                message=text
            )
