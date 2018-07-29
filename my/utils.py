import time


def log(*args, **kwargs):
    '''
    用于格式化输出的函数
    '''
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    with open('log.gua.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f,  **kwargs)






def templates(name):
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


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