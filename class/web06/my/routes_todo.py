from utils import (
    templates,
    response_with_headers,
    redirect,
    http_response,
                    )
from routes import current_user
from models.Todo import Todo
from models.User import User


def index(request):
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    todo_list = Todo.find_all(user_id=u.id)
    body = templates('todo_index.html', todos=todo_list)
    return http_response(body)


def add(request):
    uname = current_user(request)
    u = User.find_by(username=uname)
    if request.method == 'POST':
        form = request.form()
        t = Todo.new(form)
        t.user_id = u.id
        t.save()
    return redirect('/todo')


def delete_todo(request):
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    if t.user_id != u.id:
        return redirect('/login')
    if t is not None:
        t.remove()
    return redirect('/todo')


def edit(request):
    headers = {
        'Content-Type': 'text/html',
    }
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    if t.user_id != u.id:
        return redirect('/login')
    body = templates('todo_edit.html')
    body = body.replace('{{todo_id}}', str(t.id))
    # print('t.id', t.id)
    body = body.replace('{{todo_title}}', str(t.title))
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return  r.encode(encoding='utf-8')


def update(request):
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    if request.method == 'POST':
        form = request.form()
        todo_id = int(form.get('id', -1))
        t = Todo.find_by(id=todo_id)
        t.title = form.get('title', t.title)
        t.save()
    return redirect('/todo')



todo_routes = {
    '/todo' : index,
    '/todo/add' : add,
    '/todo/delete' : delete_todo,
    '/todo/edit' : edit,
    '/todo/update' : update,
}