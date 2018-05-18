from utils import log
from models.user import User


def template(name):
    path = './template/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def route_static(request):
    return b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>'


def route_login(request):
    # return b'HTTP/1.x 404 LOGIN IN\r\n\r\n<h1>Login In</h1>'

    header = 'HTTP/1.1 200 VERY OK\r\nContent-Type: text/html\r\n'
    # log(request.method)
    if request.method == 'POST':
        form = request.form()
        U = User()
        u = U.new(form)

        # u = User.new(form)
    #     if u.validate_register():
    #         u.save()
    #         result = '注册成功<br> <pre>{}</pre>'.format(User.all())
    #     else:
    #         result = '用户名或者密码长度必须大于2'
    # else:
    #     result = ''
        result = u
        log('u', u)
    else:
        result = 'no data'

    log('result', result)
    body = template('/register.html')
    with open('./template/register.html', 'r', encoding='utf-8') as f:
        body = f.read()
    log('body:', body)
    body = body.replace('{{result}}', result)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_register(request):
    header = 'HTTP/1.1 200 VERY OK\r\nContent-Type: text/html\r\n'
    # if request.method == 'POST':
    #     form = request.form()
    #     u = User.new(form)
    body = template('register.html')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_index(request):
    header = 'HTTP/1.1 200 VERY OK\r\nContent-Type: text/html\r\n'
    body = template('index.html')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')



route_dict = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register
}








