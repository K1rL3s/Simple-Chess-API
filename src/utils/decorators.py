import functools
from time import time

import flask
from loguru import logger

from src.consts import Config
from src.consts import StatusCodes
from src.utils.abort import abort


def log(
        entry: bool = True,
        output: bool = True,
        with_time: bool = True,
        with_entry_args: bool = True,
        with_output_args: bool = True,
        level: str = "DEBUG"
):
    """
    Логгер выполнения функции.
    :param entry: Выводить ли входные данные.
    :param output: Выводить ли выходные данные.
    :param with_time: Выводить ли время выполнения (и flask.Response).
    :param with_entry_args: Выводить ли входные аргументы.
    :param with_output_args: Выводить ли выходные аргументы.
    :param level: Уровень отображения.
    """

    def wrapper(func):
        function_name = (
                getattr(func, 'func_name', None)
                or getattr(func, '__name__', None)
                or '<undefined>'
        )

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            logger_ = logger.opt(depth=1)

            if entry:
                message = f'Вызов "{function_name}"'
                if with_entry_args:
                    message += f' ({args=}, {kwargs=})'
                logger_.log(level, message)

            start = time()
            result = func(*args, **kwargs)
            total = time() - start

            try:
                message = result.json.get('message')
            except AttributeError:
                message = None

            if output:
                message = f'Конец "{function_name}"'
                if with_output_args:
                    message += f' ({result=})'
                logger_.log(level, message)

            if with_time:
                request = getattr(flask, 'request', None)
                remote_addr = (request.remote_addr
                               if isinstance(request, flask.Request)
                               else 'Python')
                info = f"{remote_addr:<15} | " \
                       f"{f'{function_name} took {total:.3f} secs':<40}"

                if isinstance(result, flask.Response):
                    info += f' | {result.status_code} - {message}'

                logger_.log(level, info.strip())

            return result

        return wrapped

    return wrapper


def requires_auth(func):
    """
    Декоратор для примитивной авторизации в апишке по заранее заданному
    секретному ключу.
    Ключ один, хранится и у сервера, и у пользователя.
    Если у сервера нет ключа, то доступ у всех через всё.
    """

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        auth_header = flask.request.headers.get('Authorization', '')

        if Config.API_AUTH_KEY and auth_header != Config.API_AUTH_KEY:
            abort(StatusCodes.NOT_AUTH, 'Authorization key missing or invalid')
            return

        return func(*args, **kwargs)

    return wrapped
