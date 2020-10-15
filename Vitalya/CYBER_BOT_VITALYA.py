import random, vk_api, vk
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

import info, data, keyboards, game
import os
import os.path

vk_session = vk_api.VkApi(token=info.token)
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
longpoll = VkBotLongPoll(vk_session, info.publicId)
vk = vk_session.get_api()
from vk_api.longpoll import VkLongPoll, VkEventType
Lslongpoll = VkLongPoll(vk_session)
Lsvk = vk_session.get_api()

try:
    os.mkdir('Game')
    os.mkdir('Game/Maps')
    os.mkdir('UsersInfo')
except:
    print('')
print('start')
for event in Lslongpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        if event.from_user:
            #Смотрим статус пользователя
            userStatus = data.getUserStatus(event.user_id)
            #Если пользователь в меню
            if userStatus == '0':
                var = ['Играть']# Кнопка которая отправляла пользователя в меню игры и меняла его статус на в меню игры
                if event.text in var:
                    data.setUserStatus(event.user_id, 'G0')#изменение статуса
                    Lsvk.messages.send(
                        user_id = event.user_id,
                        random_id = get_random_id(),
                        keyboard = keyboards.gameMenu(event.user_id).get_keyboard(),
                        message = 'Рад представить игру - Лабиринт Минотавра, правда Минотавр в отпуске, поэтому это почти обычный лабиринт.'
                                  'Ты можешь отметить путь на котором сейчас стоишь, отметка - 3 любых символа, можешь осмотреться в поисках отметок, а так же пойти в любую сторону.'
                                  'Удачи!'
                        )
                var = ['Профиль']#Кнопка отправляла в меню для записи студака и отправляла клавиатуру
                if event.text in var:
                    massage = ""
                    FIO = data.getUserFIO(event.user_id)
                    STUD = data.getUserSTUD(event.user_id)
                    if FIO != '0' and STUD != '0':
                        mmessage = ('Ты уже ввел свое ФИО и номер студака, можешь проверить \n'+
                                    'Номер студака:' + STUD + '\n' +
                                    'ФИО:' + FIO + '\n' +
                                    'Если есть ошибка, можешь исправить просто нажми на нужную кнопку')
                    elif FIO != '0' and STUD == '0':
                        mmessage = 'Введи номер своего студака, для ввода просто нажми кнопку студак'
                    elif FIO == '0' and STUD != '0':
                        mmessage = 'Введи свое ФИО, для ввода просто нажми кнопку ФИО'
                    else:
                        mmessage = 'Введи свое ФИО и номер студака, для ввода просто нажми на соответствующую кнопку'
                    Lsvk.messages.send(
                        user_id = event.user_id,
                        random_id = get_random_id(),
                        keyboard = keyboards.profile(event.user_id).get_keyboard(),
                        message = mmessage
                        )
                var = ['ФИО']#Кнопка для изменения фио
                if event.text in var:
                    data.setUserStatus(event.user_id, '2')
                    Lsvk.messages.send(
                        user_id = event.user_id,
                        random_id = get_random_id(),
                        keyboard = keyboards.back(event.user_id).get_keyboard(),
                        message = 'Теперь просто введи свое ФИО'
                        )
                var = ['Cтудак']#Кнопка для изменения студака
                if event.text in var:
                    data.setUserStatus(event.user_id, '1')
                    Lsvk.messages.send(
                        user_id = event.user_id,
                        random_id = get_random_id(),
                        keyboard = keyboards.back(event.user_id).get_keyboard(),
                        message = 'Теперь просто введи номер студака'
                        )
                var = ['Назад']#Кнопка кторая возвращала в меню
                if event.text in var:
                    Lsvk.messages.send(
                        user_id = event.user_id,
                        random_id = get_random_id(),
                        keyboard = keyboards.mainMenu(event.user_id).get_keyboard(),
                        message = 'Снова в меню.'
                    )
            elif userStatus[0] == 'G':###Проверка в игре ты или нет (все статусы начинающиеся с G относились к игре)
                if userStatus[1] == '0':# Статус G0 игровое меню
                    var = ['Новая игра']# Кнопка новая игра запрашивает сложность, меняет статус на G1 - ожидание сложности + отправляем клаву с отменой
                    if event.text in var:
                        data.setUserStatus(event.user_id, 'G1')
                        Lsvk.messages.send(
                            user_id = event.user_id,
                            random_id = get_random_id(),
                            keyboard = keyboards.back(event.user_id).get_keyboard(),
                            message = 'Введи сложность - число от 1 до 9'
                        )
                    var = ['Продолжить'] # Продолжает игру, если ести сейв, если нет запрашивает сложность для создания новой игры
                    if event.text in var:#
                        if game.haveSave(event.user_id):#Проверка наличия сейвов
                            data.setUserStatus(event.user_id, 'G2')
                            Lsvk.messages.send(
                                    user_id = event.user_id,
                                    random_id = get_random_id(),
                                    keyboard = keyboards.gameKeyboard(event.user_id).get_keyboard(),
                                    message = 'Сохранение загружено'
                                )
                        else:
                            data.setUserStatus(event.user_id, 'G1')#Статус ожидается сложность + отправляем клаву с отменой
                            Lsvk.messages.send(
                                user_id = event.user_id,
                                random_id = get_random_id(),
                                keyboard = keyboards.back(event.user_id).get_keyboard(),
                                message = 'Ошибка, сохранение не найдено, создание новой игры...\nВведи сложность - число от 1 до 9'
                            )
                    var = ['Выход']#Выход из игрового меню в обычное
                    if event.text in var:
                        data.setUserStatus(event.user_id, '0')
                        Lsvk.messages.send(
                            user_id = event.user_id,
                            random_id = get_random_id(),
                            keyboard = keyboards.mainMenu(event.user_id).get_keyboard(),
                            message = 'Снова в меню.'
                        )
                if userStatus[1] == '1':#Если ожидается сложность
                    var = ['Отмена']    #Если вместо сложности получили отмену, Возвращаем в игровое меню + меняем статус
                    if event.text in var:
                        data.setUserStatus(event.user_id, 'G0')
                        Lsvk.messages.send(
                            user_id = event.user_id,
                            random_id = get_random_id(),
                            keyboard = keyboards.gameMenu(event.user_id).get_keyboard(),
                            message = 'Действие отменено.'
                        )
                    else: #Проверка ввода, создаем новую игру, меняем клаву на игровую, статус на в игре
                        hard = int(event.text[0])
                        if hard>= 1 and hard<= 9:
                                game.newGame(event.user_id, hard)
                                data.setUserStatus(event.user_id, 'G2')
                                Lsvk.messages.send(
                                    user_id = event.user_id,
                                    random_id = get_random_id(),
                                    keyboard = keyboards.gameKeyboard(event.user_id).get_keyboard(),
                                    message = 'Ты в игре!'
                                )
                        else:
                            Lsvk.messages.send(
                                user_id = event.user_id,
                                random_id = get_random_id(),
                                message = 'Некоректный ввод, попробуй еще раз'
                                )
                if userStatus[1] == '2':#Если в игре
                    var = ['Назад', 'Налево' ,'Направо', 'Вперед']#Идем назад налево на право (Функция Move возвращает true когда вышел из лабиринта)
                    if event.text in var:
                        if game.move(event.user_id, var.index(event.text)):
                            data.setUserStatus(event.user_id, 'G0')
                            Lsvk.messages.send(
                                user_id = event.user_id,
                                random_id = get_random_id(),
                                keyboard = keyboards.gameMenu(event.user_id).get_keyboard(),
                                message = 'Поздравляем, ты вышел из лабиринта!'
                            )
                        else:
                            i = game.check(event.user_id)#Если после передвижения, не вышел из лабиринта осматриваемся, возвращает массив отметок
                            if len(i) == 2:
                                Lsvk.messages.send(
                                    user_id = event.user_id,
                                    random_id = get_random_id(),
                                    keyboard = keyboards.gameKeyboard(event.user_id).get_keyboard(),
                                    message = 'Ты пошел к следующей развилке и осмотрелся в поисках отметок\n' +
                                            'Cпереди:' + i[1] +
                                            '\nПод ногами:' + i[0]
                                    )
                            if len(i) == 3:
                                Lsvk.messages.send(
                                    user_id = event.user_id,
                                    random_id = get_random_id(),
                                    keyboard = keyboards.gameKeyboard(event.user_id).get_keyboard(),
                                    message = 'Ты пошел к следующей развилке и осмотрелся в поисках отметок\n' +
                                            'Слева:' + i[1] +
                                            '\nСправа:' + i[2] +
                                            '\nПод ногами:' + i[0]
                                    )
                            if len(i) == 4:
                                Lsvk.messages.send(
                                    user_id = event.user_id,
                                    random_id = get_random_id(),
                                    keyboard = keyboards.gameKeyboard(event.user_id).get_keyboard(),
                                    message = 'Ты пошел к следующей развилке и осмотрелся в поисках отметок\n' +
                                            'Слева:' + i[1] +
                                            '\nСпереди:' + i[2] +
                                            '\nСправа:' + i[3] +
                                            '\nПод ногами:' + i[0]
                                    )
                    var = ['Отметка']#Меняем статус На ожидание отметки
                    if event.text in var:
                        data.setUserStatus(event.user_id, 'G3')
                        Lsvk.messages.send(
                                user_id = event.user_id,
                                random_id = get_random_id(),
                                keyboard = keyboards.back(event.user_id).get_keyboard(),
                                message = 'Введи отметку (3 символа)'
                            )
                    var = ['В меню']#Просто возвращаем в игровое меню
                    if event.text in var:
                        data.setUserStatus(event.user_id, 'G0')
                        Lsvk.messages.send(
                                user_id = event.user_id,
                                random_id = get_random_id(),
                                keyboard = keyboards.gameMenu(event.user_id).get_keyboard(),
                                message = 'Игра сохранена.'
                            )

                if userStatus[1] == '3':#Если ожидается отметка
                    var = ['Отмена']#Ели отменяем, возврат к игре
                    if event.text in var:
                        data.setUserStatus(event.user_id, 'G2')
                        Lsvk.messages.send(
                            user_id = event.user_id,
                            random_id = get_random_id(),
                            keyboard = keyboards.gameKeyboard(event.user_id).get_keyboard(),
                            message = 'Действие отменено.'
                        )
                    else:#В противном случае записываем отметку
                        game.addPrint(event.user_id, event.text)
                        data.setUserStatus(event.user_id, 'G2')
                        Lsvk.messages.send(
                            user_id = event.user_id,
                            random_id = get_random_id(),
                            keyboard = keyboards.gameKeyboard(event.user_id).get_keyboard(),
                            message = 'Ты оставил отметку:' + event.text
                            )
                #Примечание к игре, добавлю функцию которая возвращает количество путей в перекрестке 0- тупик 3 Перекресток крестом (Нужно для выбора правильной клавиатуры и тп)

            #Если пользователь отсуцтвует в бд, добавляем в бд
            elif userStatus == '-1':
                data.addUser(event.user_id)
                Lsvk.messages.send(
                    user_id = event.user_id,
                    random_id = get_random_id(),
                    keyboard = keyboards.mainMenu(event.user_id).get_keyboard(),
                    message = 'Поздравляю, теперь ты с нами!'
                    )
            #Если пользователь вводит свой студак
            elif userStatus == '1':
                var = ['Отмена']#Отмена 
                if event.text in var:
                    data.setUserStatus(event.user_id, '0')
                    Lsvk.messages.send(
                        user_id = event.user_id,
                        random_id = get_random_id(),
                        keyboard = keyboards.profile(event.user_id).get_keyboard(),
                        message = 'Отмена ввода данных.'
                    )
                else:
                    data.setUserSTUD(event.user_id, event.text.replace('\n', ''))
                    Lsvk.messages.send(
                    user_id = event.user_id,
                    random_id = get_random_id(),
                    keyboard = keyboards.profile(event.user_id).get_keyboard(),
                    message = 'Новый номер студака сохранен.'
                    )
            #Если пользователь вводит свое ФИО
            elif userStatus == '2':
                var = ['Отмена']#Отмена
                if event.text in var:
                    data.setUserStatus(event.user_id, '0')
                    Lsvk.messages.send(
                    user_id = event.user_id,
                    random_id = get_random_id(),
                    keyboard = keyboards.profile(event.user_id).get_keyboard(),
                    message = 'Отмена ввода данных.'
                    )
                else:
                    data.setUserFIO(event.user_id, event.text.replace('\n', ''))
                    Lsvk.messages.send(
                    user_id = event.user_id,
                    random_id = get_random_id(),
                    keyboard = keyboards.profile(event.user_id).get_keyboard(),
                    message = 'ФИО изменено.'
                    )