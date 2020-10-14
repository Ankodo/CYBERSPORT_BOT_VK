from bot import *
from db import DataBase

# API
token = "a3f417d3ff86776d39d5ec5944f957cfe8621cb6e3dc7876565f9857028e4ca9ca193f97a40de6ef28414"
id = "199323686"

db = DataBase("students.db")

bot = Bot(token, id)
msgHandler = MessageHandler(bot, db)
buttHandler = ButtonHandler(bot, db)

Events = {
        VkBotEventType.MESSAGE_NEW : msgHandler.checkCommand,
        VkBotEventType.MESSAGE_ALLOW : bot.newUser,
        VkBotEventType.MESSAGE_DENY : bot.userExit,
        VkBotEventType.MESSAGE_EVENT : buttHandler.checkCommand
}

def checkEvent(event):
        print("НОВЫЙ ЭВЕНТ")
        print(event)
        print(event.type)
        if event.type in Events:
            print("ЭВЕНТ НАЙДЕН В СПИСКЕ")
            Events[event.type](event)

# Основной цикл
print("Бот запущен")
print(Events)
for event in bot.longpoll.listen():
    print(event)
    checkEvent(event)