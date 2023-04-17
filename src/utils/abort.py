from typing import NoReturn

from src.consts import StatusCodes


class CancelHandler(Exception):
    def __init__(self, **kwargs):
        self.info = {
            'status_code': kwargs.get('status_code', StatusCodes.SERVER_ERROR),
            'message': kwargs.get('message', 'Unknown Error'),
        }


def abort(status_code: int | StatusCodes, message: str) -> NoReturn:
    raise CancelHandler(status_code=status_code, message=message)
