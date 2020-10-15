import vk_api, vk, data, info, game
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

def profile(userId):#Клавиатура с записью данныхБ меняетсю цвет
    keyboard = VkKeyboard(one_time=False)
    if data.getUserFIO(userId) == '0':
        keyboard.add_button('ФИО', color=VkKeyboardColor.NEGATIVE)
    else:
        keyboard.add_button('ФИО', color=VkKeyboardColor.POSITIVE)
    if data.getUserSTUD(userId) == '0':
        keyboard.add_button('Cтудак', color=VkKeyboardColor.NEGATIVE)
    else:
        keyboard.add_button('Cтудак', color=VkKeyboardColor.POSITIVE)
    if data.getUserGROUP(userId) == '0':
        keyboard.add_button('Группа', color=VkKeyboardColor.NEGATIVE)
    else:
        keyboard.add_button('Группа', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Назад', color=VkKeyboardColor.PRIMARY)
    return keyboard

def gameKeyboard(userId): #Игровая клава с вариативным количеством кнопок
    keyboard = VkKeyboard(one_time=False)
    a = game.getWey(userId)#Функция возвращает количество ответвлений в перекрестке от 2-4
    if a == 2:
        keyboard.add_button('Вперед', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Назад', color=VkKeyboardColor.POSITIVE)
    elif a == 3:
        keyboard.add_button('Налево', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Назад', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Направо', color=VkKeyboardColor.POSITIVE)
    elif a == 4:
        keyboard.add_button('Вперед', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Налево', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Назад', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Направо', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Отметка', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('В меню', color=VkKeyboardColor.NEGATIVE)
    return keyboard

def gameMenu(userId):#Игровое меню
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Новая игра', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Продолжить', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Выход', color=VkKeyboardColor.PRIMARY)
    return keyboard

def mainMenu(userId):#Главное Меню
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Профиль', color=VkKeyboardColor.PRIMARY)
    #keyboard.add_button('Подписки', color=VkKeyboardColor.PRIMARY)
    keyboard.add_openlink_button('Подписки', info.subs)#Ссылка на подписки, можно просто вставит т.к. используется 1 раз, я прост в отдельный файл засунул
    keyboard.add_line()
    keyboard.add_button('Играть', color=VkKeyboardColor.POSITIVE)
    return keyboard

def back(userId):#Отмена
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Отмена', color=VkKeyboardColor.NEGATIVE)
    return keyboard