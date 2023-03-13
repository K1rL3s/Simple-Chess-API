from enum import Enum


# Сервер автора не самый сильный, поэтому он сделал такие крутые ограничения
class Defaults(Enum):
    THREADS = 2
    DEPTH = 15
    RAM_HASH = 512
    SKILL_LEVEL = 20
    ELO = 2000
    BOARD_IMAGE_SIZE = 240


class Limits(Enum):
    MAX_THREADS = 2
    MAX_DEPTH = 20
    MAX_RAM_HASH = 1024
    MAX_SKILL_LEVEL = 20
    MAX_ELO = 3620
    MAX_BOARD_IMAGE_SIZE = 1024

    MIN_THREADS = 1
    MIN_DEPTH = 5
    MIN_RAM_HASH = 64
    MIN_SKILL_LEVEL = 5
    MIN_ELO = 100
    MIN_BOARD_IMAGE_SIZE = 1


class StatusCodes(Enum):
    OK = 200
    INVALID_PARAMS = 400
    NOT_FOUND = 404
    SERVER_ERROR = 500


# http://kvetka.org/Stockfish_opt.shtml#slow_m
engine_params = {
    "Debug Log File": "",
    "Contempt": 0,  # Склонность к принятию ничьи. Больше нуля - более благосклонен. [-100; 100]
    "Min Split Depth": 0,
    "Threads": Defaults.THREADS.value,  # Больше - сильнее. Должно быть меньше, чем доступно на пк.
    "Ponder": "false",
    "Hash": Defaults.RAM_HASH.value,  # Кол-во оперативный памяти в МБ. Должно быть степенью двойки.
    "MultiPV": 3,  # Сколько рекомендуемых ходов выводить движку.
    "Skill Level": Defaults.SKILL_LEVEL.value,  # Сила движка от 1 до 20
    "Move Overhead": 0,
    "Minimum Thinking Time": 0,  # Минимальное время на подумать движку (уменьшить?).
    "Slow Mover": 100,
    "UCI_Chess960": "false",
    "UCI_LimitStrength": "false",
    "UCI_Elo": Defaults.ELO.value
}
