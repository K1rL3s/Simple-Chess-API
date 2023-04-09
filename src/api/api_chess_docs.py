import flask
from pathlib import Path

blueprint = flask.Blueprint(
    'api/chess/docs',
    __name__,
    template_folder=Path(__file__).parent.parent.parent / 'templates'  # Надо как-то лучше мб
)


@blueprint.route('/api/chess/docs/', methods=['GET'])
def api_chess_docs():
    """
    Вывод readme.md.
    """

    readme = Path(__file__).absolute().parent.parent.parent / 'readme.md'  # Надо как-то лучше мб

    with open(readme, 'r', encoding='utf-8') as f:
        return flask.render_template('docs.html', markdown_string=f.read())
