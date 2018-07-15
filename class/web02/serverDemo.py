import socket

def log(*args, **kwargs):
    print('log', *args, **kwargs)


def route_index():
    header = 'HTTP/1.1 200 OK\r\nContent-type: text/html\r\n'
    body = '<h1>Gua</h1><img src = "/doge.gif">'
    r = header + '\r\n' +body
    return r.encode(encoding='utf-8')

def page(name):
    with open(name, encoding='utf-8') as f:
        return f.read()


def route_msg():
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = page('html_basic.html')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')



def error(code=404):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    # 之前上课我说过不要用数字来作为字典的 key
    # 但是在 HTTP 协议中 code 都是数字似乎更方便所以打破了这个原则
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>404 NOT FOUND</h1>',
    }
    return e.get(code, b'')


def route_image():
    """
    图片的处理函数, 读取图片并生成响应返回
    """
    with open('doge.gif', 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
        img = header + b'\r\n' + f.read()
        return img


def response_for_path(path):
    r = {
        '/': route_index,
        '/doge.gif': route_image,
        '/msg': route_msg,
    }
    response = r.get(path, error)
    return response()



def run(host = '', port = 3000):
    with socket.socket() as s:
        s.bind((host, port))



        while True:
            s.listen(5)
            connection, address = s.accept()
            request = connection.recv(1024)
            log('raw', request)
            request = request.decode('utf-8')
            log('ip and request,{}\n{}'.encode('utf-8'))
            log(request)
            try:
                path = request.split()[1]
                response = response_for_path(path)
                connection.sendall(response)
            except Exception as e:
                log('error', e)

            connection.close()


def main():
    config = dict(
        host = '',
        port = 3000,
    )

    run(**config)

if __name__ == '__main__':
    main()