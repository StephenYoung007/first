import time


def log(*args, **kwargs):
    '''
    用于格式化输出的函数
    '''
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    with open('log.gua.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f,  **kwargs)