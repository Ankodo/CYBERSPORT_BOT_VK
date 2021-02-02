# Потому что питон по умолчанию не копирует, а ссылается на объект, мда
from copy import deepcopy

from vk_api.keyboard import VkKeyboard, VkKeyboardColor

#
# Главные блоки
#

class KeyBoard:
    def __init__(self, bot, db):
        self.keyboard = None
        self.self_building = False
        self.calls = {}
        self.bot = bot
        self.db = db

    def checkCommand(self, event):
        """Проверить на наличие команды в своем списке"""
        call = event.obj.payload.get('type')
        if call in self.calls:
            self.calls[call](event)
            return True
        else:
            return False


class KeyboardMessage(KeyBoard):
    """Клавиатура-сообщение"""
    def __init__(self, bot, db):
        super().__init__(bot, db)
        settings = dict(one_time=False, inline=True)
        self.keyboard = VkKeyboard(**settings)


class KeyboardMain(KeyBoard):
    """Фиксированная клавиатура"""
    def __init__(self, bot, db):
        super().__init__(bot, db)
        settings = dict(one_time=False, inline=False)
        self.keyboard = VkKeyboard(**settings)

#
#  Главное меню
# 


class KeyboardMainMenu(KeyboardMain):
    """Главный блок для главного меню"""
    def __init__(self, bot, db):
        super().__init__(bot, db)
        self.calls = {
            "info_call" : self.infoCall,
            "notes_call" : self.notesCall,
            "game_call" : self.gameCall,
            "tags_call" : self.tagsCall,
            "exit_call" : self.exitCall
        }
        self.name = "main_keyboard"

        self.keyboard.add_callback_button(label='Мой профиль', color=VkKeyboardColor.POSITIVE, payload={"type": "info_call", "keyboard": self.name})       #payload={"type": "show_snackbar", "text": "Ты лох"})
        self.keyboard.add_line()
        self.keyboard.add_callback_button(label='Мои записи', color=VkKeyboardColor.PRIMARY, payload={"type": "notes_call", "keyboard": self.name})
        self.keyboard.add_line()
        self.keyboard.add_callback_button(label='Мини игра', color=VkKeyboardColor.PRIMARY, payload={"type": "game_call", "keyboard": self.name})
        self.keyboard.add_line()
        # self.keyboard.add_callback_button(label='Управление подписками на сообщения', payload={"type": 'tags_call', "keyboard": self.name})
        # self.keyboard.add_line()
        self.keyboard.add_openlink_button('Управление подписками на сообщения', 'https://vk.com/testbotmemrea?w=app5748831_-199323686')
        #self.keyboard.add_line()
        #self.keyboard.add_callback_button(label='Выход', color=VkKeyboardColor.NEGATIVE, payload={"type": "exit_call", "keyboard": self.name})

    def infoCall(self, event):
        """Событие вызова профиля пользователя"""
        user_id = event.obj.user_id
        self.db.select("Students", "user_id", f"WHERE user_id='{user_id}'")
        res1 = self.db.cursor.fetchone()
        self.db.select("Students", "full_name", f"WHERE user_id='{user_id}'")
        res2 = self.db.cursor.fetchone()
        self.db.select("Students", "code", f"WHERE user_id='{user_id}'")
        res3 = self.db.cursor.fetchone()

        if res1 != None and res2 != None and res3 != None:
            text = f"""
id = {res1[0]}
Имя - {res2[0]}
Группа - {res3[0]}
"""
        self.bot.sendKeyboard(user_id, "inforamtion_edit_keyboard", text)
        self.bot.sendKeyboard(user_id, self.name)

    def notesCall(self, event):
        """Событие вызова записей пользователя"""
        user_id = event.obj.user_id
        self.bot.sendKeyboard(user_id, self.name, "Тут что-то будет про записи 🤔🤔🤔")

    def gameCall(self, event):
        """Событие вызова игры"""
        user_id = event.obj.user_id
        self.bot.sendKeyboard(user_id, "main_game_start", "Запускаю игру", True)

    def tagsCall(self, event):
        """Событие вызова подписок"""
        """Устарело. Направляй в приложение рассылки."""
        user_id = event.obj.user_id
        self.bot.sendKeyboard(user_id, "main_tags_keyboard", "Открываю Ваши подписки", True, True)

    def exitCall(self, event):
        """Выход пользователя из системы"""
        self.bot.sendKeyboard(event.obj.user_id, "main_login_keyboard", "Удачи! 🐉", True)



