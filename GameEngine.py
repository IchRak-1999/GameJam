import arcade
import os
import time
from Platform import Platform
from SolidObject import SolidObject
from Player import Player
from Background import Background
from MainMenu import MainMenu
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE

class GameEngine(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.menu = None
        self.start_game = False
        self.camera = None
        self.time_slowed = False
        self.mana = None
        self.rewinding = False
        self.rewind_start_time = 0
        self.rewind_duration = 5
        self.pos_hist = []
        self.background = None
        self.is_paused = False  # Initialisation de l'attribut is_paused

    def setup(self):
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
        self.base_path = os.path.abspath(os.path.dirname(__file__))
        self.bg_layer_3_path = os.path.join(self.base_path, "Assets", "env", "Clouds", "Clouds 2", "3.png")
        self.bg_layer_4_path = os.path.join(self.base_path, "Assets", "env", "Clouds", "Clouds 2", "4.png")
        self.bg_color = arcade.color.ASH_GREY
        self.bg_width = SCREEN_WIDTH
        self.bg_height = SCREEN_HEIGHT
        self.background = Background(self.bg_width, self.bg_height, self.bg_color, self.bg_layer_3_path,
                                     self.bg_layer_4_path)

        self.camera = arcade.Camera(self.width, self.height)

        self.menu = MainMenu(self)

    def rewind(self):
        if self.mana > 0:
            self.rewinding = True
            self.rewind_start_time = time.time()

    def stop_rewind(self):
        self.rewinding = False
        self.pos_hist = []
        self.release_keys()

    def update_mana_bar(self):
        camera_x, camera_y = self.camera.position
        self.mana_bar = arcade.SpriteSolidColor(50, self.mana, arcade.color.BLUE)
        self.mana_bar.center_x = camera_x + SCREEN_WIDTH - 50
        self.mana_bar.center_y = camera_y + SCREEN_HEIGHT - self.mana / 2 - 10

    def on_draw(self):
        arcade.start_render()

        if not self.start_game:
            self.menu.on_draw()
        else:
            self.background.draw()
            self.ground.draw()
            self.mana_bar.draw()
            for platform in self.platforms:
                platform.draw()
            arcade.draw_circle_filled(self.player.center_x, self.player.center_y, 30, arcade.color.GREEN)
            self.camera.use()
            if self.is_paused:
                camera_x, camera_y = self.camera.position
                pause_text = "Jeu en pause. Appuyez sur ESPACE pour continuer."
                arcade.draw_text(pause_text, SCREEN_WIDTH / 2 + camera_x, SCREEN_HEIGHT / 2 + camera_y, arcade.color.GRAY_ASPARAGUS,
                                 font_size=23, anchor_x="center", anchor_y="center")

    def on_update(self, delta_time):
        if not self.start_game:
            self.menu.update(delta_time)
            if self.menu.start_game:
                self.start_game = True
        else:
            if self.is_paused:
                return  # Skip updating if the game is paused
            self.update_mana_bar()
            self.center_camera_to_player()

            if self.rewinding:
                rewind_time_elapsed = time.time() - self.rewind_start_time
                rewind_frame_count = int(rewind_time_elapsed * 60)
                self.mana -= self.mana_rate
                for platform in self.platforms:
                    platform.update(-delta_time)

                if self.mana <= 0:
                    self.stop_rewind()
                elif rewind_frame_count < len(self.pos_hist):
                    self.player.center_x, self.player.center_y = self.pos_hist[-rewind_frame_count - 1]
                else:
                    self.stop_rewind()
            else:
                self.player.update(self.up_pressed, self.down_pressed, self.left_pressed, self.right_pressed,
                                   self.platforms, delta_time)
                for platform in self.platforms:
                    platform.update(delta_time)

                self.pos_hist.append((self.player.center_x, self.player.center_y))

                if self.mana < 100:
                    self.mana += self.mana_rate

            self.background.update(delta_time)

    def on_key_press(self, key, modifiers):
        if not self.start_game:
            return
        if key == arcade.key.SPACE:  # Pressing space toggles the menu
            self.is_paused = not self.is_paused
            # self.show_menu = self.is_paused  # Show the menu if paused ---> à voir
        elif not self.rewinding:
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
        if not self.start_game:
            return

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

    def release_keys(self):
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.start_game:
            self.menu.on_mouse_press(x, y, button, modifiers)

    def center_camera_to_player(self):
        screen_center_x = self.player.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player.center_y - (self.camera.viewport_height / 2)

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0

        self.camera.move_to((screen_center_x, screen_center_y))


def main():
    window = GameEngine(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()

