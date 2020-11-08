import re

class Group:
    """Методы для управления событиями группы"""
    def __init__(self, bot, db):
        super().__init__()

        self.bot = bot
        self.db = db

        self.db.select("Tags")
        self.tags = list(map(lambda x: x[0], self.db.cursor.fetchall()))


    def postEvent(self, event):
        post_tags = self.getPostTags(event)
        id = event.obj.id
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
        text = event.obj.text.rstrip()
        #   такие слова, что содержат решетку на первой позиции
        regex = "\#.\w+"
        words = re.findall(regex, text)
        # избавляемся от ссылки на группу, находим их в списке тэгов
        words = list(map(lambda x: x.split('@')[0], words))
        words = list(filter(lambda x: x in self.tags, words))
        return words

    def repostToList(self, note_id, user_list):
        """Отправить подписанным студентам запись"""
        for user in user_list:
            self.bot.repostPost(user, note_id)