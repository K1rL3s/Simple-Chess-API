import os
from enum import Enum

from dotenv import load_dotenv


load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    ENGINE_PATH = os.environ['STOCKFISH_ENGINE_PATH']
    # В `.env` оставить пустым или не писать вообще, если без авторизации
    API_AUTH_KEY = os.environ.get("API_AUTH_KEY")


# Сервер автора не самый сильный, поэтому он сделал такие крутые ограничения
class Defaults(Enum):
    THINK_MS = 1000
    THREADS = 1
    DEPTH = 15
    RAM_HASH = 128
    SKILL_LEVEL = 20
    ELO = 3620
    BOARD_IMAGE_SIZE = 1024


class Limits(Enum):
    MAX_THINK_MS = 5000
    MAX_THREADS = 2
    MAX_DEPTH = 20
    MAX_RAM_HASH = 512
    MAX_SKILL_LEVEL = 20
    MAX_ELO = 3620
    MAX_BOARD_IMAGE_SIZE = 1024

    MIN_THREADS = 1
    MIN_DEPTH = 5
    MIN_RAM_HASH = 32
    MIN_SKILL_LEVEL = 1
    MIN_ELO = 100
    MIN_BOARD_IMAGE_SIZE = 1
    MIN_THINK_MS = 100


class StatusCodes(Enum):
    OK = 200
    INVALID_PARAMS = 400
    NOT_AUTH = 403
    NOT_FOUND = 404
    SERVER_ERROR = 500


class RequestsParams(Enum):
    YES = ('t', '1', 'true')
    NO = ('f', '0', 'false')
    YES_OR_NO = (*YES, *NO)
    WHITE = ('w', 'white')
    BLACK = ('b', 'black')
    COLORS = (*WHITE, *BLACK)


class TerminatorTypes(Enum):
    CHECKMATE = 'checkmate'
    STALEMATE = 'stalemate'
    INSUFFICIENT_MATERIAL = 'insufficient_material'


# http://kvetka.org/Stockfish_opt.shtml#slow_m
engine_params = {
    "Debug Log File": "",
    "Contempt": 0,  # Склонность к принятию ничьи. Больше нуля - более благосклонен. [-100; 100]
    "Min Split Depth": 0,
    "Threads": Defaults.THREADS.value,  # Больше - сильнее. Должно быть меньше, чем доступно на пк.
    "Ponder": "false",
    "Hash": Defaults.RAM_HASH.value,  # Кол-во оперативный памяти в МБ. Должно быть степенью двойки.
    "MultiPV": 1,  # Сколько рекомендуемых ходов выводить движку.
    "Skill Level": Defaults.SKILL_LEVEL.value,  # Сила движка от 1 до 20
    "Move Overhead": 0,
    "Minimum Thinking Time": Limits.MIN_THINK_MS.value,  # Минимальное время на подумать движку.
    "Slow Mover": 10,
    "UCI_Chess960": "false",
    "UCI_LimitStrength": "false",
    "UCI_Elo": Defaults.ELO.value
}
