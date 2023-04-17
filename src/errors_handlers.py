import flask

from src.consts import StatusCodes
from src.utils.abort import CancelHandler
from src.utils.decorators import log
from src.utils.response import flask_json_response


# @app.errorhandler(StatusCodes.NOT_FOUND.value)
def not_found(_):
    return flask_json_response(
        StatusCodes.NOT_FOUND.value,
        'Not found'
    )


# @app.errorhandler(StatusCodes.INVALID_PARAMS.value)
def bad_request(_):
    return flask_json_response(
        StatusCodes.INVALID_PARAMS,
        'Bad Request'
    )


# @app.errorhandler(CancelHander)
@log(entry=False, output=False, with_entry_args=False, with_output_args=False, level='INFO')
def cancel_catcher(error: CancelHandler):
    return flask_json_response(
        **error.info
    )


# @app.errorhandler(Exception)
@log(entry=False, output=False, with_entry_args=False, with_output_args=False, level='ERROR')
def global_exception_catcher(error):
    return flask_json_response(
        StatusCodes.SERVER_ERROR,
        'Something went wrong. Probably invalid params',
        error=str(error)
    )


def register_error_handlers(app: flask.Flask):
    app.register_error_handler(StatusCodes.NOT_FOUND.value, not_found)
    app.register_error_handler(StatusCodes.INVALID_PARAMS.value, bad_request)
    app.register_error_handler(CancelHandler, cancel_catcher)
    app.register_error_handler(Exception, global_exception_catcher)
