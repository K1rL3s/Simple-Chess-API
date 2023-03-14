from waitress import serve
from dotenv import load_dotenv

load_dotenv()


def main():
    import create_app
    create_app.init_app()
    host, port = '0.0.0.0', 5000
    print(f'Running a "chess-api" on {host}:{port}.')
    serve(create_app.app, host=host, port=port)


if __name__ == '__main__':
    main()
