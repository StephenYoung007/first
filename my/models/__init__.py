import json


def load(path):
    '''
    从一个文件中载入list或者字典
    :param path: 载入路径
    :return: 字典或列表
    '''
    with open(path, 'r', encoding='utf-8') as f:
        return json.loads(f.read())


def save(data, path):
    '''
    用于把一个list或者字典保存到path路径
    :param data: 字典或列表
    :param path: 路径
    :return: 写入
    '''
    s =json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(s)


'''
model是存储数据的基类，包括User、Message等数据
'''
class Model(object):
    '''
    @classmethod表示这是一个类方法，类方法的调用方式是类名.类方法
    when be called, classmethod will also creat an object
    self代表的普通方法，必须通过类的实例调用，类似于c++中的通过对象调用
    '''
    @classmethod
    def db_path(cls):
        '''
        传入cls
        :return:以classname命名的路径对象
        '''
        classname = cls.__name__
        path = 'db/{}.txt'.format(classname)
        return path


    @classmethod
    def new(cls, form):
        '''
        传入form方法，得到cls的body字典
        :param form:
        :return: 相当于User（form)或者Message(form)
        '''
        m = cls(form)
        # log('type of m', type(m))
        return m


    @classmethod
    def all(cls):
        '''
        得到一个类的所有存储的实例
        :return:
        '''
        path = cls.db_path()
        models = load(path)
        ms = [cls.new(m) for m in models]
        return ms


    def save(self):
        models = self.all()
        first_index = 0
        if self.__dict__.get('id') is None:
            if len(models) >0:
                self.id = models[-1].id +1
            else:
                self.id = first_index
            models.append(self)
        else:
            index = -1
            for i, m in enumerate(models):
                if m.id ==self.id:
                    index = i
                    break
            if index > -1:
                models[index] = self
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)


    @classmethod
    def find_by(cls, **kwargs):
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        for m in all:
            if v == m.__dict__[k]:
                return m
        return None


    @classmethod
    def find_all(cls, **kwargs):
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        data = []
        for m in all:
            if v == m.__dict__[k]:
                data.append(m)
        return data


    def __repr__(self):
        """
        这是一个 魔法函数
        不明白就看书或者 搜
        当你调用 str(o) 的时候
        实际上调用了 o.__str__()
        当没有 __str__ 的时候
        就调用 __repr__
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)





    # @classmethod
    # def find_by(cls, **kwargs):
    #     k, v = '', ''
    #     for key, value in kwargs.items():
    #         k, v = key, value
    #         all = cls.all()
    #     for m in all:
    #         if v == m.__dict__[k]:
    #             return m
    #     return None