from models import Model
from models.User import User


class Weibo(Model):
    def __init__(self, form):
        self.id = None
        self.content = form.get('content', '')

    def json(self):
        d = self.__dict__.copy()
        comments = [c.json() for c in self.comments()]
        d['comments'] = comments
        return d


class Comment(Model):
    def __init__(self, form):
        self.id = None
        self.content = form.get('content', '')
        self.weibo_id = int(form.get('weibo_id', -1))