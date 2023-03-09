import json

import flask

from src.consts import StatusCodes


def make_json_response(
        status_code: int | StatusCodes,
        text: str,
        **params
) -> flask.Response:
    """

    :param status_code:
    :param text:
    :param params:
    :return:
    """

    if isinstance(status_code, StatusCodes):
        status_code: int = status_code.value

    if not isinstance(status_code, int):
        raise TypeError(f'"status_code" param must be integer.')

    response = flask.Flask.response_class(
        response=json.dumps(
            {
                "status_code": status_code,
                "response": {
                    "message": str(text),
                    **params
                },
            }
        ),
        status=status_code,
        mimetype='application/json'
    )

    return response
