from jinja2 import Environment, FileSystemLoader
import os.path
from utils import log


path = '{}/templates/'.format(os.path.dirname(__file__))
log('path', path)
loader = FileSystemLoader(path)
env = Environment(loader=loader)
template = env.get_template('demo.html')

ns = list(range(0, 3))

us = [
    {
        'id':  1,
        'name': 'gua',
    },
    {
        'id': 2,
        'name': '瓜'
    }
]
log(template.render(name='gua',
                    numbers=ns,
                    users=us,
                    foo=100,
                    ))