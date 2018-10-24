import socket
import requests.packages.urllib3.util.ssl_
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'



def parsed_url(url):
    protocol = 'http'
    if url[:7] == 'http://':
        u = url.split('://')[1]
    elif url[:8] == 'https://':
        protocol = 'https'
        u = url.split('://')[1]
    else :
        u = url

    print("u = {}",u.format())

    i = u.find('/')
    if i == -1:
        host = u
        path = '/'
    else:
        host = u[:i]
        path = u[i:]

    port_dict = {
        'http':80,
        'https':443,
    }
    port = port_dict[protocol]

    if ':' in host:
        h = host.split(':')
        host = h[0]
        port = int(h[1])
    print(protocol, host, path, port)
    return protocol, host, path, port

def socket_by_protocol(protocol):
    if protocol == 'http':
        s = socket.socket()
    else:
        s = requests.packages.urllib3.util.ssl_.wrap_socket(socket.socket())
    return s

def response_by_socket(s):
    response = b''
    buffer_size = 1024
    while True:
        r = s.recv(buffer_size)
        if len(r) < buffer_size:
            break
        response += r
    return response

def parsed_response(r):
    print(r + '001')
    header, body = r.split('\r\n\r\n',1)
    h = header.split('\r\n')
    status_code = h[0].split()[1]
    status_code = int(status_code)

    headers = {}
    for line in h[1:]:
        k, v = line.split(': ')
        headers[k] = v
    return status_code, headers, body

def get(url):
    protocol, host, path, port = parsed_url(url)

    print("****", protocol, host, path, port)
    s = socket_by_protocol(protocol)
    print(host, port)
    s.connect((host, port))

    request = 'GET {} HTTP/1.1\r\nhost: {}\r\nConnection: close\r\n\r\n'.format(path, host)
    # request = 'GET / HTTP/1.1\r\nhost: 35.221.67.128\r\nConnection: close\r\n\r\n'.format(path, host)
    encoding = 'utf-8'
    s.send(request.encode(encoding))

    response = response_by_socket(s)
    r = response.decode(encoding)
    print(r)

    status_code, headers, body = parsed_response(r)
    if status_code in [301, 302]:
        url = headers['Location']
        return get(url)

    return status_code, headers, body

def main():
    # url = 'https://movie.douban.com/top250'
    url = 'http://udp.stephenyoung.top/test'
    status_code, headers, body = get(url)
    print(status_code, headers, body)

if __name__ == '__main__':
    main()
