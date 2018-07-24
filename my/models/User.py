from models import Model

class User(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        if self.id is not None:
            self.id = int(self.id)
        self.username = form.get('username', '')
        self.password = form.get('password', '')


    def valid_login(self):
        # return self.username == 'gua' and self.password == '123'
        u = self.find_by(username=self.username)
        return u and u.password == self.password


    def valid_register(self):
        if len(self.username) < 3:
            return False
        else:
            return True