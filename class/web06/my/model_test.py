import json


def load(path):
    '''
    从一个文件中载入list或者字典
    :param path: 载入路径
    :return: 字典或列表
    '''
    with open(path, 'r', encoding='utf-8') as f:
        return json.loads(f.read())




def db_path(cls):
    '''
    传入cls
    :return:以classname命名的路径对象
    '''
    classname = cls.__name__
    path = 'db/{}.txt'.format(classname)
    return path


def all():
    pass