import socket
import urllib.parse
import time
import json


def log(*args, **kwargs):
    '''
    用于格式化输出的函数
    '''
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    print(dt, *args, **kwargs)


class Request(object):
    '''
    用于保存请求返回的类
    '''
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''


    def form(self):
        '''
        用于将body保存为字典格式并返回
        '''
        body = urllib.parse.unquote(self.body)
        args = body.split('&')
        f= {}
        for arg in args:
            k,v = arg.split('=')
            f[k] = v
        return f



request = Request()


def load(path):
    '''
    从一个文件中载入list或者字典
    :param path: 载入路径
    :return: 字典或列表
    '''
    with open(path, 'r', encoding='utf-8') as f:
        return json.loads(f.read())


def save(data, path):
    '''
    用于把一个list或者字典保存到path路径
    :param data: 字典或列表
    :param path: 路径
    :return: 写入
    '''
    s =json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(s)


'''
model是存储数据的基类，包括User、Message等数据
'''
class model(object):
    '''
    @classmethod表示这是一个类方法，类方法的调用方式是类名.类方法
    when be called, classmethod will also creat an object
    self代表的普通方法，必须通过类的实例调用，类似于c++中的通过对象调用
    '''
    @classmethod
    def db_path(cls):
        '''
        传入cls
        :return:以classname命名的路径对象
        '''
        classname = cls.__name__
        path = 'db/{}.txt'.format(classname)
        return path


    @classmethod
    def new(cls, form):
        '''
        传入form方法，得到cls的body字典
        :param form:
        :return: 相当于User（form)或者Message(form)
        '''
        m = cls(form)
        log('type of m', type(m))
        return m


    @classmethod
    def all(cls):
        '''
        得到一个类的所有存储的实例
        :return:
        '''
        path = cls.db_path()
        models = load(path)
        ms = [cls.new(m) for m in models]
        return ms


    def save(self):
        models = self.all()
        models.append(self)
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)

    @classmethod
    def find_by(cls, **kwargs):
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        for m in all:
            if v == m.__dict__[k]:
                return m
        return None


    def __repr__(self):
        """
        这是一个 魔法函数
        不明白就看书或者 搜
        当你调用 str(o) 的时候
        实际上调用了 o.__str__()
        当没有 __str__ 的时候
        就调用 __repr__
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)





    # @classmethod
    # def find_by(cls, **kwargs):
    #     k, v = '', ''
    #     for key, value in kwargs.items():
    #         k, v = key, value
    #         all = cls.all()
    #     for m in all:
    #         if v == m.__dict__[k]:
    #             return m
    #     return None



class User(model):
    def __init__(self, form):
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


class Message(model):
    def __init__(self, form):
        self.author = form.get('author', '')
        self.message = form.get('message', '')


def parsed_path(path):
    index = path.find('?')
    if index == -1:
        path, query = path, {}
    else:
        query = {}
        path, query_string = path.split('?')
        args = query_string.split('&')
        for arg in args:
            k, v = arg.split('=')
            query[k] = v
    return path, query


def route_static(request):
    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
        img = header + b'\r\n' + f.read()
        return img


def templates(name):
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def route_index(request):
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    body = templates('index.html')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_login(request):
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        # log('type of u', type(u))
        if u.valid_login():
            result = '登录成功'
        else:
            result = '登录失败'
    else:
        result = ''
    body = templates('login.html')
    body = body.replace('{{result}}', result)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_register(request):
    header = 'HTTP/1.1 210 FUCK OK\r\nContent-Type: text/html\r\n'
    if request.method ==  'POST':
        form = request.form()
        u = User.new(form)
        if u.valid_register():
            u.save()
            result = '注册成功<br> <pre>{}</pre>'.format(User.all())
        else:
            result = '用户名或密码长度必须大于2'
        print(type(result))
    else:
        result = ''
    body = templates('register.html')
    body = body.replace('{{result}}', result)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


message_list = []


def route_message(request):
    if request.method == 'POST':
        form = request.form()
        msg = Message.new(form)
        msg.save()
        message_list.append(msg)
    header = 'HTTP/1.1 200 FUCK\r\nContent-Type: text/html\r\n'
    body = templates('html_basic.html')
    msgs = '<br/>'.join([str(m) for m in message_list])
    body = body.replace('{{messages}}', msgs)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')



route_dict = {
    '/' : route_index,
    '/login' : route_login,
    '/register' : route_register,
    '/messages' : route_message,
}


def error(request, code=404):
    e = {
        404 : b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def response_for_path(path):
    path, query = parsed_path(path)
    request.path = path
    request.query = query
    r = {
        '/static' : route_static,
    }
    r.update(route_dict)
    # log('r', r, path, query)
    response = r.get(path, error)
    return response(request)


def run(host='', port=3000):
    log('start at','{}:{}'.format(host, port))
    with socket.socket() as s:
        s.bind((host, port))
        while True:
            s.listen(5)
            connection, address = s.accept()
            r = connection.recv(1024)
            r = r.decode('utf-8')
            # log('r', r)
            if len(r.split()) < 2:
                continue
            path = r.split()[1]
            # print('response : \n', r)
            request.method = r.split()[0]
            request.body = r.split('\r\n\r\n', 1)[1]
            # log('path', path)
            response = response_for_path(path)
            # log(type(response), response)
            # print('request.method:', request.method, '\r\nrequest.path:', request.path, '\r\nrequest.body:', request.body, '\r\nrequest.query:', request.query)
            connection.sendall(response)
            connection.close()







if __name__ == '__main__':
    conifg = dict(
        host = '',
        port = 3000
    )
    run(**conifg)