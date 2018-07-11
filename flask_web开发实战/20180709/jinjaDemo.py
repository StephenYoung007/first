from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user/<name>')
def name(name):
    return render_template('base.html', name=name)


@app.route('/user/<user>')
def user(user):
    return render_template('user.html', user = '')


if __name__ == '__main__':
    app.run(debug=True)