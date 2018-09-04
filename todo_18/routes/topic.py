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


main = Blueprint('topic', __name__)


def current_user():
    uid = session.get('user_id', -1)
    print('uid',uid)
    u = User.find_by(id=uid)
    return u


@main.route('/')
def index():
    ms = Topic.all()
    return render_template('/topic/index.html', ms=ms)


@main.route('/new', methods=['GET'])
def new():
    return render_template('/topic/new.html')

@main.route('/add', methods=['POST'])
def add():
    form = request.form
    u = current_user()
    ms = Topic.new(form, user_id = u.id)
    return redirect(url_for('.index'))


@main.route('/<int:id>')
def detail(id):
    m = Topic.find(id)
    user_id = m.user_id
    print('user_id',user_id)
    u = User.get(user_id)
    return render_template('/topic/detail.html', topic=m, user=u)
