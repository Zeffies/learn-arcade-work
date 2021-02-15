import arcade
# this is a test
arcade.open_window(1280, 720, "720p Window Test")
arcade.set_background_color(arcade.csscolor.SKY_BLUE)
arcade.start_render()
arcade.draw_lrtb_rectangle_filled(0, 1279, 300, 0, arcade.csscolor.GREEN)
arcade.draw_rectangle_filled(100, 320, 20, 60, arcade.csscolor.SIENNA)
arcade.draw_circle_filled(100, 350, 30, arcade.csscolor.DARK_GREEN)
arcade.draw_ellipse_filled(100, 350, 85, 45, arcade.csscolor.DARK_GREEN)
arcade.draw_ellipse_filled(100, 370, 35, 37, arcade.csscolor.DARK_GREEN)
arcade.draw_rectangle_filled(300, 320, 20, 60, arcade.csscolor.SIENNA)
arcade.draw_arc_filled(300, 340, 60, 100, arcade.csscolor.DARK_GREEN, 0, 180)
arcade.draw_ellipse_filled(center_x=800,
                           center_y=500,
                           width=30,
                           height=40,
                           color=arcade.csscolor.DARK_RED)
arcade.finish_render()
arcade.run()
