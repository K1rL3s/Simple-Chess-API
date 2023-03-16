import json

import flask

from src.consts import StatusCodes


def make_json_response(
        status_code: int | StatusCodes,
        message: str,
        **params
) -> flask.Response:
    """
    Шаблон для ответов на запросы.

    :param status_code: Статус код ответа.
    :param message: Сообщение клиенту.
    :param params: Параметры, которые будут в словаре "response".
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
                "message": str(message),
                "response": {
                    **params
                },
            }
        ),
        status=status_code,
        mimetype='application/json'
    )

    return response
