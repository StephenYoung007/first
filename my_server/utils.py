import time

def log(*args, **kwargs):
    print(time.ctime(),args,kwargs)