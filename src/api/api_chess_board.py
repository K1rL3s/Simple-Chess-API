from io import BytesIO

import flask

import src.engine.chess_board
from src.consts import StatusCodes
from src.utils.make_json_response import make_json_response
from src.utils.params_handlers import handle_board_params
from src.utils.log_decorator import log_decorator

blueprint = flask.Blueprint(
    'api/chess/board',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/chess/board/', methods=['GET'])
@log_decorator
def get_board_image() -> flask.Response:
    """
    Возвращает .png файл с шахматной доской и фигруами на ней в соответствии с FEN.
    """

    values = handle_board_params()
    if isinstance(values, flask.Response):
        return values

    fen_position, size, orientation, colors, last_move, coords, check = values

    board_image: BytesIO = src.engine.chess_board.get_board_image(
        fen_position=fen_position,
        size=size,
        orientation=orientation,
        colors=colors,
        last_move=last_move,
        coords=coords,
        check=check,
    )

    if board_image is None:
        return make_json_response(StatusCodes.INVALID_PARAMS,
                                  '"fen" param is invalid')

    return flask.send_file(board_image, mimetype="image/png")
