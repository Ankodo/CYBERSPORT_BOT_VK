#   TODO: обращаться к классу Клавиатуры для ее установки к бд
#   self.setCurrentKeyboard(event, keyboard) привязать к функции выше

from vk_api import VkApi
from datetime import datetime
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

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

    def setCurrentKeyboard(self, event, keyboard):
        """Установить клавиатуру в бд"""
        user_id = event.obj.message['from_id']
        self.db.update("Students", "current_keyboard", f"'{keyboard}'", f"WHERE user_id='{user_id}'")
        self.db.connection.commit()

    def checkPending(self, event):
        self.db.select("Pending", "act", f"WHERE user_id='{event.obj.message['from_id']}'")
        res = self.db.cursor.fetchone()
        print(res)
        if res != None:
            res = res[0]
            if res in self.PendingStats:
                print("Pending есть у юзера")
                self.PendingStats[res](event)

    ###

    def sayHi(self, event):
        self.bot.writeMsg(event.obj.message['from_id'], "привет!!!")

    def showSimilar(self, event):
        self.bot.writeMsg(event.obj.message['from_id'], "Похожие команды:")

    def showExampleKeyboard(self, event):
        print("Поиск в БД")
        user_id = event.obj.message['from_id']
        self.db.select("Students", "user_id", f"WHERE user_id='{user_id}'")
        res = self.db.cursor.fetchone()
        print("Поиск закончен")
        if res == None:
            print("юзер не вошел")
            self.bot.sendKeyboard(user_id, "main_login_keyboard", """Для начала следует войти 🐉""")
            self.db.insert("Students", "user_id, current_keyboard", f"'{user_id}', 'main_login_keyboard'")
            self.db.connection.commit()
        else:
            print("юзер найден")
            self.bot.sendKeyboard(user_id, "main_sub_keyboard", """Держи 🐉""")
            self.setCurrentKeyboard(event, "main_sub_keyboard")

    #### РЕГИСТРАЦИЯ ####

    def registerName(self, event):
        # Регистрируем имя
        self.db.update("Students", "full_name", f"'{event.obj.message['text']}'", f"WHERE user_id = '{event.obj.message['from_id']}'")
        self.db.update("Pending", "act", "'REGISTER_CODE'", f"WHERE user_id = '{event.obj.message['from_id']}'")
        self.db.connection.commit()
        self.bot.writeMsg(event.obj.message['from_id'], "Рад познакомиться. 🐉 Теперь введи шифр свое группы")

    def registerCode(self, event):
        # Регистрируем код
        self.db.update("Students", "code", f"'{event.obj.message['text']}'", f"WHERE user_id = '{event.obj.message['from_id']}'")
        self.db.update("Pending", "act", "NULL", f"WHERE user_id = '{event.obj.message['from_id']}'")
        self.db.connection.commit()
        self.bot.sendKeyboard(event.obj.message['from_id'], "main_sub_keyboard", "Я запомнил 🐉")
        self.setCurrentKeyboard(event, "main_sub_keyboard")

    ####


class ButtonHandler:
    """Обработчик нажатий на кнопки"""
    def __init__(self, bot, db):
        super().__init__()
        self.ButtonCommands = {
            #   Кнопки-сообщения
            "info_edit_call":    self.infoEditCall
        }

        self.bot = bot
        self.db = db

    #
    #   Кнопки-сообщения
    #

    def infoEditCall(self, event):
        self.bot.writeMsg(event.obj.user_id, "Введи свое полное имя")
        self.db.update("Pending", "act", "'REGISTER_NAME'", f"WHERE user_id = '{event.obj.user_id}'")
        self.db.connection.commit()

    #
    #   Обработчик
    #

    def checkCommand(self, event):
        print("Нажата кнопка")
        user_id = event.obj.user_id
        call = event.obj.payload.get('type')
        keyboard = self.getCurrentKeyboard(user_id)

        if not self.checkPending(user_id):
            if keyboard == None:
                self.bot.writeMsg(event.obj.user_id, "Пожалуйста, отправьте скриншот адмнистраторам.\nОшибка: клавиатура не привязана к бд") 
            elif self.bot.keyboards[keyboard].checkCommand(event):
                # Если функция была найдена и выполнена
                #self.refresh(user_id, keyboard)
                pass
            elif call in self.ButtonCommands:
                # Если это кнопка-сообщение
                self.ButtonCommands[call](event)
            else:
                # Такого эвента нет
                self.bot.writeMsg(event.obj.user_id, "Пожалуйста, отправьте скриншот адмнистраторам.\nОшибка: эвент не найден") 
        else:
            self.bot.writeMsg(user_id, "От Вас ожидается ввод данных.")

    def checkPending(self, user_id):
        self.db.select("Pending", "act", f"WHERE user_id='{user_id}'")
        res = self.db.cursor.fetchone()
        if res == None:
            return False
        elif res[0] != None:
            print(res)
            return True
        else: return False

    def setCurrentKeyboard(self, event, keyboard):
        """Установить клавиатуру в бд"""
        user_id = event.obj.user_id
        self.db.update("Students", "current_keyboard", f"'{keyboard}'", f"WHERE user_id='{user_id}'")
        self.db.connection.commit()

    def getCurrentKeyboard(self, user_id):
        keyboard = None
        self.db.select("Students", "current_keyboard", f"WHERE user_id='{user_id}'")
        res = self.db.cursor.fetchone()
        if res != None:
            keyboard = res[0]

        return keyboard

    def refresh(self, user_id, keyboard):
        self.bot.sendKeyboard(user_id, keyboard)

class Bot:
    """Бот"""
    def __init__(self, token, id):
        super().__init__()
        self.token = token
        self.id = id

        self.session = VkApi(token=token, api_version="5.124")
        self.vk = self.session.get_api()
        self.longpoll = VkBotLongPoll(self.session, group_id=id)

        self.keyboards = None

    def setKeyboards(self, keyboards):
        self.keyboards = keyboards

    def newUser(self, event):
        self.sendKeyboard(event.obj.user_id, "login_keyboard", "Добро пожаловать!\n Давай заполним твой профиль")

    def userExit(self, event):
        print(f"Пользователь {event.obj.user_id} запретил сообщения.")

    def writeMsg(self, user_id, message):
        self.session.method('messages.send', {'user_id': user_id, 'message': message, "random_id":get_random_id()})

    def attachmentMsg(self, user_id, attachment_type, attachment_id):
        ownid = "-199323686"
        self.session.method('messages.send', {'user_id': user_id, "random_id":get_random_id(), "attachment":f"{attachment_type}{ownid}_{attachment_id}"})

    def sendKeyboard(self, from_id, keyboard, text=""):
        if keyboard in self.keyboards:
            if text != "":
                self.vk.messages.send(
                            user_id=from_id,
                            random_id=get_random_id(),
                            peer_id=from_id,
                            keyboard=self.keyboards[keyboard].keyboard.get_keyboard(),
                            message=text
                            )
            else:
                self.vk.messages.send(
                            user_id=from_id,
                            random_id=get_random_id(),
                            peer_id=from_id,
                            keyboard=self.keyboards[keyboard].keyboard.get_keyboard(),
                            # ДУРОВ ПОЧЕМУ НЕЛЬЗЯ ОТПРАВИТЬ КЛАВИАТУРУ БЕЗ ТЕКСТА
                            # И ВЕРНИ СТЕНУ
                            message="Выполнено"
                            )
