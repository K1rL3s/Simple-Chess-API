from loguru import logger
from waitress import serve

from src import create_app
from src.consts import Config


def main():
    """
    Ищите комментарии в коде и readme.md! :)
    """
    app = create_app.init_app()
    create_app.init_box_with_engines()

    logger.info(f'Running a Flask "Simple-Chess-API" on {Config.HOST}:{Config.PORT}')
    serve(app, host=Config.HOST, port=Config.PORT, threads=Config.APP_THREADS)
    logger.info(f'Stop a Flask "Simple-Chess-API" on {Config.HOST}:{Config.PORT}')


if __name__ == '__main__':
    main()
