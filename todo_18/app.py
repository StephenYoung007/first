from flask import Flask

app = Flask(__name__)

import config
app.secret_key = config.secret_key

from routes.index import main as index_router
app.register_blueprint(index_router)

if __name__ == '__main__':
    config = dict(
        debug = True,
        host = '0.0.0.0',
        port = 3000,
    )
    app.run(**config)