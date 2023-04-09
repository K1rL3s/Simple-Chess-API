import functools
from time import time

import flask
from loguru import logger

from src.consts import Config
from src.consts import StatusCodes
from src.utils.make_json_response import make_json_response


def log(entry: bool = True, output: bool = True, level: str = "DEBUG"):
    """
    Логгер выполнения функции.
    :param entry: Выводить ли входные данные.
    :param output: Выводить ли выходные данные.
    :param level: Уровень отображения.
    """

    def wrapper(func):
        function_name = getattr(func, 'func_name', None) or getattr(func, '__name__', None) or '<undefined>'

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            logger_ = logger.opt(depth=1)

            if entry:
                logger_.log(level, f'Вызов "{function_name}" (args={args}, kwargs={kwargs})')

            start = time()
            result: flask.Response = func(*args, **kwargs)
            total = time() - start

            try:
                message = result.json.get('message')
            except AttributeError:
                message = None

            if output:
                logger_.log(level, f'Результат "{function_name}" (result={result})')
            info = f"{flask.request.remote_addr:<15} | {f'{function_name} took {total:.3f} secs':<40}"
            if isinstance(result, flask.Response):
                info += f' | {result.status_code} - {message}'

            logger_.log(level, info.strip())

            return result

        return wrapped

    return wrapper


def requires_auth(func):
    """
    Декоратор для примитивной авторизации в апишке по заранее заданному секретному ключу.
    Ключ один, хранится и у сервера, и у пользователя.
    Если у сервера нет ключа, то доступ у всех через всё.
    """

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        auth_header = flask.request.headers.get('Authorization', '')

        if Config.API_AUTH_KEY and auth_header != Config.API_AUTH_KEY:
            return make_json_response(StatusCodes.NOT_AUTH, 'Authorization key missing or invalid')

        return func(*args, **kwargs)

    return wrapped
