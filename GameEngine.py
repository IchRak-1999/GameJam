import arcade
import os
import time
from Platform import Platform
from SolidObject import SolidObject
from Player import Player

# Constants for screen width, height, and title
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Quantum Rewind"

# Background scrolling speeds
BACKGROUND_SCROLL_SPEED_3 = 1  # Layer 3 scroll speed
BACKGROUND_SCROLL_SPEED_4 = 2  # Layer 4 scroll speed

class GameEngine(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.ASH_GREY)
        self.scene = None
        self.camera = None
        self.time_slowed = False
        self.mana = None

        self.rewinding = False
        self.rewind_start_time = 0
        self.rewind_duration = 5
        self.pos_hist = []

        # Background attributes for parallax scrolling
        self.bg_layer_3 = None
        self.bg_layer_4 = None
        self.bg_layer_3_x_1 = 0  # Initial x position for first instance of layer 3
        self.bg_layer_3_x_2 = SCREEN_WIDTH  # Initial x position for second instance of layer 3
        self.bg_layer_4_x_1 = 0  # Initial x position for first instance of layer 4
        self.bg_layer_4_x_2 = SCREEN_WIDTH  # Initial x position for second instance of layer 4

    # Initialize game elements
    def setup(self):
        # Load player and mana settings
        self.player = Player(400, 300, 5, 10, -0.5)
        self.mana = 0
        self.mana_bar = arcade.SpriteSolidColor(50, self.mana, arcade.color.BLUE)
        self.mana_bar.center_x = SCREEN_WIDTH - 50
        self.mana_bar.center_y = SCREEN_HEIGHT - 100
        self.mana_rate = 1

        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False

        self.platforms = [
            Platform(200, 20, arcade.color.YELLOW, 400, 50, -1, 0),
            Platform(200, 20, arcade.color.RED, 300, 250, 2, 0),
            Platform(200, 20, arcade.color.ORANGE, 400, 200, 0, 1)
        ]

        self.ground = SolidObject(SCREEN_WIDTH, 20, arcade.color.BLACK, SCREEN_WIDTH // 2, 10)

        # Load background textures for parallax layers
        base_path = os.path.abspath(os.path.dirname(__file__))
        bg_layer_3_path = os.path.join(base_path, "Assets", "env", "Clouds", "Clouds 2", "3.png")
        bg_layer_4_path = os.path.join(base_path, "Assets", "env", "Clouds", "Clouds 2", "4.png")

        self.bg_layer_3 = arcade.load_texture(bg_layer_3_path)
        self.bg_layer_4 = arcade.load_texture(bg_layer_4_path)

        self.camera = arcade.Camera(self.width, self.height)

    # Rewind functionality
    def rewind(self):
        if not self.rewinding:
            self.rewinding = True
            self.rewind_start_time = time.time()
            self.pos_hist = self.pos_hist[-int(self.rewind_duration * 60):]

    def stop_rewind(self):
        self.rewinding = False
        self.pos_hist = []

    def update_mana_bar(self):
        camera_x, camera_y = self.camera.position
        self.mana_bar = arcade.SpriteSolidColor(50, self.mana, arcade.color.BLUE)
        self.mana_bar.center_x = camera_x + SCREEN_WIDTH - 50
        self.mana_bar.center_y = camera_y + SCREEN_HEIGHT - self.mana / 2 - 10

    def on_draw(self):
        """ Render the screen """
        arcade.start_render()

        # Draw background layers (parallax scrolling for layers 3 and 4)
        arcade.draw_lrwh_rectangle_textured(self.bg_layer_3_x_1, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.bg_layer_3)
        arcade.draw_lrwh_rectangle_textured(self.bg_layer_3_x_2, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.bg_layer_3)
        arcade.draw_lrwh_rectangle_textured(self.bg_layer_4_x_1, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.bg_layer_4)
        arcade.draw_lrwh_rectangle_textured(self.bg_layer_4_x_2, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.bg_layer_4)

        # Draw game objects
        self.ground.draw()
        self.mana_bar.draw()
        for platform in self.platforms:
            platform.draw()
        arcade.draw_circle_filled(self.player.center_x, self.player.center_y, 30, arcade.color.GREEN)
        self.camera.use()

    def on_update(self, delta_time):
        self.update_mana_bar()
        self.center_camera_to_player()

        if self.rewinding:
            rewind_time_elapsed = time.time() - self.rewind_start_time
            rewind_frame_count = int(rewind_time_elapsed * 60)
            self.mana -= self.mana_rate
            if self.mana <= 0:
                self.stop_rewind()
            elif rewind_frame_count < len(self.pos_hist):
                self.player.center_x, self.player.center_y = self.pos_hist[-rewind_frame_count - 1]
            else:
                self.stop_rewind()
        else:
            self.player.update(self.up_pressed, self.down_pressed, self.left_pressed, self.right_pressed, self.platforms, delta_time)
            self.move_platforms(delta_time)

            self.pos_hist.append((self.player.center_x, self.player.center_y))
            if self.mana < 100:
                self.mana += self.mana_rate

        # Update parallax background scrolling
        self.bg_layer_3_x_1 -= BACKGROUND_SCROLL_SPEED_3
        self.bg_layer_3_x_2 -= BACKGROUND_SCROLL_SPEED_3
        self.bg_layer_4_x_1 -= BACKGROUND_SCROLL_SPEED_4
        self.bg_layer_4_x_2 -= BACKGROUND_SCROLL_SPEED_4

        if self.bg_layer_3_x_1 <= -SCREEN_WIDTH:
            self.bg_layer_3_x_1 = SCREEN_WIDTH
        if self.bg_layer_3_x_2 <= -SCREEN_WIDTH:
            self.bg_layer_3_x_2 = SCREEN_WIDTH

        if self.bg_layer_4_x_1 <= -SCREEN_WIDTH:
            self.bg_layer_4_x_1 = SCREEN_WIDTH
        if self.bg_layer_4_x_2 <= -SCREEN_WIDTH:
            self.bg_layer_4_x_2 = SCREEN_WIDTH

    def move_platforms(self, delta_time):
        for platform in self.platforms:
            platform.update(delta_time)

    def center_camera_to_player(self):
        screen_center_x = self.player.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player.center_y - (self.camera.viewport_height / 2)

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_key_press(self, key, modifiers):
        if not self.rewinding:
            if key == arcade.key.UP:
                self.up_pressed = True
            elif key == arcade.key.DOWN:
                self.down_pressed = True
            elif key == arcade.key.LEFT:
                self.left_pressed = True
            elif key == arcade.key.RIGHT:
                self.right_pressed = True
            elif key == arcade.key.R:
                self.rewind()

    def on_key_release(self, key, modifiers):
        if not self.rewinding:
            if key == arcade.key.UP:
                self.up_pressed = False
            elif key == arcade.key.DOWN:
                self.down_pressed = False
            elif key == arcade.key.LEFT:
                self.left_pressed = False
            elif key == arcade.key.RIGHT:
                self.right_pressed = False
        if key == arcade.key.R:
            self.stop_rewind()

def main():
    window = GameEngine(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
