from loguru import logger
from waitress import serve

from src import create_app
from src.consts import Config


def main():
    app = create_app.init_app()
    logger.info(f'Running a Flask "Simple-Chess-API" on {Config.HOST}:{Config.PORT}')
    serve(app, host=Config.HOST, port=Config.PORT)
    logger.info(f'Stop a Flask "Simple-Chess-API" on {Config.HOST}:{Config.PORT}')


if __name__ == '__main__':
    main()
