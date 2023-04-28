import flask
from loguru import logger

from src.consts import StatusCodes
from src.utils.abort import AbortError
from src.utils.decorators import log
from src.utils.response import flask_json_response


# @app.errorhandler(StatusCodes.NOT_FOUND.value)
def not_found(_):
    """
    Обработчик 404 ошибки Flask'а.
    """
    return flask_json_response(
        StatusCodes.NOT_FOUND.value,
        'Not found'
    )


# @app.errorhandler(StatusCodes.INVALID_PARAMS.value)
def bad_request(error):
    """
    Не уверен, используется ли оно вообще.
    """
    return flask_json_response(
        StatusCodes.INVALID_PARAMS,
        'Bad Request ' + str(error)
    )


# @app.errorhandler(AbortError)
@log(
    entry=False,
    output=False,
    with_entry_args=False,
    with_output_args=False,
    level='INFO'
)
def abort_catcher(error: AbortError):
    """
    Обработчик отмены ответа на запрос пользователя.
    """
    return flask_json_response(
        **error.info
    )


# @app.errorhandler(Exception)
def global_exception_catcher(error):
    """
    Обработчик для всех ошибок, которые я не знаю.
    """
    logger.error(str(error))
    return flask_json_response(
        StatusCodes.SERVER_ERROR,
        'Something went wrong. Probably invalid params',
        error=str(error)
    )


def register_error_handlers(app: flask.Flask):
    app.register_error_handler(StatusCodes.NOT_FOUND.value, not_found)
    app.register_error_handler(StatusCodes.INVALID_PARAMS.value, bad_request)
    app.register_error_handler(AbortError, abort_catcher)
    app.register_error_handler(Exception, global_exception_catcher)
