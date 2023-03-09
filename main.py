from __init__ import app
from src.api.make_a_move import register_make_a_move
from src.api.get_board_image import register_get_board_image


def main():
    register_make_a_move(app)
    register_get_board_image(app)
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
