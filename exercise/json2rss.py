import re
import sys, os
import logging
import json
import time
import argparse
import base64
import traceback

f = open("gui-config.json", 'r')
content = f.read()
dic = json.loads(content)
d = dic['configs']


def to_bytes(s):
    if type(s) == str:
        return s.encode('utf-8')
    return s


def to_str(s):
    if type(s) == bytes:
        return s.decode('utf-8')
    return s


def b64encode(data):
    if type(data) == bytes:
        return to_str(base64.urlsafe_b64encode(data)).strip('=')
    elif type(data) == str:
        return to_str(base64.urlsafe_b64encode(to_bytes(data))).strip('=')
    else:
        return data


def to_links(j):
    links = []
    for i in j:
        server = i.get('server')
        server_port = i.get('server_port')
        password = i.get('password')
        method = i.get('method')
        protocol = i.get('protocol')
        obfs = i.get('obfs', 'plain')
        remarks = i.get('remarks')
        uri = '{}:{}:{}:{}:{}:{}'.format(server, server_port, protocol, method, obfs, b64encode(password))
        group = b64encode('Google')
        stern = '/?obfsparam=&remarks={}&group={}'.format(b64encode(remarks), group)
        links.append('ssr://{}'.format(b64encode(('{}{}'.format(uri, stern)))))
    str = ''
    for j in links:
        j = j + "\r\n"
        str += j
    str = str[:-2]
    # print(str)
    print(b64encode(str))


if __name__ == '__main__':
    print(to_links(d))
