import os

from flask import Flask
from flaskext.markdown import Markdown
from dotenv import load_dotenv

from src.api.json_response import make_json_response
from src.api import api_chess_docs, api_chess_move, api_chess_board


app = Flask(__name__)
Markdown(app, extensions=['tables'])
load_dotenv()
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']


@app.errorhandler(404)
def not_found(_):
    return make_json_response(
        404,
        'Not found'
    )


@app.errorhandler(400)
def bad_request(_):
    return make_json_response(
        400,
        'Bad Requst'
    )


@app.errorhandler(Exception)
def global_exception_catcher(error):
    return make_json_response(
        500,
        'Something went wrong. Probably invalid params',
        error=str(error)
    )


def init_app():
    # waitress-serve --host 0.0.0.0 --port 5000 --call main:init_app
    # uwsgi
    # gunicorn
    app.register_blueprint(api_chess_docs.blueprint)
    app.register_blueprint(api_chess_move.blueprint)
    app.register_blueprint(api_chess_board.blueprint)
    return app
