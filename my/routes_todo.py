from routes import (
    templates,
    response_with_headers,
    redirect,
    current_user,
                    )
from utils import log
from models.Todo import Todo
from models.User import User


def index(request):
    headers = {
        'Content-Type' : 'text/html'
    }
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    todo_list = Todo.find_all(user_id=u.id)
    # todo_html = ''.join(['<h3>{} : {}</h3>'.format(t.id, t.title) for t in todo_list])
    todos = []
    for t in todo_list:
        edit_link = '<a href="/todo/edit?id={}">编辑</a>'.format(t.id)
        delete_link = '<a href="/todo/delete?id={}">删除</a>'.format(t.id)
        s = '<h3>{} : {} {} {}</h3>'.format(t.id, t.title, edit_link, delete_link)
        todos.append(s)
    todo_html = ''.join(todos)
    body = templates('todo_index.html')
    body = body.replace('{{todos}}', todo_html)
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def add(request):
    headers = {
        'Content-Type' : 'text/html'
    }
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


todo_routes = {
    '/todo' : index,
    '/todo/add' : add,
    '/todo/delete' : delete_todo,
}