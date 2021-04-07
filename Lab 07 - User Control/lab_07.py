""" Lab 7 - User Control """

import arcade

# --- Constants ---

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MOVEMENT_SPEED = 5


class Ball:
    def __init__(self, position_x, position_y, change_x, change_y, radius):
        """ Initializer for keyboard object"""
        self.position_x = position_x
        self.position_y = position_y
        self.change_x = change_x
        self.change_y = change_y
        # While the object is going to be drawn in a different manner than a normal ball, a radius is still needed
        # for hitbox purposes
        self.radius = radius
        self.x_inputs = 0
        self.y_inputs = 0
        self.wall_collide = arcade.load_sound("chipsStack4.wav")
        self.at_wall = False

    def draw(self):
        """draw thing"""
        arcade.draw_circle_filled(self.position_x, self.position_y, self.radius, arcade.color.YELLOW)
        arcade.draw_circle_filled(self.position_x + 4, self.position_y + 1, self.radius - 8, arcade.color.RED)
        arcade.draw_circle_filled(self.position_x - 4, self.position_y + 1, self.radius - 8, arcade.color.RED)
        arcade.draw_arc_filled(self.position_x, self.position_y-4, self.radius - 4, -5, arcade.color.RED, 0, 180)

    def update(self):
        """move the object"""
        self.position_y += self.change_y
        self.position_x += self.change_x

        # check for screen boundaries here
        if self.position_y < self.radius:
            self.position_y = self.radius
            if not self.at_wall:
                arcade.play_sound(self.wall_collide)
                self.at_wall = True
        elif self.position_x < self.radius:
            self.position_x = self.radius
            if not self.at_wall:
                arcade.play_sound(self.wall_collide)
                self.at_wall = True
        elif self.position_x > SCREEN_WIDTH - self.radius:
            self.position_x = SCREEN_WIDTH - self.radius
            if not self.at_wall:
                arcade.play_sound(self.wall_collide)
                self.at_wall = True
        elif self.position_y > SCREEN_HEIGHT - self.radius:
            self.position_y = SCREEN_HEIGHT - self.radius
            if not self.at_wall:
                arcade.play_sound(self.wall_collide)
                self.at_wall = True
        else:
            self.at_wall = False


class Ball2:
    def __init__(self, position_x, position_y, change_x, change_y):
        """ Initializer for mouse object"""
        self.position_x = position_x
        self.position_y = position_y
        self.change_x = change_x
        self.change_y = change_y

    def draw(self):
        """draw thing"""
        arcade.draw_circle_filled(self.position_x, self.position_y, 3, arcade.color.GREEN)

    def update(self):
        """move the object"""
        self.position_y += self.change_y
        self.position_x += self.change_x


class MyGame(arcade.Window):
    """ Our Custom Window Class"""

    def __init__(self):
        """ Initializer """

        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Lab 7 - User Control")
        self.set_mouse_visible(False)
        arcade.set_background_color(arcade.color.BLACK)
        self.ball = Ball(50, 50, 0, 0, radius=10)
        self.ball2 = Ball2(50, 50, 15, 0)
        self.click_sound = arcade.load_sound("cardFan1.wav")

    def on_draw(self):
        arcade.start_render()
        self.ball.draw()
        self.ball2.draw()

    def update(self, delta_time):
        self.ball.update()

    def on_key_press(self, key, modifiers):
        """When you press a key, start moving in that direction at movement speed"""
        if key == arcade.key.LEFT:
            self.ball.x_inputs += 1
            self.ball.change_x = -MOVEMENT_SPEED
        if key == arcade.key.RIGHT:
            self.ball.x_inputs += 1
            self.ball.change_x = MOVEMENT_SPEED
        if key == arcade.key.UP:
            self.ball.y_inputs += 1
            self.ball.change_y = MOVEMENT_SPEED
        if key == arcade.key.DOWN:
            self.ball.y_inputs += 1
            self.ball.change_y = -MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """When a key is released, set movement in that direction to 0. Problem with this method is that if you are
        holding two keys in the opposite direction, releasing one stops movement entirely instead of switching to the
        other way. This makes changing direction annoying, as this often happens accidentally"""
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.ball.y_inputs -= 1
            if self.ball.y_inputs == 0:
                self.ball.change_y = 0
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.ball.x_inputs -= 1
            if self.ball.x_inputs == 0:
                self.ball.change_x = 0

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.ball2.position_x = x
        self.ball2.position_y = y

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            # sound
            arcade.play_sound(self.click_sound)


def main():
    # noinspection PyUnusedLocal
    window = MyGame()
    arcade.run()


main()
