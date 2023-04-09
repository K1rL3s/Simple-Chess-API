import flask

from src.consts import StatusCodes
from src.utils.make_json_response import make_json_response


# @app.errorhandler(StatusCodes.NOT_FOUND.value)
def not_found(_):
    return make_json_response(
        StatusCodes.NOT_FOUND.value,
        'Not found'
    )


# @app.errorhandler(StatusCodes.INVALID_PARAMS.value)
def bad_request(_):
    return make_json_response(
        StatusCodes.INVALID_PARAMS,
        'Bad Request'
    )


# @app.errorhandler(Exception)
def global_exception_catcher(error):
    return make_json_response(
        StatusCodes.SERVER_ERROR,
        'Something went wrong. Probably invalid params',
        error=str(error)
    )


def register_error_handlers(app: flask.Flask):
    app.register_error_handler(StatusCodes.NOT_FOUND.value, not_found)
    app.register_error_handler(StatusCodes.INVALID_PARAMS.value, not_found)
    app.register_error_handler(Exception, not_found)