#
#   Клавиатура для управления
#   Клавиатура самособирается - это статичный класс
#


class KeyboardMainTagsManager(KeyboardMain):
    """Ну типа миниприложения круче, поэтому я все это зря делал, конечно!"""
    def __init__(self, bot, db):
        super().__init__(bot, db)
        self.self_building = True
        self.name = "main_tags_keyboard"

        self.calls = {
            "sub_call" : self.subCall,
            "unsub_call" : self.unSubCall,
            "back_call" : self.backCall
        }

        self.db.select("Tags")
        self.tags = list(map(lambda x: x[0], self.db.cursor.fetchall()))

    def build(self, user_id):
        """Событие получения подписок"""
        keyboard = deepcopy(self.keyboard)
        self.db.select("Subscribes", "tag_id", f"WHERE user_id='{user_id}'")
        sub_tags = list(map(lambda x: x[0], self.db.cursor.fetchall()))

        for tag in self.tags:
            if tag not in sub_tags:
                keyboard.add_callback_button(label=f"Подписка на {tag}",
                color=VkKeyboardColor.POSITIVE, payload={"type": "sub_call", "tag": f"{tag}", "keyboard": self.name})
                keyboard.add_line()

        for tag in sub_tags:
            keyboard.add_callback_button(label=f"Отписка от {tag}",
             color=VkKeyboardColor.PRIMARY, payload={"type": "unsub_call", "tag": f"{tag}", "keyboard": self.name})
            keyboard.add_line()

        keyboard.add_callback_button(label=f"В меню",
                color=VkKeyboardColor.NEGATIVE, payload={"type": "back_call", "keyboard": self.name})

        return keyboard

    def subCall(self, event):
        """Подписаться на тэг"""
        user_id = event.obj.user_id
        tag = event.obj.payload.get('tag')
        message = f"Вы подписались на {tag}"

        self.db.select("Subscribes", "tag_id", f"WHERE user_id='{user_id}'")
        sub_tags = list(map(lambda x: x[0], self.db.cursor.fetchall()))

        if tag not in sub_tags:
            self.db.insert("Subscribes", "user_id, tag_id", f"'{user_id}', '{tag}'")
            self.db.connection.commit()
        else:
            # А вдруг баг
            message = f"Вы уже подписаны на {tag}"

        self.bot.sendKeyboard(user_id, "main_tags_keyboard", message, True, True)

    def unSubCall(self, event):
        """Отписаться от тэга"""
        user_id = event.obj.user_id
        tag = event.obj.payload.get('tag')
        message = f"Вы отписались от {tag}"

        self.db.select("Subscribes", "tag_id", f"WHERE user_id='{user_id}'")
        sub_tags = list(map(lambda x: x[0], self.db.cursor.fetchall()))

        if tag in sub_tags:
            self.db.delete("Subscribes", f"user_id='{user_id}' AND tag_id='{tag}'")
            self.db.connection.commit()
        else:
            # А вдруг баг
            message = f"Вы уже отписались от {tag}"

        
        self.bot.sendKeyboard(user_id, "main_tags_keyboard", message, True, True)

    def backCall(self, event):
        """Событие возврата в меню"""
        user_id = event.obj.user_id
        self.bot.sendKeyboard(user_id, "main_keyboard", "Возвращаю в меню", True)


#
#   Игра
#

