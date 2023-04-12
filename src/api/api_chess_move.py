import flask

from src.consts import StatusCodes, Limits
from src.utils.make_json_response import make_json_response
from src.engine import stockfish_engine
from src.utils.params_handlers import handle_move_params
from src.utils.decorators import log, requires_auth

blueprint = flask.Blueprint(
    'api/chess/move',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/chess/move/', methods=['GET'])
@log(entry=False, output=False, level='INFO')
@requires_auth
def make_a_move() -> flask.Response:
    """
    "Генератор" шахматных ходов.
    """

    values = handle_move_params()
    if isinstance(values, flask.Response):
        return values
    user_move, prev_moves, orientation, min_time, max_time, threads, depth, ram_hash, skill_level, elo = values

    # Инициализация движка для игры, часть игры пользователя
    stockfish = stockfish_engine.get_stockfish(min_time, threads, depth, ram_hash, skill_level, elo, prev_moves)
    if stockfish is None:
        return make_json_response(StatusCodes.INVALID_PARAMS,
                                  f'"prev_moves" param has illegal moves')

    if user_move:
        answer = stockfish_engine.make_move(stockfish, user_move)
        if answer == StatusCodes.INVALID_PARAMS.value:
            return make_json_response(StatusCodes.INVALID_PARAMS,
                                      f'"{user_move}" is illegal move')

    # Часть игры машины
    max_time = max(min(min_time, Limits.MAX_THINK_MS.value), Limits.MIN_THINK_MS.value)  # min_time в limitations
    stockfish_move = stockfish.get_best_move_time(max_time)
    end_type, check = stockfish_engine.make_move(stockfish, stockfish_move, is_stockfish=True)

    prev_moves = ';'.join(filter(lambda x: x, (prev_moves, user_move, stockfish_move)))
    end_fen = stockfish.get_fen_position()

    return make_json_response(
        StatusCodes.OK, 'OK',
        fen=end_fen,
        stockfish_move=stockfish_move,
        prev_moves=prev_moves,
        orientation='w' if 'w' in end_fen else 'b',
        end_type=end_type,
        check=check
    )
