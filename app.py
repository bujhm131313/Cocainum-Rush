import random

import arcade

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 900
WALL_SIZE = 50

RUSH_THRESHOLD = 100
DEATH_THRESHOLD = 10000


JUMP_SPEED = 65
MOVEMENT_SPEED = 15
SPRITE_SCALING_COIN = 0.2
SPRITE_SCALING_PLAYER = 0.2
SPRITE_SCALING = 0.2
COIN_COUNT = 10
GRAVITY = 5
HALLUCINATION_POWER = 0.02
HALLUCINATION_RELEASE = 0.0001


class MyGame(arcade.Window):
    """ Главный класс приложения. """

    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.BLUE_GRAY)
        self.frame_counter = 0

    def setup(self):
        """ Настроить игру и инициализировать переменные. """

        # Создать список спрайтов
        self.player_list = arcade.SpriteList()
        self.cocainum_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        self._add_cocainum()
        self._draw_walls()

        # Счет
        self.score = 0

        # Задать игрока и его изображение
        self.player_sprite = arcade.Sprite("img/character.png",
                                           SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 100  # Стартовая позиция
        self.player_sprite.center_y = 100
        self.player_sprite.height = 100
        self.player_sprite.width = 80
        self.player_list.append(self.player_sprite)

        self._draw_hallucination()

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, self.wall_list, gravity_constant=GRAVITY)

    def _add_cocainum(self):
        # Создать монетки
        for i in range(COIN_COUNT):
            # Создать инстанс монеток
            # и их изображение из kenney.nl
            coin = arcade.Sprite("img/coin.png", SPRITE_SCALING_COIN)

            # Задать положение монеток
            coin.center_x = random.randrange(100, SCREEN_WIDTH - 100)
            coin.center_y = random.randrange(100, SCREEN_HEIGHT)

            # Добавить монетку к списку
            self.cocainum_list.append(coin)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if self.score > DEATH_THRESHOLD:
            # You died and cannot move
            return

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
        self.frame_counter += 1
        self.hallucation.alpha -= HALLUCINATION_RELEASE

        arcade.start_render()
        self.cocainum_list.draw()
        self.wall_list.draw()
        self.player_list.draw()

        self._generate_hallucination()
        self.hallucation.draw()

        if self.score > DEATH_THRESHOLD:
            arcade.draw_text('COCAINUM OVERDOSE', 300, 500,
                             color=arcade.color.RED_DEVIL, font_size=70)
        elif self.score > RUSH_THRESHOLD:
            arcade.draw_text('COCAINUM RUSH', 300, 500,
                             color=arcade.color.RED_DEVIL, font_size=70)

    def update(self, delta_time):
        coins_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.cocainum_list)

        for coin in coins_hit_list:
            coin.kill()
            self.score += 1
            self.hallucation.alpha += HALLUCINATION_POWER

        self.physics_engine.update()
        if 0 < self.score < DEATH_THRESHOLD and self.score % COIN_COUNT == 0:
            self._add_cocainum()


    def _draw_walls(self):
        # create box
        for x in range(0, SCREEN_WIDTH + WALL_SIZE, WALL_SIZE):
            bottom_border = arcade.Sprite("img/wall.png", SPRITE_SCALING)
            top_border = arcade.Sprite("img/wall.png", SPRITE_SCALING)
            bottom_border.center_x = top_border.center_x = x
            bottom_border.center_y = 0
            top_border.center_y = SCREEN_HEIGHT
            self.wall_list.append(bottom_border)
            self.wall_list.append(top_border)

        for y in range(0, SCREEN_HEIGHT + WALL_SIZE, WALL_SIZE):
            left_border = arcade.Sprite("img/wall.png", SPRITE_SCALING)
            right_border = arcade.Sprite("img/wall.png", SPRITE_SCALING)
            left_border.center_y = right_border.center_y = y
            left_border.center_x = 0
            right_border.center_x = SCREEN_WIDTH
            self.wall_list.append(left_border)
            self.wall_list.append(right_border)

        # Put layers
        for x in range(0, SCREEN_WIDTH, 200):
            wall = arcade.Sprite("img/wall.png", SPRITE_SCALING)
            wall.center_x = x
            wall.center_y = 200
            self.wall_list.append(wall)

        for x in range(100, SCREEN_WIDTH, 200):
            wall = arcade.Sprite("img/wall.png", SPRITE_SCALING)
            wall.center_x = x
            wall.center_y = 400
            self.wall_list.append(wall)

        for x in range(100, SCREEN_WIDTH, 200):
            wall = arcade.Sprite("img/wall.png", SPRITE_SCALING)
            wall.center_x = x
            wall.center_y = 600
            self.wall_list.append(wall)

        for x in range(0, SCREEN_WIDTH, 200):
            wall = arcade.Sprite("img/wall.png", SPRITE_SCALING)
            wall.center_x = x
            wall.center_y = 800
            self.wall_list.append(wall)

    def _draw_hallucination(self):
        self.hallucation = arcade.Sprite("img/catdrugs.jpg", 3)
        self.hallucation.alpha = 0
        self.hallucation.center_x = SCREEN_WIDTH / 2
        self.hallucation.center_y = SCREEN_HEIGHT / 2

    def _generate_hallucination(self):
        INTERVAL = 400
        ANGLE_SPEED_K = 4
        HALLUCINATION_SIZE_SPEED_K = 5

        x = self.frame_counter % INTERVAL
        delta = random.random() if x > INTERVAL / 2 else -random.random()
        self.hallucation.center_x += delta
        delta = random.random() if x < INTERVAL / 2 else -random.random()
        self.hallucation.center_y += delta
        self.hallucation._angle += delta / ANGLE_SPEED_K
        self.hallucation.width += delta * HALLUCINATION_SIZE_SPEED_K
        self.hallucation.height -= delta * HALLUCINATION_SIZE_SPEED_K


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
