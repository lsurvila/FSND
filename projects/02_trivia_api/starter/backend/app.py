from flask import Flask
from flask_cors import CORS

from db import init_db
from routes import init_routes


def create_app(config_file):
    app = Flask(__name__)
    app.config.from_object(config_file)
    init_db(app)
    init_routes(app)
    CORS(app)
    return app


if __name__ == '__main__':
    create_app('config').run()

