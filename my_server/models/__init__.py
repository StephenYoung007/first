import json

from utils import log


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        return json.loads(s)



class Model(object):
    @classmethod
    def db_path(cls):
        classname = cls.__name__
        path = 'db/{}.txt'.format(classname)
        return path

    @classmethod
    def new(cls, form):
        m = cls(form)
        return m

    @classmethod
    def all(cls):
        path = cls.db_path()
        models = load(path)
        ms = []
        for m in models:
            me = cls.new(m)
            ms.append(me)
        # ms = [cls.new(m) for m in models]
        return ms

