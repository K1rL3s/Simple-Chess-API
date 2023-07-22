import flask
from pathlib import Path


blueprint = flask.Blueprint(
    'api/chess/docs',
    __name__,
    # Надо как-то лучше мб
    template_folder=Path(__file__).parent.parent.parent / 'templates'
)


@blueprint.route('/api/chess/docs/', methods=['GET'])
def api_chess_docs() -> flask.Response:
    """
    Вывод readme.md.
    """

    # Надо как-то лучше мб
    readme = Path(__file__).absolute().parent.parent.parent / 'README.md'

    with open(readme, 'r', encoding='utf-8') as f:
        return flask.Response(
            flask.render_template('docs.html', markdown_string=f.read())
        )
