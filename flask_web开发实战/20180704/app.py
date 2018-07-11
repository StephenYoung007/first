from flask import Flask, request, make_response, redirect, abort, render_template
app = Flask(__name__)

# from flask.ext import Manager
# manager = Manager(app)





@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user-agent')
def user_agent():
    user_agent  =request.headers.get('User-Agent')
    return '<p>your brower is {}</p>'.format(user_agent)


@app.route('/response')
def make_responses():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response


@app.route('/redirect')
def redirect_demo():
    return redirect('http://python.stephenyoung.top')

'''
@app.route('/user/<id>')
def get_user(id):
    user = load_user(id)
    if not user:
        abort(404)
    return '<h1>hello, {}</h1>'.format(user.name)
'''


@app.route('/user/<name>')
def user(name):
    # name = 'gua'
    return render_template('user.html', name=name)


if __name__ == '__main__':
    config = dict(
        debug=True,
        host='localhost',
        port=3000
    )
    app.run(**config)