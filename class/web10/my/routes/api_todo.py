import json
from routes.session import session

from utils import (
    log,
    redirect,
    http_response,
    json_response,
)

from models.Todo import Todo
from models.Weibo import Weibo


def all_weibos(request):
    ms = Weibo.all()
    data = [m.json() for m in ms]
    return json_response(data)


def add_weibo(request):
    form = request.json()
    m = Weibo.new(form)
    return json_response(m.json())


route_dict = {
    '/api/todo/all': all_weibos,
    '/api/todo/add': add_weibo,
}