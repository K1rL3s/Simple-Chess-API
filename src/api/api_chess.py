import flask

blueprint = flask.Blueprint(
    'api/chess',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/chess/', methods=['GET'])
@blueprint.route('/', methods=['GET'])
def api_chess_docs():
    """
    Вывод readme.md.
    """
    return flask.redirect('/api/chess/docs/')
