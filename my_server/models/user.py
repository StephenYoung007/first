from models import Model


class User(Model):
    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def validate_login(self):
        u = User.find_by(username=self.username)
        # return self.username == 'gua' and self.password == '123'
        us=User.all()
        for u in us:
            if u.username==self.username and u.password ==self.password:
                return True
            else:
                return False


    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2