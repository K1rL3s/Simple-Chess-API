from io import BytesIO

import flask

import src.engine.chess_board
from src.consts import StatusCodes
from src.utils.abort import abort
from src.utils.params_handlers import handle_board_params
from src.utils.decorators import log, requires_auth

blueprint = flask.Blueprint(
    'api/chess/board',
    __name__,
)


@blueprint.route('/api/chess/board/', methods=['GET'])
@log(entry=False, output=False, level='INFO')
@requires_auth
def get_board_image() -> flask.Response:
    """
    Возвращает .png файл с шахматной доской и фигруами на ней в соответствии с FEN.
    """

    params = handle_board_params()

    board_image: BytesIO = src.engine.chess_board.get_board_image(
        fen=params.fen,
        size=params.size,
        orientation=params.orientation,
        colors=params.colors,
        last_move=params.last_move,
        coords=params.coords,
        check=params.check,
    )

    if board_image is None:
        abort(StatusCodes.INVALID_PARAMS, '"fen" param is invalid')

    return flask.send_file(board_image, mimetype="image/png")
