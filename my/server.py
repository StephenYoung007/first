import socket
import urllib.parse
from utils import log
from routes import route_static
from routes import route_dict
from routes_todo import todo_routes


class Request(object):
    '''
    用于保存请求返回的类
    '''
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''
        self.headers = {}
        self.cookies = {}


    def add_cookies(self):
        """
        height=169; user=gua
        :return:
        """
        cookies = self.headers.get('Cookie', '')
        kvs = cookies.split('; ')
        for kv in kvs:
            if '=' in kv:
                k, v = kv.split('=')
                self.cookies[k] = v

    def add_headers(self, header):
        """
        [
            'Accept-Language: zh-CN,zh;q=0.8'
            'Cookie: height=169; user=gua'
        ]
        """
        lines = header
        for line in lines:
            k, v = line.split(': ', 1)
            self.headers[k] = v
        # 清除 cookies
        self.cookies = {}
        self.add_cookies()


    def form(self):
        '''
        用于将body保存为字典格式并返回
        '''
        body = urllib.parse.unquote(self.body)
        args = body.split('&')
        f= {}
        log(args)
        for arg in args:
            k,v = arg.split('=')
            f[k] = v
        return f



request = Request()




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
    r.update(todo_routes)
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
            log('r', r)
            if len(r.split()) < 2:
                continue
            path = r.split()[1]
            # print('response : \n', r)
            request.method = r.split()[0]
            request.add_headers(r.split('\r\n\r\n', 1)[0].split('\r\n')[1:])
            request.body = r.split('\r\n\r\n', 1)[1]
            # log('----', request.__dict__)
            # log('path', path)
            response = response_for_path(path)
            connection.sendall(response)
            connection.close()
            print('closed')







if __name__ == '__main__':
    conifg = dict(
        host = '127.0.0.1',
        port = 3000
    )
    run(**conifg)