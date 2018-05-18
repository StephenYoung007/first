import socket
import ssl


def parsed_url(url):
    protocal = 'http'
    if url[:7] == "http://":
        u = url.split('://')[1]
    elif url[:8] == 'https://':
        protocal = 'https'
        u = url.split("://")[1]
    else:
        u = url

    # log(u)

    i = u.find('/')
    if i == -1:
        host = u
        path = '/'
    else:
        host = u[:i]
        path = u[i:]

    # log(host,path)

    port_dict = {
        "http":80,
        "https":433
    }
    port = port_dict[protocal]
    if ":" in host:
        h = host.split(':')
        host = h[0]
        port = h[1]
    # log(host,port)

    return protocal, host, port, path


def socket_by_protocal(protocal):
    if protocal == 'http':
        s = socket.socket()
    else:
        s = ssl.wrap_socket(socket.socket())


def run(host="", port=3000):
    with socket.socket() as s:
        s.bind((host, port))
        while True:
            s.listen(5)
            connection, address = s.accept()
            r =  connection.recv(1024)
            r.decode("utf-8")
            response = b'HTTP/1.1 233 VERY OK\r\n\r\n<h1>hello world</h1>'
            connection.sendall(response)
            connection.close()


def parsed_response(response):
    header, body = response.split('\r\n\r\n')
    h = header.split('\r\n')
    status_code = h[0].split()[1]
    status_code = int(status_code)

    headers = {}

    print(h[1:])
    for line in  h[1:]:
        print(line)
        key, value = line.split(':',1)
        headers[key] = value

    return status_code, headers, body


def response_test():
    response = 'HTTP/1.1 301 Moved Permanently\r\n' \
        'Content-Type: text/html\r\n' \
        'Location: https://movie.douban.com/top250\r\n' \
        'Content-Length: 178\r\n\r\n' \
        'test body'
    status_code, header, body = parsed_response(response)
    print(status_code, header, body)


def parsed_url_test():
    url = ["www.baidu.com",
           "https://g.cn:3000/path",
           "z.cn"]

    for i in url:
        protocal, host, port, path = parsed_url(i)

    print(protocal, host, port, path)


if __name__ == '__main__':
    config = dict(
        host = '',
        port = 3000,
    )
    run(**config)


