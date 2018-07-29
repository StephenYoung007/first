from utils import (
    log,
    templates,
    redirect,
    http_response,
    )

from models.Todo import Todo



def index(request):
    todo_list = Todo.all()
    body = templates('simple_todo_index.html', todos=todo_list)
    return http_response(body)


def edit(request):
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    body = templates('simple_todo_edit.html', todo =t)
    return http_response(body)


def add(request):
    form = request.form()
    Todo.new(form)
    return redirect('/todo')


route_simple_dict = {
    '/todo': index,
    '/todo/edit': edit,
    '/todo/add' : add,
}