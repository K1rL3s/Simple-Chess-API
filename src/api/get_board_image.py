from io import BytesIO

import flask

from src.consts import StatusCodes
from src.engine import engine
from src.api.json_response import make_json_response


def get_board_image() -> flask.Response:
    """
    Возвращает .png файл 390x390 с шахматной доской и фигруами на ней в соответствии с FEN-Notaion.
    """
    data = flask.request.args
    fen_position: str = data.get('fen_position')
    orientation: str = str(data.get('orientation', 'w')).lower()

    board_image: BytesIO = engine.get_board_image(fen_position, orientation)
    if board_image is None:
        return make_json_response(StatusCodes.INVALID_PARAMS, text='Invalid FEN position')
    return flask.send_file(board_image, mimetype="image/x-png")


def register_get_board_image(app: flask.Flask):
    app.add_url_rule('/get_board_image', view_func=get_board_image, methods=["GET"])
