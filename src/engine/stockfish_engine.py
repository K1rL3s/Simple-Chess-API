import contextlib
import queue

import chess
from loguru import logger
from stockfish import Stockfish

from src.consts import TerminatorTypes, Config, engine_params, Defaults, StatusCodes
from src.utils.abort import abort, AbortError
from src.utils.decorators import log
from src.utils.limitations import limit_engine_params


class BoxWithEngines:
    def __init__(self, n: int):
        """
        "Коробка с движками", которая занимается распределение движков по потокам.

        :param n: Сколько движков хранить в очереди.
        """

        self._worker_queue = queue.Queue()

        for i in range(n):
            self._worker_queue.put(
                Stockfish(
                    path=Config.ENGINE_PATH,
                    depth=Defaults.DEPTH.value,
                    parameters=engine_params
                )
            )

    @contextlib.contextmanager
    def get_engine(
            self,
            prev_moves: str | None = None,
            prepared: bool | None = False,
            *args,
            **kwargs,
    ) -> Stockfish:
        """
        Контекстный менеджер, гарантирующий, что движок вернётся в очередь.
        Если не будет доступных движков, то мы просто будем ждать на .get(block=True).
        Аргументы к функции `get_stockfish`.
        """

        if not prepared:
            yield get_stockfish(*args, **kwargs, prev_moves=prev_moves)
            return

        if not Config.PREPARED_ENGINES:
            return abort(StatusCodes.NO_PREPARED_ENGINES, 'There are no prepared engines on server')

        engine = self._worker_queue.get(block=True)
        try:
            reset_params(engine)
            set_position_by_moves(engine, prev_moves)
            yield engine
        except AbortError as e:  # Если суета с отменой обработки, то движка это не касается
            raise e
        except Exception:  # noqa
            logger.error('Error on engine processing', exc_info=True)
        finally:
            self._worker_queue.put(engine)



@log(entry=True, output=True,
     with_entry_args=True, with_output_args=True,
     with_time=True, level='DEBUG')
def get_stockfish(
        min_time: int = Defaults.THINK_MS.value,
        threads: int = Defaults.THREADS.value,
        depth: int = Defaults.DEPTH.value,
        ram_hash: int = Defaults.RAM_HASH.value,
        skill_level: int = Defaults.SKILL_LEVEL.value,
        elo: int = Defaults.ELO.value,
        prev_moves: str = None
) -> Stockfish | StatusCodes:
    """
    Возвращает instance stockfish.Stockfish с указанными параметрами.

    :param min_time: = Минимальное время движку на подумать.
    :param threads: Потоки для работы движка. Больше - сильнее. Должно быть меньше, чем доступно на пк.
    :param depth: Глубина продумывания ходов.
    :param ram_hash: Кол-во оперативный памяти в МБ. Должно быть степенью двойки.
    :param skill_level: Уровень скилла от 1 до 20.
    :param elo: Шахматный рейтинг Эло.
    :param prev_moves: Предыдущие ходы в формате "e2e4;e7e5;...".
    :return: stockfish.Stockfish.
    """

    min_time, threads, depth, ram_hash, skill_level, elo = limit_engine_params(
        min_time, threads, depth, ram_hash, skill_level, elo
    )

    new_params = engine_params.copy()
    new_params.update({
        "Minimum Thinking Time": min_time,
        "Threads": threads,
        "Hash": ram_hash,
        "Skill Level": skill_level,
        "UCI_Elo": elo
    })
    engine = Stockfish(
        path=Config.ENGINE_PATH,
        depth=depth,
        parameters=new_params
    )

    set_position_by_moves(engine, prev_moves)

    return engine


def set_position_by_moves(engine: Stockfish, prev_moves: str | None = None) -> None:
    if prev_moves:
        for move in prev_moves.split(';'):
            answer = make_move(engine, move)
            if answer == StatusCodes.INVALID_PARAMS:
                abort(StatusCodes.INVALID_PARAMS, '"prev_moves" param has illegal moves')


def reset_params(engine: Stockfish) -> None:
    engine.set_fen_position(Config.START_FEN)


def make_move(
        engine: Stockfish,
        move: str,
        is_stockfish: bool = False
) -> tuple[str | None, str | None] | StatusCodes:
    """
    Делатель хода. Обновляет engine, делая новый ход из текущего положения.

    :param engine: Движок.
    :param move: Ход формата "e2e4".
    :param is_stockfish: Делает ли ход сам движок.
    :return: Состояние, по которому закончилась игра, или статус-код ошибки.
    """

    # Движок может выдать пустую строку вместо хода, если игра закончилась
    if not is_stockfish and not engine.is_move_correct(move):
        return StatusCodes.INVALID_PARAMS

    if move:
        engine.make_moves_from_current_position([move])

    terminator = is_game_over(engine.get_fen_position())
    if terminator == chess.Termination.CHECKMATE:
        terminator = TerminatorTypes.CHECKMATE.value
    elif terminator == chess.Termination.STALEMATE:
        terminator = TerminatorTypes.STALEMATE.value
    elif terminator == chess.Termination.INSUFFICIENT_MATERIAL:
        terminator = TerminatorTypes.INSUFFICIENT_MATERIAL.value
    else:
        terminator = None

    board = chess.Board(fen := engine.get_fen_position())
    if board.is_check():
        check = chess.square_name(board.king(chess.WHITE if 'w' in fen else chess.BLACK))
    else:
        check = None

    return terminator, check


def is_game_over(fen: str) -> chess.Termination | None:
    """
    Проверка на конец игры.

    :param fen: FEN позиция.
    :return: Состояние, по которому закончилась игра, или None (не закончилась).
    """

    outcome = chess.Board(fen).outcome()
    if outcome is not None:
        return outcome.termination
    return None
