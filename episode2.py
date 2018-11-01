import random
import itertools
import arcade

WALL_SIZE = 50
SPRITE_SCALING_COIN = 0.2
SPRITE_SCALING_PLAYER = 0.2
SPRITE_SCALING = 0.2

g = 9.81


class NewGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.player = arcade.Sprite("img/character.png",
                                    SPRITE_SCALING_PLAYER)
        self.drugs = arcade.SpriteList()
        self.healthy_food = arcade.SpriteList()

        self.hp = 0
        self.score = 0
        self.player.center_x = self.width / 2
        self.player.center_y = self.player.height / 2
        self.time_left = 0
        self.is_running = False


    def setup(self):
        while len(self.drugs):
            self.drugs.pop().kill()
        while len(self.healthy_food):
            self.healthy_food.pop().kill()

        self.hp = 3
        self.score = 0
        self.time_left = 30

        self.player.center_x = self.width / 2
        self.player.center_y = self.player.height / 2
        self.is_running = True

    def on_draw(self):
        arcade.start_render()
        self.player.draw()
        self.drugs.draw()
        self.healthy_food.draw()
        arcade.draw_rectangle_filled(
            center_x=self.width / 2,
            center_y=self.height - 30,
            width=self.width,
            height=60,
            color=(255, 255, 255),
        )
        arcade.draw_text(
            text=f'♥: {self.hp:2d}\t$: {self.score:5d}\t⏱: {self.time_left:5.1f}',
            start_x=10,
            start_y=self.height - 50,
            color=(255, 0, 0),
            font_size=36,
        )
        if not self.is_running:
            arcade.draw_text(
                text='Press space to start',
                start_x=10,
                start_y=self.height / 2,
                color=(255, 255, 255),
                font_size=36,
            )


    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player.change_x = - 10
        elif key == arcade.key.RIGHT:
            self.player.change_x = 10

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0
        elif key == arcade.key.SPACE and not self.is_running:
            self.setup()

    def update(self, dt):
        if self.is_running:
            self.time_left = max(0, self.time_left - dt)
            drugs_picked = arcade.check_for_collision_with_list(self.player,
                                                                self.drugs)
            healthy_food_eaten = arcade.check_for_collision_with_list(
                self.player, self.healthy_food
            )

            for drug in drugs_picked:
                self.score += drug.score
                drug.kill()

            for food in healthy_food_eaten:
                self.hp = max(0, self.hp - 1)
                food.kill()

        if self.is_running and (self.hp == 0 or self.time_left == 0):
            self.is_running = False
            if self.hp > 1:
                self.score *= self.hp

        new_player_x = self.player.center_x + self.player.change_x
        if 0 < new_player_x < self.width:
            self.player.center_x = new_player_x

        for item in itertools.chain(self.drugs, self.healthy_food):
            item.center_y -= item.velocity * dt
            item.velocity += g * dt

        if len(self.drugs) < 15 and random.randint(0, 100) < 10:
            drug = arcade.Sprite("img/coin.png", SPRITE_SCALING_COIN)
            drug.score = 1
            drug.velocity = random.randint(10, 25) * g
            drug.center_x = random.randint(0, self.width)
            drug.center_y = random.randint(self.height - 100, self.height)
            self.drugs.append(drug)

        if len(self.healthy_food) < 3 and random.randint(0, 100) < 5:
            food = arcade.Sprite("img/wall.png", SPRITE_SCALING)
            food.velocity = random.randint(15, 30) * g
            food.center_x = random.randint(0, self.width)
            food.center_y = random.randint(self.height - 100, self.height)
            self.healthy_food.append(food)

        for item in itertools.chain(self.drugs, self.healthy_food):
            if item.center_y < 0:
                item.kill()


if __name__ == "__main__":
    game = NewGame(600, 800)
    arcade.run()
