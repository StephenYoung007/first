from models import Model
import time


class Topic(Model):
    def __init__(self, form):
        self.title = form.get('title', '')
        self.id = None
        self.views = 0
        self.content = form.get('content', '')
        self.ct = int(time.time())
        self.ut = self.ct
        self.user_id = form.get('user_id', '')
        self.board_id = int(form.get('board_id', -1))

    @classmethod
    def get(cls, id):
        m = cls.find_by(id = id)
        m.views += 1
        m.save()
        return m


    def replies(self):
        from .reply import Reply
        ms = Reply.find_all(topic_id = self.id)
        return ms


    def reply_delete(self):
        ms = self.replies()
        for m in ms:
            m.delete(m.id)


