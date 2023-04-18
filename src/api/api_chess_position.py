import flask
import chess

from src.consts import StatusCodes, Config
from src.utils.abort import abort
from src.utils.response import flask_json_response
from src.utils.params_handlers import handle_position_params
from src.utils.decorators import log, requires_auth

blueprint = flask.Blueprint(
    'api/chess/position',
    __name__,
)


# Подумать над `with_engine`, и если он False, то не открывать движок.
@blueprint.route('/api/chess/position/', methods=['GET'])
@log(entry=True, output=False, with_entry_args=False, with_output_args=False, level='INFO')
@requires_auth
def get_position_score() -> flask.Response:
    """
    Возвращает оценку позиции (у кого больше шансов выиграть) и состояние (конец ли игры и кто выиграл).
    """

    params = handle_position_params()

    with Config.BOX.get_engine(
            prev_moves=params.prev_moves,
            prepared=params.prepared,
    ) as engine:

        if engine == StatusCodes.INVALID_PARAMS:
            abort(StatusCodes.INVALID_PARAMS, f'"prev_moves" param has illegal moves')

        if params.fen:
            try:
                chess.Board(params.fen)
                engine.set_fen_position(params.fen)
            except ValueError:
                abort(StatusCodes.INVALID_PARAMS, '"fen" param is invalid')

        board = chess.Board(fen := engine.get_fen_position())

        is_end = False
        who_win = None
        end_type = None
        value = None
        if board.is_checkmate():
            is_end = True
            who_win = 'b' if 'w' in fen else 'w'
            end_type = "checkmate"
            value = 0
        elif board.is_stalemate():
            is_end = True
            who_win = None
            end_type = "stalemate"
            value = 0
        elif board.is_insufficient_material():
            is_end = True
            who_win = None
            end_type = "insufficient_material"
            value = 0
        elif params.with_engine:
            evalutation = engine.get_evaluation()
            end_type = evalutation["type"]
            if end_type == 'mate':
                end_type = 'checkmate'
            value = evalutation["value"]

        if params.with_engine and engine.does_current_engine_version_have_wdl_option():
            wdl = engine.get_wdl_stats()
            if not wdl:
                wdl = None
        else:
            wdl = None

        return flask_json_response(
            StatusCodes.OK, "OK",
            is_end=is_end,
            who_win=who_win,
            end_type=end_type,
            value=value,
            wdl=wdl,
            fen=fen,
        )
