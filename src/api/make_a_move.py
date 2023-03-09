import flask

# from chess import Termination

from src.consts import StatusCodes, Defaults
from src.api.json_response import make_json_response
from src.engine import engine


def make_a_move() -> flask.Response:
    """
    "Генератор" шахматных ходов.
    """
    data = flask.request.args
    prev_moves = str(data.get('prev_moves', '')).lower()
    next_move = str(data.get('next_move')).lower()
    orientation = str(data.get('orientation', 'w')).lower()
    threads = int(data.get('threads', Defaults.THREADS.value))
    depth = int(data.get('depth', Defaults.DEPTH.value))
    ram_hash = int(data.get('ram_hash', Defaults.RAM_HASH.value))
    skill_level = int(data.get('skill_level', Defaults.SKILL_LEVEL.value))
    elo = int(data.get('elo', Defaults.ELO.value))

    ram_hash = min(ram_hash, Defaults.RAM_HASH.value)

    # Обработка некорректных данных
    if not next_move and not prev_moves and orientation != 'b':
        # Если не задан ход, раньше ходов не было и игрок не игрет за чёрных
        # Нужно, чтобы машина играла белыми
        return make_json_response(StatusCodes.INVALID_PARAMS,
                                  'Invalid param "next_move"')

    if orientation not in ('w', 'b'):
        return make_json_response(StatusCodes.INVALID_PARAMS,
                                  'Invalid param "orientation". It must be "w" or "b".')

    if len(prev_moves) > 4 and ';' not in prev_moves:
        return make_json_response(StatusCodes.INVALID_PARAMS,
                                  'Invalid param "prev_moves". Between moves must be ";".')

    # Инициализация движка для игры, часть игры пользователя
    stockfish = engine.get_stockfish(threads, depth, ram_hash, skill_level, elo, prev_moves)
    if stockfish is None:
        return make_json_response(StatusCodes.INVALID_PARAMS,
                                  f'param "prev_moves" has illegal moves',
                                  fen_position='')

    start_fen_pos = stockfish.get_fen_position()
    if next_move:
        answer = engine.make_move(stockfish, next_move)
        if answer == StatusCodes.CONFLICT.value:
            return make_json_response(StatusCodes.CONFLICT,
                                      f'"{next_move}" is illegal move',
                                      fen_position=start_fen_pos)
        prev_moves += ';' + next_move

    # Часть игры машины
    stockfish_move = stockfish.get_best_move_time(1000)
    engine.make_move(stockfish, stockfish_move)

    prev_moves += ';' + stockfish_move
    prev_moves = prev_moves.strip(' ;')
    end_fen_pos = stockfish.get_fen_position()

    return make_json_response(StatusCodes.OK, 'OK',
                              fen_position=end_fen_pos,
                              stockfish_move=stockfish_move,
                              prev_moves=prev_moves,
                              orientation=orientation
                              )


def register_make_a_move(app: flask.Flask):
    app.add_url_rule('/make_a_move', view_func=make_a_move, methods=["GET"])
