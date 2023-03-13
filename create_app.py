import os

from flask import Flask
from flaskext.markdown import Markdown

from src.api.json_response import make_json_response
from src.consts import StatusCodes
from src.api import api_chess_docs, api_chess_move, api_chess_board, api_chess_position, api_chess

app = Flask(__name__)
Markdown(app, extensions=['tables'])
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']


@app.errorhandler(StatusCodes.NOT_FOUND.value)
def not_found(_):
    return make_json_response(
        StatusCodes.NOT_FOUND.value,
        'Not found'
    )


@app.errorhandler(StatusCodes.INVALID_PARAMS.value)
def bad_request(_):
    return make_json_response(
        StatusCodes.INVALID_PARAMS,
        'Bad Requst'
    )


@app.errorhandler(Exception)
def global_exception_catcher(error):
    return make_json_response(
        StatusCodes.SERVER_ERROR,
        'Something went wrong. Probably invalid params',
        error=str(error)
    )


def init_app():
    # waitress-serve --host 0.0.0.0 --port 5000 --call main:init_app
    # uwsgi
    # gunicorn
    app.register_blueprint(api_chess.blueprint)
    app.register_blueprint(api_chess_docs.blueprint)
    app.register_blueprint(api_chess_move.blueprint)
    app.register_blueprint(api_chess_board.blueprint)
    app.register_blueprint(api_chess_position.blueprint)
    return app
