from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
)

from models.user import User

from utils import log

main = Blueprint('index', __name__)


def current_user():
    uid = session.get('user_id', -1)
    u = User.find_by(id = uid)
    return u


@main.route('/')
def index():
    u = current_user()
    return render_template('index.html', user = u)


@main.route('/register', methods=['POST'])
def register():
    form = request.form
    u = User.register(form)
    return redirect(url_for('.index'))


@main.route('/login', methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        return redirect(url_for('index.profile'))
    else:
        session['user_id'] = u.id
        session.permanent = True
        return redirect(url_for('index.index'))


@main.route('/profile')
def profile():
    u = current_user()
    if u is None:
        return redirect(url_for('topic.index'))
    else:
        return render_template('profile.html', user = u)
