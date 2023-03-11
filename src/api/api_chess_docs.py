import flask

blueprint = flask.Blueprint(
    'api/chess/docs',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/chess/docs/', methods=['GET'])
def api_chess_docs():
    """
    Вывод readme.md.
    """
    with open('./readme.md', 'r', encoding='utf-8') as f:
        return flask.render_template('docs.html', markdown_string=f.read())
