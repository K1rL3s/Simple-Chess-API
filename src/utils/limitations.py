from src.consts import Limits


def limit_min_max(value: int, minimum: int, maximum: int) -> int:
    return int(
        max(
            min(value, maximum),
            minimum
        )
    )


def limit_engine_params(
        min_time: int = 0,
        threads: int = 0,
        depth: int = 0,
        ram_hash: int = 0,
        skill_level: int = 0,
        elo: int = 0,
) -> tuple[int, int, int, int, int, int]:
    """
    Нормализует значения, передаваемые в /api/chess/move.

    :param min_time: Минимальное время на подумать.
    :param threads: Количество потоков.
    :param depth: Глубина просчёта ходов.
    :param ram_hash: Количество оперативной памяти.
    :param skill_level: Уровень игры.
    :param elo: Количество ЭЛО.
    :return: Передаваемые значения, ограниченные src.consts.Limits
    """

    min_time = limit_min_max(
        min_time, Limits.MIN_THINK_MS.value, Limits.MAX_THINK_MS.value
    )
    # max_time должно ограничиваться в другом месте :(

    threads = limit_min_max(
        threads, Limits.MIN_THREADS.value, Limits.MAX_THREADS.value
    )

    depth = limit_min_max(
        depth, Limits.MIN_DEPTH.value, Limits.MAX_DEPTH.value
    )

    ram_hash = limit_min_max(
        ram_hash, Limits.MIN_RAM_HASH.value, Limits.MAX_RAM_HASH.value
    )

    skill_level = limit_min_max(
        skill_level, Limits.MIN_SKILL_LEVEL.value, Limits.MAX_SKILL_LEVEL.value
    )

    elo = limit_min_max(
        elo, Limits.MIN_ELO.value, Limits.MAX_ELO.value
    )

    return min_time, threads, depth, ram_hash, skill_level, elo


def limit_board_params(
        size: int = 0
) -> tuple[int] | int:
    """
    Нормализует значения, передаваемые в /api/chess/board.

    :param size: Размер стороны квадратного изображения в пикселях.
    :return: Передаваемые значения, ограниченные src.consts.Limits
    """

    size = limit_min_max(
        size,
        Limits.MIN_BOARD_IMAGE_SIZE.value,
        Limits.MAX_BOARD_IMAGE_SIZE.value
    )

    return size
