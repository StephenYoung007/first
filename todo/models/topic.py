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