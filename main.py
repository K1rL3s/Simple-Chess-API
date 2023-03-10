from waitress import serve

import create_app


def main():
    create_app.init_app()
    host, port = '0.0.0.0', 5000
    print(f'Running a {__name__} on {host}:{port}.')
    serve(create_app.app, host=host, port=port)


if __name__ == '__main__':
    main()
