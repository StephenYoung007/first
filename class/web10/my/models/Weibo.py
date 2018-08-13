from models import Model
from models.Comment import Comment


class Weibo(Model):
    def __init__(self, form, user_id=-1):
        self.id = form.get('id', None)
        self.content = form.get('content', '')
        self.user_id = form.get('user_id', user_id)


    def commet(self):
        return Comment.find_all(weibo_id=self.id)