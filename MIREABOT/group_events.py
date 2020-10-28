class Group:
    """Методы для управления событиями группы"""
    def __init__(self, bot, db):
        super().__init__()

        self.bot = bot
        self.db = db

    def repostToEverybody(self, event):
        """Отправить всем подписанным студентам запись"""
        self.db.select("Students", "user_id", "WHERE subscribed = '1'")
        result = self.db.cursor.fetchall()
        for item in result:
            self.bot.repostPost(item[0], event.obj.id)