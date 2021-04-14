import random
import arcade

# --- Constants ---
SPRITE_SCALING_COIN = 0.2
SPRITE_SCALING_ENEMY = 1
COIN_COUNT = 50
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# --- Other Variables ---
sprite_scaling_player = 0.15
sprite_scaling_player_shrunk = .07
sprite_scaling_player_bullet = .8
sprite_scaling_player_bullet_shrunk = .4
enemy_count = 50
red_coin_count = 1


class Coin(arcade.Sprite):
    """
    This class represents the coins on our screen. It is a child class of
    the arcade library's "Sprite" class.
    """

    def reset_pos(self):
        # Reset the coin to a random spot above the screen
        self.center_y = random.randrange(SCREEN_HEIGHT + 20,
                                         SCREEN_HEIGHT + 100)
        self.center_x = random.randrange(SCREEN_WIDTH)

    def update(self):
        # Move the coin
        self.center_y -= 1

        # See if the coin has fallen off the bottom of the screen.
        # If so, reset it.
        if self.top < 0:
            self.reset_pos()


class RedCoin(Coin):
    def reset_pos(self):
        # Reset the coin to a random spot above the screen
        self.center_y = random.randrange(SCREEN_HEIGHT + 200,
                                         SCREEN_HEIGHT + 1000)
        self.center_x = random.randrange(SCREEN_WIDTH)


class Enemy(arcade.Sprite):
    """
    This class uses the basis of the coin sprite to make an enemy. Didn't use inheritance because I don't know how to
    only edit portions of a method rather than the full thing.
    """

    def reset_pos(self):
        # Reset the coin to a random spot above the screen
        self.center_y = random.randrange(SCREEN_HEIGHT)
        self.center_x = random.randrange(SCREEN_WIDTH + 20,
                                         SCREEN_WIDTH + 500)

    def update(self):
        # Move the enemy
        self.center_x -= 1

        # See if the enemy has made it to the left of the screen.
        # If so, reset it.
        if self.right < 0:
            self.reset_pos()
            self.scale += 1


class PlayerBullet(arcade.Sprite):
    """
    This class is used to move the player's bullets upwards.
    """

    def update(self):
        # Move the bullet
        self.center_y += 3


