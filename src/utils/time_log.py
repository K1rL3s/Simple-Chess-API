from time import time


def log_run_time(func):
    function_name = getattr(func, 'func_name', None) or getattr(func, '__name__', None) or '<undefined>'

    def wrapper(*args, **kwargs):
        nonlocal function_name
        start = time()
        result = func(*args, **kwargs)
        total = time() - start
        print(f'{function_name} took {total:.3f} secs')
        return result
    return wrapper
