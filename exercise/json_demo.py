import json
from utils import log


R = {'job':['dev, 1.5'], 'emp' : {'who': 'Bob'}}

json.dump(R, open('savejson.txt', 'w'))

def run():
    d = open('savejson.txt').read()
    lo = json.loads(open('savejson.txt').read())
    log(d, type(d))
    log(lo, type(lo))


class name(object):
    def __init__(self):
        log(self.__class__.__name__)


if __name__ == '__main__':
    # run()
    a = name()