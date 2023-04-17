import flask

from src.consts import StatusCodes, Limits
from src.utils.abort import abort
from src.utils.response import flask_json_response
from src.engine import stockfish_engine
from src.utils.params_handlers import handle_move_params
from src.utils.decorators import log, requires_auth

blueprint = flask.Blueprint(
    'api/chess/move',
    __name__,
)


@blueprint.route('/api/chess/move/', methods=['GET'])
@log(entry=True, output=False, with_entry_args=False, with_output_args=False, level='INFO')
@requires_auth
def make_a_move() -> flask.Response:
    """
    "Генератор" шахматных ходов.
    """

    params = handle_move_params()

    # Инициализация движка для игры, часть игры пользователя
    stockfish = stockfish_engine.get_stockfish(
        min_time=params.min_time,
        threads=params.threads,
        depth=params.depth,
        ram_hash=params.ram_hash,
        skill_level=params.skill_level,
        elo=params.elo,
        prev_moves=params.prev_moves,
    )
    if stockfish == StatusCodes.INVALID_PARAMS:
        abort(StatusCodes.INVALID_PARAMS, f'"prev_moves" param has illegal moves')

    if params.user_move:
        answer = stockfish_engine.make_move(stockfish, params.user_move)
        if answer == StatusCodes.INVALID_PARAMS:
            abort(StatusCodes.INVALID_PARAMS, f'"{params.user_move}" is illegal move')

    # Часть игры машины
    # min_time ограничивается в limitations, в get_stockfish
    max_time = max(min(params.min_time, Limits.MAX_THINK_MS.value), Limits.MIN_THINK_MS.value)
    stockfish_move = stockfish.get_best_move_time(max_time)

    # 100% не вернёт ошибку
    end_type, check = stockfish_engine.make_move(
        stockfish, stockfish_move, is_stockfish=True
    )

    prev_moves = ';'.join(
        filter(
            lambda x: x,
            (params.prev_moves, params.user_move, stockfish_move)
        )
    )
    end_fen = stockfish.get_fen_position()

    return flask_json_response(
        StatusCodes.OK, 'OK',
        fen=end_fen,
        stockfish_move=stockfish_move,
        prev_moves=prev_moves,
        orientation='w' if 'w' in end_fen else 'b',
        end_type=end_type,
        check=check
    )
