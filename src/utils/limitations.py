from src.consts import Limits


def limit_engine_params(
        threads: int = 0,
        depth: int = 0,
        ram_hash: int = 0,
        skill_level: int = 0,
        elo: int = 0,
) -> tuple[int, int, int, int, int]:
    """
    Нормализует значения, передаваемые в /api/chess/move.

    :param threads: Количество потоков.
    :param depth: Глубина просчёта ходов.
    :param ram_hash: Количество оперативной памяти.
    :param skill_level: Уровень игры.
    :param elo: Количество ЭЛО.
    :return: Передаваемые значения, ограниченные src.consts.Limits
    """

    threads = max(min(threads, Limits.MAX_THREADS.value), Limits.MIN_THREADS.value)
    depth = max(min(depth, Limits.MAX_DEPTH.value), Limits.MIN_DEPTH.value)
    ram_hash = max(min(ram_hash, Limits.MAX_RAM_HASH.value), Limits.MIN_RAM_HASH.value)
    skill_level = max(min(skill_level, Limits.MAX_SKILL_LEVEL.value), Limits.MIN_SKILL_LEVEL.value)
    elo = max(min(elo, Limits.MAX_ELO.value), Limits.MIN_ELO.value)

    return threads, depth, ram_hash, skill_level, elo


def limit_board_params(
        size: int = 0
) -> tuple[int] | int:
    """
    Нормализует значения, передаваемые в /api/chess/board.

    :param size: Размер стороны квадратного изображения в пикселях.
    :return: Передаваемые значения, ограниченные src.consts.Limits
    """

    size = max(min(size, Limits.MAX_BOARD_IMAGE_SIZE.value), Limits.MIN_BOARD_IMAGE_SIZE.value)

    return size
