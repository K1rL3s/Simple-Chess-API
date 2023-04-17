import flask

blueprint = flask.Blueprint(
    'api/chess',
    __name__,
)


@blueprint.route('/api/chess/', methods=['GET'])
@blueprint.route('/', methods=['GET'])
def api_chess():
    """
    Переадресация на вывод readme.md.
    """
    return flask.redirect('/api/chess/docs/')
