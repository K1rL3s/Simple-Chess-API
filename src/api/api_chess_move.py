import flask

# from chess import Termination

from src.consts import StatusCodes
from src.api.json_response import make_json_response
from src.engine import stockfish_engine
from src.utils.params_handlers import handle_move_params
from src.utils.time_log import log_run_time

blueprint = flask.Blueprint(
    'api/chess/move',
    __name__,
    template_folder='templates'
)


# Сделать проверку на то, что orientation равен цвету игрока.
@blueprint.route('/api/chess/move/', methods=['GET'])
@log_run_time
def make_a_move() -> flask.Response:
    """
    "Генератор" шахматных ходов.
    """
    values = handle_move_params()
    if isinstance(values, flask.Response):
        return values
    user_move, prev_moves, orientation, threads, depth, ram_hash, skill_level, elo = values

    # Инициализация движка для игры, часть игры пользователя
    stockfish = stockfish_engine.get_stockfish(threads, depth, ram_hash, skill_level, elo, prev_moves)
    if stockfish is None:
        return make_json_response(StatusCodes.INVALID_PARAMS,
                                  f'"prev_moves" param has illegal moves',
                                  fen_position='')

    start_fen_pos = stockfish.get_fen_position()
    if user_move:
        answer = stockfish_engine.make_move(stockfish, user_move)
        if answer == StatusCodes.INVALID_PARAMS.value:
            return make_json_response(StatusCodes.INVALID_PARAMS,
                                      f'"{user_move}" is illegal move',
                                      fen_position=start_fen_pos)

    # Часть игры машины
    stockfish_move = stockfish.get_best_move_time(1000)
    stockfish_engine.make_move(stockfish, stockfish_move)

    prev_moves = ';'.join(filter(lambda x: x, (prev_moves, user_move, stockfish_move)))
    end_fen_pos = stockfish.get_fen_position()

    return make_json_response(
        StatusCodes.OK, 'OK',
        fen=end_fen_pos,
        stockfish_move=stockfish_move,
        prev_moves=prev_moves,
        orientation='w' if 'w' in end_fen_pos else 'b'
    )
