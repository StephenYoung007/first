from routes import (
    templates,
    response_with_headers,
    redirect,
    current_user,
                    )
from utils import log
from models.Todo import Todo



def index(request):
    headers = {
        'Content-Type' : 'text/html'
    }
    todo_list = Todo.all()
    todo_html = ''.join(['<h3>{} : {}</h3>'.format(t.id, t.title) for t in todo_list])
    body = templates('todo_index.html')
    body = body.replace('{{todos}}', todo_html)
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def add(request):
    headers = {
        'Content-Type' : 'text/html'
    }
    # uname = current_user(redirect)
    # u = User.find_by(username=uname)
    if request.method == 'POST':
        form = request.form()
        t = Todo.new(form)
        t.save()
    return redirect('/todo')



todo_routes = {
    '/todo' : index,
    '/todo/add' : add,
}