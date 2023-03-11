import flask
import chess

from src.consts import StatusCodes
from src.engine import engine
from src.api.json_response import make_json_response

blueprint = flask.Blueprint(
    'api/chess/position',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/chess/position/', methods=['GET'])
def get_position_score() -> flask.Response:
    """
    Возвращает оценку позиции (у кого больше шансов выиграть) и состояние (конец ли игры и кто выиграл).
    """
    data = flask.request.args
    prev_moves = data.get('prev_moves')
    fen_position = data.get('fen')

    if not prev_moves and not fen_position:
        return make_json_response(StatusCodes.INVALID_PARAMS.value,
                                  '"prev_moves" or "fen" param is required')

    stockfish = engine.get_stockfish(previous_moves=prev_moves)
    if stockfish is None:
        return make_json_response(StatusCodes.INVALID_PARAMS,
                                  f'"prev_moves" param has illegal moves')

    if fen_position:
        try:
            chess.Board(fen_position)
            stockfish.set_fen_position(fen_position)
        except ValueError:
            return make_json_response(StatusCodes.INVALID_PARAMS,
                                      '"fen" param is invalid')

    board = chess.Board(fen_position := stockfish.get_fen_position())

    if board.is_checkmate():
        is_end = True
        who_win = 'w' if 'b' in fen_position else 'b'
        end_type = "mate"
        value = 0
    elif board.is_stalemate():
        is_end = True
        who_win = None
        end_type = "stalemate"
        value = 0
    else:
        is_end = False
        who_win = None
        evalutation = stockfish.get_evaluation()
        end_type = evalutation["type"]
        value = evalutation["value"]

    if stockfish.does_current_engine_version_have_wdl_option():
        wdl = stockfish.get_wdl_stats()
        if not wdl:
            wdl = None
    else:
        wdl = None

    # position = {
    #     "is_end": is_end,
    #     "who_win": who_win,
    #     "type": end_type,
    #     "value": value,
    #     "wdl": wdl
    # }

    return make_json_response(200, "OK",
                              is_end=is_end,
                              who_win=who_win,
                              type=end_type,
                              value=value,
                              wdl=wdl,
                              fen=stockfish.get_fen_position(),
                              )
