import time
from jinja2 import Environment, FileSystemLoader
import os.path


def log(*args, **kwargs):
    '''
    用于格式化输出的函数
    '''
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    with open('log.gua.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f,  **kwargs)
        print(dt, *args, **kwargs)


path = '{}/templates/'.format(os.path.dirname(__file__))
loader = FileSystemLoader(path)
env = Environment(loader=loader)




def templates(path, **kwargs):
    # print('path', path)
    t = env.get_template(path)
    return t.render(**kwargs)


def response_with_headers(headers, code=200):
    header = 'HTTP/1.1 {} FUCK OK\r\n'.format(code)
    header += ''.join(['{}:{}\r\n'.format(k, v)
                       for k, v in headers.items()])
    return header


def redirect(url):
    headers={
        'Location': url,
    }
    r = response_with_headers(headers, 302) + '\r\n'
    return r.encode('utf-8')


def http_response(body, headers=None):
    header = 'HTTP/1.1 200 OK\r\nContent-ype: text/html\r\n'
    if headers is not None:
        header += ''.join(['{}: {}\r\n'.format(k, v) for k, v in headers.items()])
    r = header + '\r\n' + body
    # return r
    return r.encode(encoding='utf-8')