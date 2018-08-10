import random

import arcade

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 900

JUMP_SPEED = 65
MOVEMENT_SPEED = 15
SPRITE_SCALING_COIN = 0.2
SPRITE_SCALING_PLAYER = 0.2
SPRITE_SCALING = 0.2
COIN_COUNT = 10
GRAVITY = 5


class MyGame(arcade.Window):
    """ Главный класс приложения. """

    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.BLUE_GRAY)

    def setup(self):
        """ Настроить игру и инициализировать переменные. """

        # Создать список спрайтов
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # Счет
        self.score = 0

        # Задать игрока и
        # Его изображение из kenney.nl
        self.player_sprite = arcade.Sprite("img/character.png",
                                           SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 0  # Стартовая позиция
        self.player_sprite.center_y = 0
        self.player_sprite.height = 100
        self.player_sprite.width = 70
        self.player_list.append(self.player_sprite)

        # Создать монетки
        for i in range(COIN_COUNT):
            # Создать инстанс монеток
            # и их изображение из kenney.nl
            coin = arcade.Sprite("img/coin.png", SPRITE_SCALING_COIN)

            # Задать положение монеток
            coin.center_x = random.randrange(100, SCREEN_WIDTH - 100)
            coin.center_y = random.randrange(100, SCREEN_HEIGHT)

            # Добавить монетку к списку
            self.coin_list.append(coin)

        self._draw_walls()

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, self.wall_list, gravity_constant=GRAVITY)


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.player_sprite.change_y = JUMP_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
                self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Вызывается, когда пользователь отпускает клавишу"""

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_draw(self):
        """ Отрендерить этот экран. """
        arcade.start_render()
        self.coin_list.draw()
        self.wall_list.draw()
        self.player_list.draw()
        text = arcade.draw_text('score: {}'.format(self.score), 30, 800, color=arcade.color.RED_DEVIL, font_size=70)

    def update(self, delta_time):
        coins_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.coin_list)

        for coin in coins_hit_list:
            coin.kill()
            self.score += 1

        self.physics_engine.update()

        if self.score == COIN_COUNT:
            arcade.draw_text('GAME OVER YOU LOST', 500, 500,
                             color=arcade.color.RED_DEVIL, font_size=70)

    def _draw_walls(self):
        for x in range(-2000, 2000, 50):
            wall = arcade.Sprite("img/wall.png", SPRITE_SCALING)
            wall.center_x = x
            wall.center_y = 0
            self.wall_list.append(wall)

        for x in range(-1900, 2000, 200):
            wall = arcade.Sprite("img/wall.png", SPRITE_SCALING)
            wall.center_x = x
            wall.center_y = 200
            self.wall_list.append(wall)

        for x in range(-2000, 2000, 200):
            wall = arcade.Sprite("img/wall.png", SPRITE_SCALING)
            wall.center_x = x
            wall.center_y = 400
            self.wall_list.append(wall)

        for x in range(-2000, 2000, 200):
            wall = arcade.Sprite("img/wall.png", SPRITE_SCALING)
            wall.center_x = x
            wall.center_y = 600
            self.wall_list.append(wall)

        for x in range(-1900, 2000, 200):
            wall = arcade.Sprite("img/wall.png", SPRITE_SCALING)
            wall.center_x = x
            wall.center_y = 800
            self.wall_list.append(wall)


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()