class GameKeyboardMenu(KeyboardMain):
    """Клавиатура для игры"""
    def __init__(self, bot, db, game):
        super().__init__(bot, db)

        self.calls = {
            "new_call" : self.newGameCall,
            "continue_call" : self.continueCall,
            "back_call" : self.backCall
        }

        self.game  = game
        self.name = "main_game_start"
        self.keyboard.add_callback_button(label='Новая игра', color=VkKeyboardColor.POSITIVE, payload={"type" : "new_call", "keyboard": self.name})
        self.keyboard.add_line()
        self.keyboard.add_callback_button(label='Продолжить игру', color=VkKeyboardColor.PRIMARY, payload={"type": "continue_call", "keyboard": self.name})
        self.keyboard.add_line()
        self.keyboard.add_callback_button(label='В меню', color=VkKeyboardColor.NEGATIVE, payload={"type": "back_call", "keyboard": self.name})

    def newGameCall(self, event):
        """Событие новой игры"""
        user_id = event.obj.user_id
        self.bot.sendKeyboard(user_id, "main_game", "Начинаю игру", True)
        self.game.gameManager(user_id, "newgame")

    def continueCall(self, event):
        """Событие продолжения игры"""
        user_id = event.obj.user_id
        self.db.select("GameMaze", "m_coords", f"WHERE user_id='{user_id}'")
        if self.db.cursor.fetchone() != None:
            self.bot.sendKeyboard(user_id, "main_game", "Продолжаю игру", True)
        else:
            self.bot.sendKeyboard(user_id, "main_game_start", "Сохраненной игры не найдено", True)

    def backCall(self, event):
        """Событие возврата в меню"""
        user_id = event.obj.user_id
        self.bot.sendKeyboard(user_id, "main_keyboard", "Возвращаю в меню", True)


class GameKeyboard(KeyboardMain):
    """Клавиатура для игры"""
    def __init__(self, bot, db, game):
        super().__init__(bot, db)

        self.calls = {
            "forward_call" : self.forwardCall,
            "left_call" : self.leftCall,
            "right_call" : self.rightCall,
            "stay_call" : self.stayCall,
            "back_call" : self.backCall,
            "menu_call" : self.menuCall
        }

        self.game  = game
        self.name = "main_game"
        self.keyboard.add_callback_button(label='Вверх', color=VkKeyboardColor.POSITIVE, payload={"type" : "forward_call", "keyboard": self.name})
        self.keyboard.add_line()
        self.keyboard.add_callback_button(label='Налево', color=VkKeyboardColor.PRIMARY, payload={"type": "left_call", "keyboard": self.name})
        self.keyboard.add_callback_button(label='Направо', color=VkKeyboardColor.PRIMARY, payload={"type": "right_call", "keyboard": self.name})
        self.keyboard.add_line()
        self.keyboard.add_callback_button(label='Вниз', color=VkKeyboardColor.POSITIVE, payload={"type": "back_call", "keyboard": self.name})
        self.keyboard.add_line()
        self.keyboard.add_callback_button(label='Прислушаться', color=VkKeyboardColor.PRIMARY, payload={"type": "stay_call", "keyboard": self.name})
        self.keyboard.add_line()
        self.keyboard.add_callback_button(label='В меню', color=VkKeyboardColor.NEGATIVE, payload={"type": "menu_call", "keyboard": self.name})

    def forwardCall(self, event):
        user_id = event.obj.user_id
        self.bot.sendKeyboard(user_id, "main_game", "Идем вверх")
        self.game.gameManager(user_id, "move", "up")

    def leftCall(self, event):
        user_id = event.obj.user_id
        self.bot.sendKeyboard(user_id, "main_game", "Идем налево")
        self.game.gameManager(user_id, "move", "left")

    def rightCall(self, event):
        user_id = event.obj.user_id
        self.bot.sendKeyboard(user_id, "main_game", "Идем направо")
        self.game.gameManager(user_id, "move", "right")

    def stayCall(self, event):
        user_id = event.obj.user_id
        self.bot.sendKeyboard(user_id, "main_game", "Остаемся на месте")
        self.game.gameManager(user_id, "stay")

    def backCall(self, event):
        user_id = event.obj.user_id
        self.bot.sendKeyboard(user_id, "main_game", "Идем вниз")
        self.game.gameManager(user_id, "move", "down")

    def menuCall(self, event):
        user_id = event.obj.user_id
        self.bot.sendKeyboard(user_id, "main_game_start", "Возвращаю в меню", True)

