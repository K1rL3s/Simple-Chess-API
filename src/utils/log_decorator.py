from time import time

import flask


def log_decorator(func):
    """
    Простая функция для засечения времени ответа на запрос.
    """

    function_name = getattr(func, 'func_name', None) or getattr(func, '__name__', None) or '<undefined>'

    def wrapper(*args, **kwargs):
        nonlocal function_name
        start = time()
        result: flask.Response = func(*args, **kwargs)

        try:
            message = result.json.get('message')
        except Exception:
            message = None

        total = time() - start
        print(f"{f'{function_name} took {total:.3f} secs':<40} | {result.status_code} - {message}")
        return result
    return wrapper
