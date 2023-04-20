import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()


class Config:
    # Путь к исполняемому файлу двжика, именно он
    ENGINE_PATH = os.environ['ENGINE_PATH']

    # В `.env` оставить пустым или не писать вообще, если без авторизации
    API_AUTH_KEY = os.getenv("API_AUTH_KEY")
    SECRET_KEY = os.getenv('SECRET_KEY')
    HOST = os.getenv('HOST') or '127.0.0.1'
    PORT = int(os.getenv("PORT") or 5000)
    APP_THREADS = int(os.getenv("APP_THREADS") or 4)

    # В `.env` задать кол-во заготовленных движков.
    PREPARED_ENGINES = int(os.getenv("PREPARED_ENGINES") or 0)
    START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    # В эту переменную помещается BoxWithEngines в main.py,
    # вызывая src.create_app.init_box_with_engines.
    BOX = None


# Сервер автора не самый сильный, поэтому он сделал такие крутые ограничения
# Эти настройки используются для заготовленных движков, но можно создать отдельный класс.
class Defaults(Enum):
    THINK_MS = 1000
    THREADS = 1
    DEPTH = 20
    RAM_HASH = 64  # На Windows 11 едят по 64мб минимум, плюс это значение
    SKILL_LEVEL = 20
    ELO = 3620
    BOARD_IMAGE_SIZE = 1024
    START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


class Limits(Enum):
    MAX_THINK_MS = 5000
    MAX_THREADS = 2
    MAX_DEPTH = 20
    MAX_RAM_HASH = 128
    MAX_SKILL_LEVEL = 20
    MAX_ELO = 3620
    MAX_BOARD_IMAGE_SIZE = 1024

    MIN_THREADS = 1
    MIN_DEPTH = 1
    MIN_RAM_HASH = 8
    MIN_SKILL_LEVEL = 1
    MIN_ELO = 100
    MIN_BOARD_IMAGE_SIZE = 1
    MIN_THINK_MS = 100


class StatusCodes(Enum):
    OK = 200
    INVALID_PARAMS = 400
    NOT_AUTH = 403
    NOT_FOUND = 404
    NO_PREPARED_ENGINES = 409
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


# http://kvetka.org/Stockfish_opt.shtml
engine_params = {
    "Debug Log File": "",
    "Contempt": 0,  # Склонность к принятию ничьи. Больше нуля - более благосклонен. [-100; 100]
    "Min Split Depth": 0,
    "Threads": Defaults.THREADS.value,  # Больше - сильнее. Должно быть меньше, чем доступно на пк.
    "Ponder": "false",
    "Hash": Defaults.RAM_HASH.value,  # Кол-во оперативной памяти в МБ. Рекомендуется степень двойки.
    "MultiPV": 1,  # Сколько рекомендуемых ходов выводить движку.
    "Skill Level": Defaults.SKILL_LEVEL.value,  # Сила движка от 1 до 20
    "Move Overhead": 0,
    "Minimum Thinking Time": Limits.MIN_THINK_MS.value,  # Минимальное время на подумать движку.
    "Slow Mover": 10,  # Минимум
    "UCI_Chess960": "false",
    "UCI_LimitStrength": "false",
    "UCI_Elo": Defaults.ELO.value
}
