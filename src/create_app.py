from pathlib import Path

from flask import Flask
from flaskext.markdown import Markdown
from loguru import logger

from src.consts import Config
from src.api import api_chess_docs, api_chess_move, api_chess_board, api_chess_position, api_chess, api_chess_limits
from src.engine.stockfish_engine import BoxWithEngines
from src.errors_handlers import register_error_handlers

abs_path = Path(__file__).parent.parent.absolute()
logger.add(
    abs_path / 'logs' / 'logs.log',
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} {level:<7} {message}",
    level='DEBUG',
    rotation="00:00",
    compression="zip",
)


def init_app():
    app = Flask(__name__)
    Markdown(app, extensions=['tables'])
    app.config['SECRET_KEY'] = Config.SECRET_KEY

    app.register_blueprint(api_chess.blueprint)
    app.register_blueprint(api_chess_docs.blueprint)
    app.register_blueprint(api_chess_limits.blueprint)
    app.register_blueprint(api_chess_move.blueprint)
    app.register_blueprint(api_chess_board.blueprint)
    app.register_blueprint(api_chess_position.blueprint)

    register_error_handlers(app)

    return app


def init_box_with_engines() -> None:
    Config.BOX = BoxWithEngines(Config.PREPARED_ENGINES)
    logger.info(f"{Config.PREPARED_ENGINES} chess engines prepared!")