#
# Авторизация
#

class KeyboardLogin(KeyboardMain):
    """Кнопка входа"""
    def __init__(self, bot, db):
        super().__init__(bot, db)
        self.name = "main_login_keyboard"
        self.calls = {
            "login_call" : self.loginCall,
        }
        self.keyboard.add_callback_button(label='Авторизация', color=VkKeyboardColor.POSITIVE, payload={"type": "login_call", "keyboard": self.name})

    def loginCall(self, event):
        """Событие вызова авторизации"""
        # NOTE: Лучше заменить на MINI APPS
        user_id = event.obj.user_id
        self.db.select("Students", "user_id", f"WHERE user_id='{user_id}' AND full_name IS NOT NULL")
        res = self.db.cursor.fetchone()
        if res == None:
            self.bot.writeMsg(user_id, "Для начала введи свое полное имя")
            self.db.insert("Pending", "user_id, act", f"'{user_id}', 'REGISTER_NAME'")
            self.db.connection.commit()
        else:
            self.bot.sendKeyboard(user_id, "main_keyboard", "Вы успешно авторизовались!", True)


#
#   Редактирование профиля
#


class KeyboardMainEditProfile(KeyboardMain):
    """Клавиатура с кнопками для редактирования профиля"""
    def __init__(self, bot, db):
        super().__init__(bot, db)
        self.name = "main_info_edit_keyboard"
        self.calls = {
            "info_edit_name_call" : self.editNameCall,
            "info_edit_group_call" : self.editGroupCall,
            "to_menu_call" : self.toMenuCall
        }
        self.keyboard.add_callback_button(label='Редактировать имя', color=VkKeyboardColor.PRIMARY , payload={"type": "info_edit_name_call", "keyboard": self.name})
        self.keyboard.add_line()
        self.keyboard.add_callback_button(label='Редактировать группу', color=VkKeyboardColor.PRIMARY , payload={"type": "info_edit_group_call", "keyboard": self.name})
        self.keyboard.add_line()
        self.keyboard.add_callback_button(label='В меню', color=VkKeyboardColor.PRIMARY , payload={"type": "to_menu_call", "keyboard": self.name})

    def editNameCall(self, event):
        """Редактирование имени пользователя"""
        self.bot.sendKeyboard(event.obj.user_id, "cancel_keyboard", "Введи свое полное имя")
        self.db.update("Pending", "act", "'EDIT_NAME'", f"WHERE user_id = '{event.obj.user_id}'")
        self.db.connection.commit()

    def editGroupCall(self, event):
        """Редактирование группы пользователя"""
        self.bot.sendKeyboard(event.obj.user_id, "cancel_keyboard", "Введи шифр группы")
        self.db.update("Pending", "act", "'EDIT_CODE'", f"WHERE user_id = '{event.obj.user_id}'")
        self.db.connection.commit()

    def toMenuCall(self, event):
        self.bot.sendKeyboard(event.obj.user_id, "main_keyboard", "Возвращаю в меню", True)



#
# Побочные кнопки в виде сообщений
# NOTE: Так как можно привязать только одну ГЛАВНУЮ клавиатуру,
# Функции для кнопок-сообщений будут реализованы в классе 
# ButtonHandler. Либо можно функции вынести в отдельный класс,
# и передавать payload туда
#


class KeyboardEditProfile(KeyboardMessage):
    def __init__(self, bot, db):
        super().__init__(bot, db)
        self.keyboard.add_callback_button(label='Редактировать профиль 📝', color=VkKeyboardColor.PRIMARY, payload={"type": "info_edit_call", "keyboard": "oneline"})

class CancelLastInput(KeyboardMessage):
    def __init__(self, bot, db):
        super().__init__(bot, db)
        self.keyboard.add_callback_button(label='Отменить', color=VkKeyboardColor.NEGATIVE, payload={"type": "cancel_call", "exception": "1", "keyboard": "oneline"})