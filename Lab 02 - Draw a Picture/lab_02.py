import arcade

arcade.open_window(480, 480, "Lab 2 drawing")
arcade.set_background_color(arcade.csscolor.DEEP_SKY_BLUE)
arcade.start_render()

# grass
arcade.draw_lrtb_rectangle_filled(0, 480, 100, 0, arcade.color.OLIVE_DRAB)

# sidewalk
# use trapezoid to show distance / perspective
arcade.draw_polygon_filled(((245, 90), (285, 90), (310, 0), (210, 0)), arcade.csscolor.GRAY)
arcade.draw_polygon_outline(((245, 90), (285, 90), (310, 0), (210, 0)), arcade.csscolor.BLACK, 3)
y = 5
z = 15
for x in range(1, 5):
    arcade.draw_line(245 - (x * y), 90 - (x * z), 285 + ((x * y) - x), 90 - (x * z), arcade.csscolor.BLACK, 3)
    y += 1.3
    z += 3

# cabin
arcade.draw_triangle_filled(200, 200, 360, 200, 290, 300, arcade.csscolor.DARK_RED)
arcade.draw_lrtb_rectangle_filled(220, 340, 200, 90, arcade.csscolor.BROWN)
arcade.draw_lrtb_rectangle_outline(220, 340, 200, 90, arcade.csscolor.BLACK, 3)
arcade.draw_triangle_outline(200, 200, 360, 200, 290, 300, arcade.csscolor.BLACK, 3)

# cabin door
arcade.draw_lrtb_rectangle_filled(245, 285, 160, 92, arcade.csscolor.SADDLE_BROWN)
arcade.draw_lrtb_rectangle_outline(245, 285, 160, 92, arcade.csscolor.BLACK, 2)
arcade.draw_circle_filled(249, 126, 4, arcade.csscolor.GOLDENROD)
arcade.draw_circle_outline(249, 126, 5, arcade.csscolor.BLACK, 2)

# tree
arcade.draw_lrtb_rectangle_filled(85, 110, 190, 90, arcade.color.BOLE)
arcade.draw_lrtb_rectangle_outline(85, 110, 190, 90, arcade.color.BLACK, 2)
arcade.draw_circle_filled(100, 190, 40, arcade.csscolor.DARK_GREEN)
for x in range(0, 180, 25):
    arcade.draw_ellipse_outline(100, 190, 106, 51, arcade.csscolor.BLACK, 35, x)
for x in range(0, 180, 25):
    arcade.draw_ellipse_filled(100, 190, 100, 45, arcade.csscolor.DARK_GREEN, x)


# clouds
def draw_cloud(cloud_x, cloud_y):
    arcade.draw_ellipse_filled(cloud_x, cloud_y, 150, 50, arcade.csscolor.WHITE)


# using several ellipses to make one cloud rather than making a function that makes good clouds to save time
draw_cloud(50, 325)
draw_cloud(65, 350)
draw_cloud(50, 375)
draw_cloud(370, 325)
draw_cloud(365, 350)
draw_cloud(370, 375)
draw_cloud(375, 350)


# birds
def draw_bird(bird_x, bird_y):
    arcade.draw_arc_outline(bird_x, bird_y, 15, 10, arcade.csscolor.BLACK, 0, 180, 3)
    arcade.draw_arc_outline((bird_x + 15), bird_y, 15, 10, arcade.csscolor.BLACK, 0, 180, 3)


draw_bird(350, 350)
draw_bird(300, 350)
draw_bird(325, 325)

arcade.finish_render()
arcade.run()
