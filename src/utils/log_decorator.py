import functools
from time import time

import flask
from loguru import logger


def log_decorator(entry: bool = True, output: bool = True, level: str = "DEBUG"):
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

            info = f"{f'{function_name} took {total:.3f} secs':<40}"
            if isinstance(result, flask.Response):
                info += f' | {result.status_code} - {message}'

            logger_.log(level, info.strip())

            return result

        return wrapped

    return wrapper
