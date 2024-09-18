import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "ChronoBlade"

class GameEngine(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.ASH_GREY)

        self.player_x = 400
        self.player_y = 300
        self.player_speed = 5

        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("test", 100, 500, arcade.color.BLACK, 20)
        arcade.draw_circle_filled(self.player_x, self.player_y, 30, arcade.color.BLUE)

    def on_update(self, delta_time):
        if self.up_pressed:
            self.player_y += self.player_speed
        if self.down_pressed:
            self.player_y -= self.player_speed
        if self.left_pressed:
            self.player_x -= self.player_speed
        if self.right_pressed:
            self.player_x += self.player_speed

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

def main():
    window = GameEngine(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()

if __name__ == "__main__":
    main()
