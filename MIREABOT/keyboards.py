from vk_api.keyboard import VkKeyboard, VkKeyboardColor

class KeyboardOneTime:
    def __init__(self):
        self.settings = dict(one_time=False, inline=False)
        self.keyboard = VkKeyboard(**self.settings)
        super().__init__()


class KeyboardAsMessage:
    def __init__(self):
        self.settings = dict(one_time=False, inline=True)
        self.keyboard = VkKeyboard(**self.settings)
        super().__init__()


class KeyboardLogin(KeyboardOneTime):
    def __init__(self):
        super().__init__()
        self.keyboard.add_callback_button(label='Заполнить профиль', color=VkKeyboardColor.POSITIVE, payload={"type": "login_call"})


# Главные, закрепляющиеся кнопки
class KeyboardMainNoSub(KeyboardOneTime):
    def __init__(self):
        super().__init__()
        self.keyboard.add_callback_button(label='Мой профиль', color=VkKeyboardColor.SECONDARY, payload={"type": "information_call"})       #payload={"type": "show_snackbar", "text": "Ты лох"})
        self.keyboard.add_line()
        self.keyboard.add_callback_button(label='Подписаться на новости', color=VkKeyboardColor.POSITIVE, payload={"type" : "sub_call"})
        self.keyboard.add_line()
        self.keyboard.add_callback_button(label='Мои записи', color=VkKeyboardColor.PRIMARY, payload={"type": "notes_call"})
        self.keyboard.add_line()
        # кнопка по открытию ВК-приложения
        #self.keyboard.add_callback_button(label='Style transfer', color=VkKeyboardColor.NEGATIVE, payload={"type": "open_app", "app_id": APP_ID, "owner_id": OWNER_ID, "hash": "anything_data_100500"})
        # кнопка переключения на 2ое меню
        self.keyboard.add_callback_button(label='Мини игра', color=VkKeyboardColor.PRIMARY, payload={"type": "game_call"})
        self.keyboard.add_line()
        self.keyboard.add_callback_button(label='Выход', color=VkKeyboardColor.NEGATIVE, payload={"type": "exit_call"})


class KeyboardMainWithSub(KeyboardOneTime):
    def __init__(self):
        super().__init__()
        self.keyboard.add_callback_button(label='Мой профиль', color=VkKeyboardColor.SECONDARY, payload={"type": "information_call"})       #payload={"type": "show_snackbar", "text": "Ты лох"})
        self.keyboard.add_line()
        self.keyboard.add_callback_button(label='Мои записи', color=VkKeyboardColor.PRIMARY, payload={"type": "notes_call"})
        self.keyboard.add_line()
        # кнопка по открытию ВК-приложения
        #self.keyboard.add_callback_button(label='Style transfer', color=VkKeyboardColor.NEGATIVE, payload={"type": "open_app", "app_id": APP_ID, "owner_id": OWNER_ID, "hash": "anything_data_100500"})
        # кнопка переключения на 2ое меню
        self.keyboard.add_callback_button(label='Мини игра', color=VkKeyboardColor.PRIMARY, payload={"type": "game_call"})
        self.keyboard.add_line()
        self.keyboard.add_callback_button(label='Отписаться от новостей', color=VkKeyboardColor.NEGATIVE, payload={"type" : "unsub_call"})
        self.keyboard.add_line()
        self.keyboard.add_callback_button(label='Выход', color=VkKeyboardColor.NEGATIVE, payload={"type": "exit_call"})


# Побочные кнопки в виде сообщений
class EditProfile(KeyboardAsMessage):
    def __init__(self):
        super().__init__()
        self.keyboard.add_callback_button(label='Редактировать профиль 📝', color=VkKeyboardColor.PRIMARY, payload={"type": "information_edit_call"})