import socket
import urllib.parse
from utils import log
# from routes import route_static
# from routes import route_dict
# from routes_todo import todo_routes
from routes.api_todo import route_dict as api_todo


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


    def json(self):
        # 解码python json格式
        import json
        return json.loads(self.body)



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


def response_for_path(path, request):
    path, query = parsed_path(path)
    request.path = path
    request.query = query
    r = {
        # '/static' : route_static,
    }
    # r.update(route_dict)
    # r.update(todo_routes)
    r.update(api_todo)
    # log('r', r, path, query)
    response = r.get(path, error)
    return response(request)


def process_request(connection):
    r = connection.recv(1024)
    r = r.decode('utf-8')
    if len(r.split()) < 2:
        connection.close()
    path = r.split()[1]
    request = Request()
    request.method = r.split()[0]
    request.add_headers(r.split('\r\n\r\n', 1)[0].split('\r\n')[1:])
    request.body = r.split('\r\n\r\n', 1)[1]
    response = response_for_path(path, request)
    connection.sendall(response)
    try:
        log('响应\n', response.decode('utf-8').replace('\r\n', '\n'))
    except Exception as e:
        log('异常', e)
    connection.close()
    print('close')


def run(host='', port=3000):
    print('start at','{}:{}'.format(host, port))
    with socket.socket() as s:
        s.bind((host, port))
        while True:
            s.listen(5)
            connection, address = s.accept()
            import _thread
            _thread.start_new_thread(process_request, (connection,))







if __name__ == '__main__':
    conifg = dict(
        host = '127.0.0.1',
        port = 3000
    )
    run(**conifg)
