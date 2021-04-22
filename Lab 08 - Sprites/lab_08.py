import random
import arcade

# --- Constants ---
SPRITE_SCALING_COIN = 0.2
SPRITE_SCALING_ENEMY = 1
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SHRINK_CHARGE_UP_SPEED = 2
SHRINK_CHARGE_DOWN_SPEED = .25
HEALTH_CHARGE_SPEED = 1.5
COOLDOWN_BIG = .3
COOLDOWN_BIG_OVERCHARGE = .2
COOLDOWN_SMALL = .1

# --- Other Variables ---
sprite_scaling_player = 0.15
sprite_scaling_player_shrunk = .07
sprite_scaling_player_bullet = .8
sprite_scaling_player_bullet_shrunk = .4
enemy_count = 10
score = 0
coin_count = 20


class Coin(arcade.Sprite):
    """
    This class represents the coins on our screen. It is a child class of
    the arcade library's "Sprite" class.
    """

    def __init__(self, e_texture, e_scale, name, value):
        super(Coin, self).__init__(e_texture, e_scale)
        self.name = name
        self.value = value

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
            if self.name == "gold":
                self.reset_pos()
            else:
                self.remove_from_sprite_lists()


class Enemy(arcade.Sprite):
    """
    This class uses the basis of the coin sprite to make an enemy. Didn't use inheritance because I don't know how to
    only edit portions of a method rather than the full thing.
    """

    def __init__(self, e_texture, e_scale, name, health=2, speedmax=4):
        super(Enemy, self).__init__(e_texture, e_scale)
        self.health = health
        self.name = name
        self.scale = .5 + (self.health * .25)
        self.speed = random.randrange(1, speedmax)

    def reset_pos(self):
        # Reset the coin to a random spot above the screen
        self.center_y = random.randrange(SCREEN_HEIGHT)
        self.center_x = random.randrange(SCREEN_WIDTH + 20,
                                         SCREEN_WIDTH + 500)
        self.speed = random.randrange(1, 4)

    def update(self):
        global score, enemy_count, coin_count
        # Move the enemy
        self.center_x -= self.speed

        # See if the enemy has made it to the left of the screen.
        # If so, reset it.
        if self.right < 0:
            if self.name == "blue":
                self.reset_pos()
                self.health += 2
                if self.health > 10:
                    if enemy_count > (coin_count*2):
                        self.remove_from_sprite_lists()
                        enemy_count -= 1
                    else:
                        self.health = 2
                    score += 10
                self.scale = .5 + (self.health * .25)
            else:
                self.remove_from_sprite_lists()


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
        global score
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Sprite Example")

        # Variables that will hold sprite lists
        self.player_list = None
        self.coin_list = None
        self.enemy_list = None
        self.player_bullet_list = None

        # Set up the player info
        self.player_sprite = None
        self.charge = 20
        self.shrink_charging = False
        self.shrunk = False
        self.health = 20
        self.alive = True
        self.healing = False
        self.difficulty_check = 0
        self.lmb_down = False
        self.rmb_down = False
        self.last_shot = 'r'
        self.firing_big = False
        self.firing_small = False
        self.can_fire = True
        self.can_regen = True
        self.charge_cooling = False

        # misc
        self.random_enemy = 0

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        # Get monitor list for fullscreen
        self.monitors = arcade.get_screens()
        self.view_coords = arcade.get_viewport()

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
        self.better_coin_sounds = [arcade.load_sound("impactMining_000.ogg"),
                                   arcade.load_sound("impactMining_001.ogg"),
                                   arcade.load_sound("impactMining_002.ogg"),
                                   arcade.load_sound("impactMining_003.ogg"),
                                   arcade.load_sound("impactMining_004.ogg")]

    def setup(self):
        global score
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player_bullet_list = arcade.SpriteList()

        # Score
        score = 0

        # Set up the player
        # Ship image from Shoot'em Ups Pack HD by Jose Medina (Medimon). Purchased from itch.io
        self.player_sprite = arcade.Sprite("P-green-b3.png", sprite_scaling_player)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)
        self.charge = 20
        self.shrunk = False
        self.shrink_charging = False
        self.health = 20
        self.alive = True
        self.healing = False
        self.last_shot = 'r'
        self.firing_big = False
        self.firing_small = False
        self.lmb_down = False
        self.rmb_down = False
        self.can_fire = True

        # Create the coins
        for i in range(coin_count):
            # Create the coin instance
            # Coin image from kenney.nl
            coin = Coin("coinGold.png", SPRITE_SCALING_COIN, "gold", value=1)

            # Position the coin
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)

            # Add the coin to the lists
            self.coin_list.append(coin)

        # Create the enemies
        for i in range(enemy_count):
            # Laser image from kenny.nl
            enemy = Enemy("laserBlue01.png", SPRITE_SCALING_ENEMY, "blue")

            # Position the enemy
            enemy.center_x = random.randrange(SCREEN_WIDTH + 50, SCREEN_WIDTH + 500)
            enemy.center_y = random.randrange(SCREEN_HEIGHT)
            enemy.angle = 180

            # Add the enemy to the list
            self.enemy_list.append(enemy)

    # noinspection PyUnusedLocal
    def shrink_charge_down(self, delta_time):
        if self.charge <= 20:
            self.charge -= 1
        elif self.charge < 25:
            self.charge = 20
        else:
            self.charge -= 3
        if self.charge == 0:
            self.unshrink()
            if self.charge_cooling:
                arcade.unschedule(self.regen_cooldown)
            arcade.schedule(self.regen_cooldown, 5)
            self.charge_cooling = True

    # noinspection PyUnusedLocal
    def shrink_charge_up(self, delta_time):
        if self.charge < 20:
            self.charge += 1
        else:
            self.shrink_charging = False
            arcade.unschedule(self.shrink_charge_up)
        if self.charge == 1 and self.rmb_down:
            self.shrink()

    def shrink(self):
        self.player_sprite.scale = sprite_scaling_player_shrunk
        arcade.unschedule(self.shrink_charge_up)
        arcade.schedule(self.shrink_charge_down, SHRINK_CHARGE_DOWN_SPEED)
        self.shrunk = True
        if self.firing_big and self.lmb_down:
            arcade.unschedule(self.fire_big)
            self.firing_small = True
            self.firing_big = False
            arcade.schedule(self.fire_small, COOLDOWN_SMALL)

    def unshrink(self):
        self.shrunk = False
        self.player_sprite.scale = sprite_scaling_player
        arcade.unschedule(self.shrink_charge_down)
        if self.firing_small and self.lmb_down:
            arcade.unschedule(self.fire_small)
            arcade.schedule(self.fire_big, COOLDOWN_BIG)
            self.firing_big = True
            self.firing_small = False

    # noinspection PyUnusedLocal
    def heal(self, delta_time):
        if self.healing and self.health < 20:
            self.health += 1
        else:
            arcade.unschedule(self.heal)
            self.healing = False

    # noinspection PyUnusedLocal
    def fire_big(self, delta_time):
        # Laser image from kenney.nl
        if self.charge < 40:
            player_bullet = PlayerBullet("laserGreen11.png", sprite_scaling_player_bullet)
        else:
            player_bullet = PlayerBullet("laserYellow1.png", sprite_scaling_player_bullet)
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
            arcade.schedule(self.fire_cooldown, COOLDOWN_BIG)

    # noinspection PyUnusedLocal
    def fire_small(self, delta_time):
        # Laser image from kenney.nl
        if self.charge < 40:
            player_bullet = PlayerBullet("laserGreen11.png", sprite_scaling_player_bullet_shrunk)
        else:
            player_bullet = PlayerBullet("laserYellow1.png", sprite_scaling_player_bullet_shrunk)
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
            arcade.schedule(self.fire_cooldown, COOLDOWN_BIG)

    # noinspection PyUnusedLocal
    def fire_cooldown(self, delta_time):
        self.can_fire = True
        arcade.unschedule(self.fire_cooldown)

    # noinspection PyUnusedLocal
    def regen_cooldown(self, delta_time):
        self.charge_cooling = False
        if self.charge < 20:
            self.shrink_charging = True
            arcade.schedule(self.shrink_charge_up, SHRINK_CHARGE_UP_SPEED)
        arcade.unschedule(self.regen_cooldown)

    def spawn_coin(self, coin_type, x, y):
        global coin_count
        coin = Coin("coin" + coin_type.title() + ".png", SPRITE_SCALING_COIN, coin_type, 2)
        if coin_type == "gold":
            coin.value = 1
            coin_count += 1
        elif coin_type == "blue":
            coin.value = 2
        elif coin_type == "red":
            coin.value = 5
        elif coin_type == "purple":
            coin.value = 10
        elif coin_type == "silver":
            coin.value = 25

        # Position the coin
        coin.center_x = x
        coin.center_y = y

        # Add the coin to the lists
        self.coin_list.append(coin)

    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        self.coin_list.draw()
        self.player_bullet_list.draw()
        self.player_list.draw()
        self.enemy_list.draw()
        if self.charge < 20:
            arcade.draw_lrtb_rectangle_filled(self.player_sprite.center_x - 35, self.player_sprite.center_x + 35,
                                              self.player_sprite.center_y + 50, self.player_sprite.center_y + 47,
                                              arcade.color.BLACK)
        if 20 > self.charge > 0:
            arcade.draw_lrtb_rectangle_filled(self.player_sprite.center_x - 35,
                                              self.player_sprite.center_x - 35 + (70 * (self.charge * 5 / 100)),
                                              self.player_sprite.center_y + 50, self.player_sprite.center_y + 47,
                                              arcade.color.GREEN)
        elif 20 <= self.charge < 40:
            arcade.draw_lrtb_rectangle_filled(self.player_sprite.center_x - 35,
                                              self.player_sprite.center_x - 35 + (70 * (20 * 5 / 100)),
                                              self.player_sprite.center_y + 50, self.player_sprite.center_y + 47,
                                              arcade.color.GREEN)
        if self.charge > 20:
            arcade.draw_lrtb_rectangle_filled(self.player_sprite.center_x - 35,
                                              self.player_sprite.center_x - 35 + (70 * ((self.charge - 20) * 5 / 100)),
                                              self.player_sprite.center_y + 50, self.player_sprite.center_y + 47,
                                              arcade.color.GOLD)

        arcade.draw_lrtb_rectangle_filled(self.player_sprite.center_x - 35, self.player_sprite.center_x + 35,
                                          self.player_sprite.center_y + 55, self.player_sprite.center_y + 52,
                                          arcade.color.BLACK)
        if self.health > 0:
            arcade.draw_lrtb_rectangle_filled(self.player_sprite.center_x - 35, self.player_sprite.center_x - 35 +
                                              (70 * (self.health * 5 / 100)), self.player_sprite.center_y + 55,
                                              self.player_sprite.center_y + 52, arcade.color.RED)

        # Put the text on the screen.
        output = f"Score: {score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)
        arcade.draw_text("Enemy count: " + str(enemy_count) + "/" + str(coin_count*2), SCREEN_WIDTH - 200, 20,
                         arcade.color.WHITE, 14)
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
                    if self.charge < 40:
                        arcade.schedule(self.fire_cooldown, COOLDOWN_BIG)
                    else:
                        arcade.schedule(self.fire_cooldown, COOLDOWN_BIG_OVERCHARGE)
                if self.charge < 40:
                    arcade.schedule(self.fire_big, COOLDOWN_BIG)
                else:
                    arcade.schedule(self.fire_big, COOLDOWN_BIG_OVERCHARGE)
            else:
                self.firing_small = True
                if self.can_fire:
                    self.fire_small(0)
                    self.can_fire = False
                    arcade.schedule(self.fire_cooldown, COOLDOWN_SMALL)
                arcade.schedule(self.fire_small, COOLDOWN_SMALL)
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.rmb_down = True
            if self.charge > 0:
                self.shrink()
                self.can_regen = False

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.lmb_down = False
            if not self.shrunk:
                arcade.unschedule(self.fire_big)
                self.firing_big = False
            else:
                arcade.unschedule(self.fire_small)
                self.firing_small = False
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.rmb_down = False
            if self.shrunk:
                self.unshrink()
                if self.charge_cooling:
                    arcade.unschedule(self.regen_cooldown)
                arcade.schedule(self.regen_cooldown, 5)
                self.charge_cooling = True

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.F:
            if self.fullscreen:
                self.set_fullscreen(False)
            else:
                self.set_fullscreen(screen=self.monitors[1])
                self.set_viewport(self.view_coords[0], self.view_coords[1], self.view_coords[2], self.view_coords[3])

    def update(self, delta_time):
        global enemy_count, score
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        if self.alive:
            self.coin_list.update()
            self.enemy_list.update()
            self.player_list.update()
            self.player_bullet_list.update()

        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                        self.coin_list)
        damage_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                           self.enemy_list)
        for bullet in self.player_bullet_list:
            kill_list = arcade.check_for_collision_with_list(bullet,
                                                             self.enemy_list)

            for kill in kill_list:
                if bullet.scale == sprite_scaling_player_bullet_shrunk:
                    if bullet.texture == "laserGreen11.png":
                        kill.health -= 1
                    else:
                        kill.health -= 2
                    kill.scale = .5 + (kill.health * .25)
                    if len(kill_list) > 0:
                        bullet.remove_from_sprite_lists()
                else:
                    if len(kill_list) > 0:
                        if kill.health > 1:
                            bullet.remove_from_sprite_lists()
                        else:
                            bullet.scale = sprite_scaling_player_bullet_shrunk
                    if bullet.texture == "laserGreen11.png":
                        kill.health -= 2
                    else:
                        kill.health -= 3
                    kill.scale = .5 + (kill.health * .25)
                if kill.health <= 0:
                    self.spawn_coin(kill.name, kill.center_x, kill.center_y)
                    if kill.name == "blue":
                        kill.reset_pos()
                    else:
                        kill.remove_from_sprite_lists()
                    kill.health = 2
                    kill.scale = SPRITE_SCALING_ENEMY
                    if kill.name == "blue":
                        score += 1
                    elif kill.name == "red":
                        score += 2
                    elif kill.name == "purple":
                        score += 3
                    elif kill.name == "silver":
                        score += 4
                    elif kill.name == "gold":
                        score += 15
                    if self.charge < 40:
                        self.charge += 1
                        if self.charge == 40 and self.firing_big:
                            arcade.unschedule(self.fire_big)
                            arcade.schedule(self.fire_big, COOLDOWN_BIG_OVERCHARGE)

        # Loop through each colliding sprite, remove it, and add to the score.
        for coin in hit_list:
            if coin.name == "gold":
                coin.reset_pos()
            else:
                coin.remove_from_sprite_lists()
            score += coin.value
            self.difficulty_check += coin.value
            if self.difficulty_check > 5:
                self.difficulty_check -= 5
                if self.difficulty_check < 0:
                    self.difficulty_check = 0
                self.random_enemy = random.randrange(190)
                if self.random_enemy <= 100:
                    enemy = Enemy("laserBlue01.png", SPRITE_SCALING_ENEMY, "blue")
                    enemy_count += 1
                elif 100 < self.random_enemy <= 150:
                    enemy = Enemy("laserRed01.png", SPRITE_SCALING_ENEMY, "red", health=4)
                elif 150 < self.random_enemy <= 175:
                    enemy = Enemy("laserPurple.png", SPRITE_SCALING_ENEMY, "purple", health=6)
                elif 175 < self.random_enemy <= 185:
                    enemy = Enemy("laserSilver.png", SPRITE_SCALING_ENEMY, "silver", health=8)
                else:
                    enemy = Enemy("laserGold.png", SPRITE_SCALING_ENEMY, "gold", health=10)

                # Position the enemy
                enemy.center_x = random.randrange(SCREEN_WIDTH + 100, SCREEN_WIDTH + 300)
                enemy.center_y = random.randrange(SCREEN_HEIGHT)
                if enemy.name == "blue":
                    enemy.angle = 180
                else:
                    enemy.angle = 90

                # Add the enemy to the list
                self.enemy_list.append(enemy)

            if coin == hit_list[0]:
                if coin.name == "gold":
                    arcade.play_sound(self.coin_sounds[random.randrange(10)], volume=.02)
                else:
                    arcade.play_sound(self.better_coin_sounds[random.randrange(5)], volume=.03)

        for damage in damage_list:
            damage.reset_pos()
            score -= 10
            if self.firing_big and self.charge == 40:
                arcade.unschedule(self.fire_big)
                arcade.schedule(self.fire_big, COOLDOWN_BIG)
            if self.charge > 0:
                self.charge -= 5
                if self.charge <= 0:
                    self.charge = 0
                    self.unshrink()
                    if self.charge_cooling:
                        arcade.unschedule(self.regen_cooldown)
                    arcade.schedule(self.regen_cooldown, 5)
                    self.charge_cooling = True
            if self.charge < 20:
                self.charge_cooling = True
                arcade.unschedule(self.shrink_charge_up)
                arcade.schedule(self.regen_cooldown, SHRINK_CHARGE_UP_SPEED)
            if self.health > 0:
                self.health -= damage.health
            if self.health <= 0:
                self.alive = False
                self.healing = False
            if 0 < self.health < 20 and not self.healing:
                arcade.schedule(self.heal, HEALTH_CHARGE_SPEED)
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
