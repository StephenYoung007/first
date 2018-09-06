from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
)

from models.topic import Topic
from models.user import User
from routes import *


main = Blueprint('topic', __name__)


@main.route('/')
def index():
    ms = Topic.all()
    return render_template('/topic/index.html', ms=ms)


@main.route('/new', methods=['GET'])
def new():
    u = current_user()
    if u is None:
        return redirect(url_for('index.index'))
    else:
        return render_template('/topic/new.html')

@main.route('/add', methods=['POST'])
def add():
    form = request.form
    u = current_user()
    ms = Topic.new(form, user_id = u.id)
    return redirect(url_for('.index'))


@main.route('/detail/<int:id>')
def detail(id):
    m = Topic.find(id)
    user_id = m.user_id
    print('user_id',user_id)
    u = User.get(user_id)
    return render_template('/topic/detail.html', topic=m, user=u)
