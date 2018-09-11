from models import Model
import time


class Board(Model):
    def __init__(self, form):
        self.title = form.get('title', '')
        self.id = None
        self.ct = int(time.time())
        self.ut = self.ct