class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Sprite Example")

        # Variables that will hold sprite lists
        self.player_list = None
        self.coin_list = None
        self.enemy_list = None
        self.red_coin_list = None
        self.player_bullet_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0
        self.charge = 0
        self.shrunk = False
        self.health = 10
        self.alive = True
        self.healing = False
        self.difficulty_check = 0
        self.lmb_down = False
        self.rmb_down = False
        self.last_shot = 'r'
        self.firing_big = False
        self.firing_small = False
        self.can_fire = True

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.AMAZON)

        # Load sounds
        # Pain sound from opengameart.com 'Fps Placeholder Sounds'
        self.hurt = arcade.load_sound("pain_jack_01.wav")
        # Impact sounds from kenny.nl
        self.coin_sounds = [arcade.load_sound("impactGeneric_light_000.ogg"),
                            arcade.load_sound("impactGeneric_light_001.ogg"),
                            arcade.load_sound("impactGeneric_light_002.ogg"),
                            arcade.load_sound("impactGeneric_light_003.ogg"),
                            arcade.load_sound("impactGeneric_light_004.ogg"),
                            arcade.load_sound("impactGlass_heavy_000.ogg"),
                            arcade.load_sound("impactGlass_heavy_001.ogg"),
                            arcade.load_sound("impactGlass_heavy_002.ogg"),
                            arcade.load_sound("impactGlass_heavy_003.ogg"),
                            arcade.load_sound("impactGlass_heavy_004.ogg")]
        self.red_coin_sounds = [arcade.load_sound("impactMining_000.ogg"),
                                arcade.load_sound("impactMining_001.ogg"),
                                arcade.load_sound("impactMining_002.ogg"),
                                arcade.load_sound("impactMining_003.ogg"),
                                arcade.load_sound("impactMining_004.ogg")]

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.red_coin_list = arcade.SpriteList()
        self.player_bullet_list = arcade.SpriteList()

        # Score
        self.score = 0

        # Set up the player
        # Ship image from Shoot'em Ups Pack HD by Jose Medina (Medimon). Purchased from itch.io
        self.player_sprite = arcade.Sprite("P-green-b3.png", sprite_scaling_player)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)
        self.charge = 0
        self.shrunk = False
        self.health = 10
        self.alive = True
        self.healing = False
        self.last_shot = 'r'
        self.firing_big = False
        self.firing_small = False
        self.lmb_down = False
        self.rmb_down = False
        self.can_fire = True

        # Create the coins
        for i in range(COIN_COUNT):
            # Create the coin instance
            # Coin image from kenney.nl
            coin = Coin("coin_01.png", SPRITE_SCALING_COIN)

            # Position the coin
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)

            # Add the coin to the lists
            self.coin_list.append(coin)

        # Create the enemies
        for i in range(enemy_count):
            # Laser image from kenny.nl
            enemy = Enemy("laserBlue01.png", SPRITE_SCALING_ENEMY)

            # Position the enemy
            enemy.center_x = random.randrange(SCREEN_WIDTH + 50, SCREEN_WIDTH + 500)
            enemy.center_y = random.randrange(SCREEN_HEIGHT)
            enemy.angle = 180

            # Add the enemy to the list
            self.enemy_list.append(enemy)

        for i in range(red_coin_count):
            # Modified coin image from kenny.nl
            red_coin = RedCoin("coin_02.png", SPRITE_SCALING_COIN)

            # Position the coin
            red_coin.center_x = random.randrange(SCREEN_WIDTH)
            red_coin.center_y = random.randrange(SCREEN_HEIGHT)

            # Add the coin to the lists
            self.red_coin_list.append(red_coin)

    # noinspection PyUnusedLocal
    def shrink_charge(self, delta_time):
        self.charge -= 1
        if self.charge == 0:
            self.unshrink()

    def shrink(self):
        self.player_sprite.scale = sprite_scaling_player_shrunk
        arcade.schedule(self.shrink_charge, .25)
        self.shrunk = True
        if self.firing_big and self.lmb_down:
            arcade.unschedule(self.fire_big)
            self.firing_small = True
            self.firing_big = False
            arcade.schedule(self.fire_small, .3)

    def unshrink(self):
        self.shrunk = False
        self.player_sprite.scale = sprite_scaling_player
        arcade.unschedule(self.shrink_charge)
        if self.firing_small and self.lmb_down:
            arcade.unschedule(self.fire_small)
            arcade.schedule(self.fire_big, .3)
            self.firing_big = True
            self.firing_small = False

    # noinspection PyUnusedLocal
    def heal(self, delta_time):
        if self.healing and self.health < 10:
            self.health += 1
        else:
            arcade.unschedule(self.heal)
            self.healing = False

    # noinspection PyUnusedLocal
    def fire_big(self, delta_time):
        # Laser image from kenney.nl
        player_bullet = PlayerBullet("laserGreen11.png", sprite_scaling_player_bullet)
        if self.last_shot == 'r':
            # position the right bullet
            player_bullet.center_x = self.player_sprite.center_x - 27
            self.last_shot = 'l'
        else:
            # position the left bullet
            player_bullet.center_x = self.player_sprite.center_x + 27
            self.last_shot = 'r'
        player_bullet.center_y = self.player_sprite.center_y - 10
        self.player_bullet_list.append(player_bullet)
        if self.can_fire:
            self.can_fire = False
            arcade.schedule(self.fire_cooldown, .3)

    # noinspection PyUnusedLocal
    def fire_small(self, delta_time):
        # Laser image from kenney.nl
        player_bullet = PlayerBullet("laserGreen11.png", sprite_scaling_player_bullet_shrunk)
        if self.last_shot == 'r':
            # position the right bullet
            player_bullet.center_x = self.player_sprite.center_x - 14
            self.last_shot = 'l'
        else:
            # position the left bullet
            player_bullet.center_x = self.player_sprite.center_x + 14
            self.last_shot = 'r'
        player_bullet.center_y = self.player_sprite.center_y - 5
        self.player_bullet_list.append(player_bullet)
        if self.can_fire:
            self.can_fire = False
            arcade.schedule(self.fire_cooldown, .3)

    # noinspection PyUnusedLocal
    def fire_cooldown(self, delta_time):
        self.can_fire = True
        arcade.unschedule(self.fire_cooldown)

    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        self.coin_list.draw()
        self.red_coin_list.draw()
        self.player_bullet_list.draw()
        self.player_list.draw()
        self.enemy_list.draw()
        arcade.draw_lrtb_rectangle_filled(self.player_sprite.center_x - 35, self.player_sprite.center_x + 35,
                                          self.player_sprite.center_y + 50, self.player_sprite.center_y + 47,
                                          arcade.color.BLACK)
        if self.charge > 0:
            arcade.draw_lrtb_rectangle_filled(self.player_sprite.center_x - 35,
                                              self.player_sprite.center_x - 35 + (70 * (self.charge * 5 / 100)),
                                              self.player_sprite.center_y + 50, self.player_sprite.center_y + 47,
                                              arcade.color.GREEN)
        arcade.draw_lrtb_rectangle_filled(self.player_sprite.center_x - 35, self.player_sprite.center_x + 35,
                                          self.player_sprite.center_y + 55, self.player_sprite.center_y + 52,
                                          arcade.color.BLACK)
        if self.health > 0:
            arcade.draw_lrtb_rectangle_filled(self.player_sprite.center_x - 35, self.player_sprite.center_x - 35 +
                                              (70 * (self.health * 10 / 100)), self.player_sprite.center_y + 55,
                                              self.player_sprite.center_y + 52, arcade.color.RED)

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)
        arcade.draw_text("Enemy count: " + str(enemy_count), SCREEN_WIDTH - 200, 20, arcade.color.WHITE, 14)
        if not self.alive:
            arcade.draw_text("You died!", (SCREEN_WIDTH * .5) + .9, SCREEN_HEIGHT * .5, arcade.color.BLACK, 25.5)
            arcade.draw_text("You died!", SCREEN_WIDTH * .5, SCREEN_HEIGHT * .5, arcade.color.RED, 25)

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """

        # Move the center of the player sprite to match the mouse x, y
        if self.alive:
            self.player_sprite.center_x = x
            self.player_sprite.center_y = y

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.lmb_down = True
            if not self.shrunk:
                self.firing_big = True
                if self.can_fire:
                    self.fire_big(0)
                    self.can_fire = False
                    arcade.schedule(self.fire_cooldown, .3)
                arcade.schedule(self.fire_big, .3)
            else:
                self.firing_small = True
                if self.can_fire:
                    self.fire_small(0)
                    self.can_fire = False
                    arcade.schedule(self.fire_cooldown, .3)
                arcade.schedule(self.fire_small, .3)
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.rmb_down = True
            if self.charge > 0:
                self.shrink()

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.lmb_down = False
            if not self.shrunk:
                arcade.unschedule(self.fire_big)
            else:
                arcade.unschedule(self.fire_small)
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.rmb_down = False
            if self.shrunk:
                self.unshrink()

    def update(self, delta_time):
        global enemy_count
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        if self.alive:
            self.coin_list.update()
            self.enemy_list.update()
            self.player_list.update()
            self.red_coin_list.update()
            self.player_bullet_list.update()

        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                        self.coin_list)
        damage_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                           self.enemy_list)
        red_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                            self.red_coin_list)
        for bullet in self.player_bullet_list:
            kill_list = arcade.check_for_collision_with_list(bullet,
                                                             self.enemy_list)
            if len(kill_list) > 0:
                bullet.remove_from_sprite_lists()
            for kill in kill_list:
                if bullet.scale == sprite_scaling_player_bullet_shrunk:
                    kill.scale -= .25
                else:
                    kill.scale -= 1
                if kill.scale <= .5:
                    kill.reset_pos()
                    kill.scale = SPRITE_SCALING_ENEMY
                    self.score += 1

        # Loop through each colliding sprite, remove it, and add to the score.
        for coin in hit_list:
            coin.reset_pos()
            self.score += 2
            if self.charge < 20:
                self.charge += 1
            if self.rmb_down and not self.shrunk:
                self.shrink()
            self.difficulty_check += 2
            if self.difficulty_check > 5:
                enemy_count += 1
                self.difficulty_check -= 5
                if self.difficulty_check < 0:
                    self.difficulty_check = 0
                enemy = Enemy("laserBlue01.png", SPRITE_SCALING_ENEMY)

                # Position the enemy
                enemy.center_x = random.randrange(SCREEN_WIDTH + 100, SCREEN_WIDTH + 300)
                enemy.center_y = random.randrange(SCREEN_HEIGHT)
                enemy.angle = 180

                # Add the enemy to the list
                self.enemy_list.append(enemy)
            if coin == hit_list[0]:
                arcade.play_sound(self.coin_sounds[random.randrange(10)], volume=.02)

        for red_coin in red_hit_list:
            red_coin.reset_pos()
            self.score += 5
            if self.charge < 20:
                self.charge += 5
                if self.charge > 20:
                    self.charge = 20
            if self.rmb_down and not self.shrunk:
                self.shrink()
            self.difficulty_check += 5
            if self.difficulty_check > 5:
                enemy_count += 1
                self.difficulty_check -= 5
                if self.difficulty_check < 0:
                    self.difficulty_check = 0
                # Laser image from kenny.nl
                enemy = Enemy("laserBlue01.png", SPRITE_SCALING_ENEMY)

                # Position the enemy
                enemy.center_x = random.randrange(SCREEN_WIDTH + 100, SCREEN_WIDTH + 300)
                enemy.center_y = random.randrange(SCREEN_HEIGHT)
                enemy.angle = 180

                # Add the enemy to the list
                self.enemy_list.append(enemy)
            if red_coin == red_hit_list[0]:
                arcade.play_sound(self.red_coin_sounds[random.randrange(5)], volume=.03)

        for damage in damage_list:
            damage.reset_pos()
            self.score -= 10
            if self.charge > 0:
                self.charge -= 5
                if self.charge <= 0:
                    self.charge = 0
                    self.unshrink()
            if self.health > 0:
                self.health -= 2
            if self.health <= 0:
                self.alive = False
                self.healing = False
            if 0 < self.health < 10 and not self.healing:
                arcade.schedule(self.heal, 3)
                self.healing = True
            if damage == damage_list[0]:
                arcade.play_sound(self.hurt, volume=.02)


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
