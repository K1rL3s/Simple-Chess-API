from enum import Enum
from functools import cache

import flask

from src.consts import Limits, Defaults, StatusCodes
from src.utils.log_decorator import log_decorator
from src.utils.make_json_response import make_json_response

blueprint = flask.Blueprint(
    'api/chess/limits',
    __name__,
    template_folder='templates'
)


@cache
def to_dict(minimum: int | Enum, default: int | Enum, maximum: int | Enum) -> dict[str, int]:
    return {
        "min": minimum if isinstance(minimum, int) else minimum.value,
        "default": default if isinstance(default, int) else default.value,
        "max": maximum if isinstance(maximum, int) else maximum.value,
    }


@blueprint.route('/api/chess/limits/', methods=['GET'])
@log_decorator(entry=False, output=False, level='INFO')
@cache
def api_chess_limits():
    """
    Возвращает минимум, дефолт и максимум для числовых параметров генерации хода и рисования доски.
    Если где-то переименовать ключ (параметр), то и тут надо, а то будет не круто.
    """

    return make_json_response(
        StatusCodes.OK, 'OK',
        min_time=to_dict(
            Limits.MIN_THINK_MS,
            Defaults.THINK_MS,
            Limits.MAX_THINK_MS
        ),
        max_time=to_dict(
            Limits.MIN_THINK_MS,
            Defaults.THINK_MS,
            Limits.MAX_THINK_MS
        ),
        threads=to_dict(
            Limits.MIN_THREADS,
            Defaults.THREADS,
            Limits.MAX_THREADS
        ),
        depth=to_dict(
            Limits.MIN_DEPTH,
            Defaults.DEPTH,
            Limits.MAX_DEPTH
        ),
        ram_hash=to_dict(
            Limits.MIN_RAM_HASH,
            Defaults.RAM_HASH,
            Limits.MAX_RAM_HASH
        ),
        skill_level=to_dict(
            Limits.MIN_SKILL_LEVEL,
            Defaults.SKILL_LEVEL,
            Limits.MAX_SKILL_LEVEL
        ),
        elo=to_dict(
            Limits.MIN_ELO,
            Defaults.ELO,
            Limits.MAX_ELO
        ),
        size=to_dict(
            Limits.MIN_BOARD_IMAGE_SIZE,
            Defaults.BOARD_IMAGE_SIZE,
            Limits.MAX_BOARD_IMAGE_SIZE,
        )
    )
