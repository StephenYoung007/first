import socket
import urllib.parse

from utils import log

from routes import route_static
from routes import route_dict


class Request(object):
    def __init__(self):
        self.method = 'get'
        self.path = ''
        self.body = ''
        self.query = {}
        self.headers = {}
        self.cookies = {}


    def form(self):
        body = urllib.parse.unquote(self,body)
        args = body.split('&')
        f = {}
        for arg in args:
            k, v = arg.split("=")
            f[k] = v
        return f


    def add_cookies(self):
        cookies = self.headers.get("Cookies", '')
        kvs = cookies.split(":", 1)
        log('cookies', kvs)
        for kv in kvs:
            if ':' in kv:
                k, v = kv.split("=", 1)
                self.cookies[k] = v

    def add_headers(self, header):
        lines = header
        for line in lines:
            k, v = line.split(":", 1)
            self.headers[k] = v
            self.cookies = {}
            self.add_cookies()



request = Request()

def error(request, code = 404):
    e = {
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')

def response_for_path(path):
    request.path, request.query = parsed_path(path)
    r = {
        'static' : route_static,

    }

    r.update(route_dict)
    log('response_for_path', path)
    log('r', r)
    response = r.get(path, error)
    return response(request)

def parsed_path(path):
    if '?' not in path:
        path = path
        query = {}
    else:
        path, query_string = path.split('?', 1)
        args = query_string.split("&")
        query = {}
        for arg in args:
            k, v = arg.split("=")
            query[k] = v

    return path, query

def run(host, port = 80):
    with socket.socket() as s:
        s.bind((host, port))
        while True:
            s.listen(5)
            connection, address = s.accept()
            r = connection.recv(1024)
            r = r.decode("utf-8")
            if len(r.split()) < 2:
                continue
            log('r', r)
            path = r.split()[1]
            request.method = r.split()[0]
            request.add_headers(r.split('\r\n\r\n', 1)[0].split('\r\n', 1)[1:])
            request.body = r.split('\r\n\r\n', 1)[1]
            response = response_for_path(path)
            connection.send(response)
            connection.close()

if __name__ == '__main__':
    config = dict(
        host = '',
        port = 3000
    )

    run(**config)
