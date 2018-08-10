import arcade

from py_game.helpers.render_helpers import render
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
NAME = 'HALO'


def draw_circle():
    x = 300
    y = 300
    radius = 200
    arcade.draw_circle_filled(x, y, radius, arcade.color.YALE_BLUE)


@render(SCREEN_WIDTH, SCREEN_HEIGHT, NAME)
def main():
    if __name__ == '__main__':
        draw_circle()


main()
