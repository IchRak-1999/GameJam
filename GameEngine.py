import arcade
import time
from Platform import Platform
from SolidObject import SolidObject
from Player import Player

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "???"

class GameEngine(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.WHITE)
        self.scene = None
        self.camera = None
        self.time_slowed = False
        self.mana = None

        self.rewinding = False
        self.rewind_start_time = 0
        self.rewind_duration = 5
        self.pos_hist = []

    # Initialise les éléments du jeu
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

        self.camera = arcade.Camera(self.width, self.height)

    # Permet de retourner en arrière
    def rewind(self):
        if not self.rewinding:
            self.rewinding = True
            self.rewind_start_time = time.time()
            self.pos_hist = self.pos_hist[-int(self.rewind_duration * 60):]

    # Arrête le rewind
    def stop_rewind(self):
        self.rewinding = False
        self.pos_hist = []

    # Met à jour la barre de mana
    def update_mana_bar(self):
        camera_x, camera_y = self.camera.position
        self.mana_bar = arcade.SpriteSolidColor(50, self.mana, arcade.color.BLUE)
        self.mana_bar.center_x = camera_x + SCREEN_WIDTH - 50
        self.mana_bar.center_y = camera_y + SCREEN_HEIGHT - self.mana / 2 - 10

    # Dessine les objets du jeu
    def on_draw(self):
        arcade.start_render()
        self.ground.draw()
        self.mana_bar.draw()
        for platform in self.platforms:
            platform.draw()
        arcade.draw_circle_filled(self.player.center_x, self.player.center_y, 30, arcade.color.GREEN)
        self.camera.use()

    # Met à jour les objets du jeu
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

    # Centre la caméra sur le joueur
    def center_camera_to_player(self):
        screen_center_x = self.player.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player.center_y - (self.camera.viewport_height / 2)

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    # Déplace les plateformes
    def move_platforms(self, delta_time):
        for platform in self.platforms:
            platform.update(delta_time)

    # Action en fonction de la touche appuyée
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

    # Relâche la touche appuyée
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

    # Action en fonction de la touche de la souris appuyée
    def on_mouse_press(self, x, y, button, modifiers):
        pass

    # Relâche la touche de la souris appuyée
    def on_mouse_release(self, x, y, button, modifiers):
        pass

def main():
    window = GameEngine(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
