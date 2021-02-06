#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

from tools.getpostconstructor import *

import re

class Group:
    """Методы для управления событиями группы"""
    def __init__(self, bot, db, miniapps_token):
        super().__init__()

        self.bot = bot
        self.db = db
        self.id = self.bot.id
        self.token = miniapps_token

        self.db.select("Tags")
        tags = self.db.cursor.fetchall()
        self.tagsname = list(map(lambda x: x[0], tags))
        self.tagspair = {}
        for item in tags:
            self.tagspair[item[0]] = item[1]

    def postEvent(self, event):
        """Получаем подписки по тэгам и передаем приложению"""
        post_tags = self.getPostTags(event)
        id = event.object.id
        lists = []
        for item in post_tags:
            lists.append(self.tagspair[item])

        self.repostByApp(id, lists)


    def postEventByUserList(self, event):
        """Составить список пользователей и разослать всем пост
        NOTE: устарело, юзай postEvent
        """
        post_tags = self.getPostTags(event)
        id = event.object.id
        users = []
        for tag in post_tags:
            self.db.select("Subscribes", "user_id", f"WHERE tag_id='{tag}'")
            sub_users = list(map(lambda x: x[0], self.db.cursor.fetchall()))
            for user in sub_users:
                if user not in users:
                    users.append(user)

        self.repostToList(id, users)

    def getPostTags(self, event):
        """Получить тэги записи"""
        text = event.object.text.rstrip()
        #   такие слова, что содержат решетку на первой позиции
        regex = "\#.\w+"
        words = re.findall(regex, text)
        # избавляемся от ссылки на группу (если есть), находим их в списке тэгов
        words = list(map(lambda x: x.split('@')[0], words))
        words = list(filter(lambda x: x in self.tagsname, words))
        return words

    def repostByApp(self, note_id, lists):
        data = {
            "message": {
                "attachment":f"wall-{self.id}_{note_id}"
                #"message": "вы все педики"
            },
            "list_ids":lists,
            "run_now":1
        }
        data = createJson(data)

        header = {"Content-Type":"application/json"}

        res = query(self.token, "POST", header, data)
        print(res)

    def repostToList(self, note_id, user_list):
        """Отправить подписанным студентам запись
        NOTE: отныне пользуемся приложением для рассылки - repostByApp
        """
        for user in user_list:
            self.bot.repostPost(user, note_id)