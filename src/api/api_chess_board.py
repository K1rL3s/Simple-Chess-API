from io import BytesIO

import flask

from src.consts import StatusCodes, Defaults
from src.engine import engine
from src.api.json_response import make_json_response
from src.utils.limitations import limit_board_params

blueprint = flask.Blueprint(
    'api/chess/board',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/chess/board/', methods=['GET'])
def get_board_image() -> flask.Response:
    """
    Возвращает .png файл с шахматной доской и фигруами на ней в соответствии с FEN.
    """
    data = flask.request.args
    # Вынести обработку в отдельный файл.
    try:
        fen_position = data.get('fen')
        size = int(data.get('size', Defaults.BOARD_IMAGE_SIZE.value))
        orientation = data.get('orientation', 'w').lower()
    except Exception as e:
        return make_json_response(StatusCodes.INVALID_PARAMS,
                                  str(e))

    size = limit_board_params(size)

    board_image: BytesIO = engine.get_board_image(
        fen_position=fen_position,
        size=size,
        orientation=orientation
    )
    if board_image is None:
        return make_json_response(StatusCodes.INVALID_PARAMS,
                                  '"fen" param is invalid')
    return flask.send_file(board_image, mimetype="image/png")
