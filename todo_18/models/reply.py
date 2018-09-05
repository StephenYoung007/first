from models import Model
import time

class Reply(Model):
    def __init__(self, form):
        self.id = None
        self.content = form.get('content', '')
        self.ct = time.time()
        self.ut = self.ct
        self.topic_id = form.get('topic_id', -1)