import socket
import urllib.parse
import time
import json

def log(*args, **kwargs):
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    print(dt, *args, **kwargs)


class Request(object):
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''


    def form(self):
        body = urllib.parse.unquote(self.body)
        args = body.split('&')
        f= {}
        for arg in args:
            k,v = arg.split('=')
            f[k] = v
        return f



request = Request()


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.loads(f.read())


def save(data, path):
    s =json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(s)



class model(object):
    @classmethod
    def db_path(cls):
        classname = cls.__name__
        path = 'db/{}.txt'.format(classname)
        return path


    @classmethod
    def new(cls, form):
        m = cls(form)
        return m


    @classmethod
    def all(cls):
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


class User(model,form):
    def __init__(self):
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def valid_login(self):
        return self.username == 'gua' and self.password == '123'




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




route_dict = {
    '/' : route_index,
    '/login' : route_login
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
    log('r', r, path, query)
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
            if len(r.split()) < 2:
                continue
            path = r.split()[1]
            print('response : \n', r)
            request.method = r.split()[0]
            request.body = r.split('\r\n\r\n', 1)[1]
            log('path', path)
            response = response_for_path(path)
            print('request.method:', request.method, '\r\nrequest.path:', request.path, '\r\nrequest.body:', request.body, '\r\nrequest.query:', request.query)
            connection.sendall(response)
            connection.close()







if __name__ == '__main__':
    conifg = dict(
        host = '',
        port = 3000
    )
    run(**conifg)