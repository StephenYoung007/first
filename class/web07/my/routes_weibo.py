from utils import (
    templates,
    response_with_headers,
    redirect,
    http_response,
    log,
                    )


from session import session
from models.User import User
from models.Weibo import Weibo




def current_user(request):
    session_id = request.query.get('user_id', '')
    user_id = session.get(session_id, -1)
    return user_id


def index(request):
    user_id = request.query.get('user_id', -1)
    user_id = int(user_id)
    log('user_id', user_id)
    user = User.find(user_id)
    if user is None:
        return redirect('/login')
    weibos = Weibo.find_all(user_id=user_id)
    body = templates('weibo_index.html', weibos=weibos, user=user)
    return http_response(body)



route_dict = {
    '/weibo/index' : index,
}
