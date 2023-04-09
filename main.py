from loguru import logger
from waitress import serve

from src import create_app


def main():
    app = create_app.init_app()
    host, port = '0.0.0.0', 5000
    logger.info(f'Running a Flask "Simple-Chess-API" on {host}:{port}')
    serve(app, host=host, port=port)


if __name__ == '__main__':
    main()
