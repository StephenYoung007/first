from utils import (
    log,
    redirect,
    http_response,
    templates,
    response_with_headers,
)
import random
from models.Message import Message
from models.User import User


session = {}


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


def  current_user(request):
    session_id = request.cookies.get('user', '')
    user_id = int(session.get(session_id, '-1'))
    u = User.find_by(id=user_id)
    return u


def route_index(request):
    body = templates('index.html')
    return http_response(body)




def route_login(request):
    # header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    headers = {}
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        # log('type of u', type(u))
        if u.valid_login():
            user = User.find_by(username=u.username)
            session_id = random_str()
            session[session_id] = user.id
            log('session', session)
            headers['Set-Cookie'] = 'user={}'.format(session_id)
            result = '登录成功'
        else:
            result = '用户名或密码错误'
    else:
        result = ''
    body = templates('login.html',result=result)
    return http_response(body, headers=headers)


def route_register(request):
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
    body = templates('register.html',result=result)
    return http_response(body)


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


def route_admin_users(request):
    u = current_user(request)
    if u is not None and u.is_admin():
        us = User.all()
        body = templates('admin_user.html', users=us)
        return http_response(body)
    else:
        return redirect('/login')




route_dict = {
    '/' : route_index,
    '/login' : route_login,
    '/register' : route_register,
    '/messages' : route_message,
    '/test' : route_test,
    '/admin/users' : route_admin_users,
}