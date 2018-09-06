from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
)


from routes import *

from models.reply import Reply


main = Blueprint('reply', __name__)

@main.route('/add', methods=['POST', 'GET'])
def add():
    form = request.form
    u = current_user()
    m = Reply.new(form, user_id = u.id)
    return redirect(url_for('topic.detail', id = m.topic_id))
