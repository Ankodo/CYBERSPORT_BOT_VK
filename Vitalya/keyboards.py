import vk_api, vk, data, info
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

def gameMenu(userId):
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Новая игра', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Продолжить', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Выход', color=VkKeyboardColor.PRIMARY)
    return keyboard

def game(userId):
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Налево', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Назад', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Направо', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Отметка', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('В меню', color=VkKeyboardColor.NEGATIVE)
    return keyboard

def mainMenu(userId):
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Профиль', color=VkKeyboardColor.PRIMARY)
    #keyboard.add_button('Подписки', color=VkKeyboardColor.PRIMARY)
    keyboard.add_openlink_button('Подписки', info.subs)
    keyboard.add_line()
    keyboard.add_button('Играть', color=VkKeyboardColor.POSITIVE)
    return keyboard

def subs(userId):
    keyboard = VkKeyboard(one_time=False)
    SUBS = data.getUserSUBS(userId)
    if SUBS[0] == '0':
        keyboard.add_button('Подписка на_что-то_там', color=VkKeyboardColor.NEGATIVE)
    else:
        keyboard.add_button('Подписка на_что-то_там', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Назад', color=VkKeyboardColor.PRIMARY)
    return keyboard

def profile(userId):
    keyboard = VkKeyboard(one_time=False)
    if data.getUserFIO(userId) == '0':
        keyboard.add_button('ФИО', color=VkKeyboardColor.NEGATIVE)
    else:
        keyboard.add_button('ФИО', color=VkKeyboardColor.POSITIVE)
    if data.getUserSTUD(userId) == '0':
        keyboard.add_button('Cтудак', color=VkKeyboardColor.NEGATIVE)
    else:
        keyboard.add_button('Cтудак', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Назад', color=VkKeyboardColor.PRIMARY)
    return keyboard

def back(userId):
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
    return keyboard