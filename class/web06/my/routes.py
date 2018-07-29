from utils import (
    log,
    redirect,
    response_with_headers,
)
from models.Message import Message
from models.User import User


session = {
    'session id' : {
        'username' : 'gua',
        '过期时间' : '2.22 21:00:00',
    }
}


import random


def random_str():
    seed = 'abcdefjsad89234hdsfkljasdkjghigaksldf89weru'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


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


def  current_user(request):
    session_id = request.cookies.get('user', '')
    username = session.get(session_id, '游客')
    # username = request.cookies.get('user', '【游客】')
    return username


def route_index(request):
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    body = templates('index.html')
    username = current_user(request)
    body = body.replace('{{username}}', username)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')




def route_login(request):
    # header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    headers = {
        'Content-Type' : 'text/html',
    }
    username = current_user(request)
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        # log('type of u', type(u))
        if u.valid_login():
            session_id = random_str()
            session[session_id] = u.username
            log(session)
            headers['Set-Cookie'] = 'user={}'.format(session_id)
            result = '登录成功'
        else:
            result = '用户名或密码错误'
    else:
        result = ''
    body = templates('login.html')
    body = body.replace('{{result}}', result)
    body = body.replace('{{username}}', username)
    header = response_with_headers(headers)
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
    username = current_user(request)
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

def route_test(request):
    username = current_user(request)
    if username == 'gua':
        return redirect('/')
    else:
        return  redirect('http://python.stephenyoung.top')

route_dict = {
    '/' : route_index,
    '/login' : route_login,
    '/register' : route_register,
    '/messages' : route_message,
    '/test' : route_test,
}