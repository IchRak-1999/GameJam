import arcade
import time
from Platform import Platform
from SolidObject import SolidObject

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Game with Platforms"

class GameEngine(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.WHITE)
        self.scene = None
        self.player_sprite = None
        self.sword_sprite = None 
        self.physics_engine = None
        self.camera = None
        self.background = None
        self.time_slowed = False
        self.mana = None

        self.rewinding = False
        self.rewind_start_time = 0
        self.rewind_duration = 5
        self.pos_hist = []

    # Initialise les éléments du jeu
    def setup(self):
        self.player_x = 400
        self.player_y = 300
        self.player_speed = 5
        self.gravity = -0.5
        self.jump_strength = 10
        self.player_velocity_y = 0
        self.is_jumping = False
        self.is_on_ground = False

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
            Platform(200, 20, arcade.color.RED, 400, 50),
            Platform(200, 20, arcade.color.RED, 300, 250),
            Platform(200, 20, arcade.color.RED, 400, 200)
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
        arcade.draw_circle_filled(self.player_x, self.player_y, 30, arcade.color.GREEN)
        self.camera.use()

    # Met à jour les objets du jeu
    def on_update(self, delta_time):
        self.update_mana_bar()
        if self.rewinding:
            rewind_time_elapsed = time.time() - self.rewind_start_time
            rewind_frame_count = int(rewind_time_elapsed * 60)
            self.mana -= self.mana_rate
            self.center_camera_to_player()
            if self.mana <= 0:
                self.stop_rewind()
            elif rewind_frame_count < len(self.pos_hist):
                self.player_x, self.player_y = self.pos_hist[-rewind_frame_count - 1]
            else:
                self.stop_rewind()
        else:
            if self.up_pressed and self.is_on_ground:
                self.player_velocity_y = self.jump_strength
                self.is_jumping = True
                self.is_on_ground = False
            
            self.player_velocity_y += self.gravity
            self.player_y += self.player_velocity_y

            if self.player_y <= 30:
                self.player_y = 30
                self.is_on_ground = True
                self.player_velocity_y = 0
                self.is_jumping = False

            self.check_platform_collisions()
            self.move_platforms(delta_time)

            if self.up_pressed:
                self.player_y += self.player_speed
            if self.down_pressed:
                self.player_y -= self.player_speed
            if self.left_pressed:
                self.player_x -= self.player_speed
            if self.right_pressed:
                self.player_x += self.player_speed

            self.center_camera_to_player()

            self.pos_hist.append((self.player_x, self.player_y))
            if self.mana < 100:
                self.mana += self.mana_rate

    # Centre la caméra sur le joueur
    def center_camera_to_player(self):
        screen_center_x = self.player_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_y - (self.camera.viewport_height / 2)

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    # Vérifie les collisions avec les plateformes
    def check_platform_collisions(self):
        self.is_on_ground = False
        for platform in self.platforms:
            if (self.player_y - 30 <= platform.sprite.center_y + self.jump_strength and
                self.player_y - 30 >= platform.sprite.center_y - self.jump_strength and
                self.player_x >= platform.sprite.center_x - 100 and
                self.player_x <= platform.sprite.center_x + 100):
                self.is_on_ground = True
                self.player_y = platform.sprite.center_y + 30
                self.player_velocity_y = 0
                self.is_jumping = False

        if self.player_y <= 30:
            self.player_y = 30
            self.is_on_ground = True
            self.player_velocity_y = 0
            self.is_jumping = False

    # Déplace les plateformes
    def move_platforms(self, delta_time):
        for platform in self.platforms:
            platform.update(delta_time)

    # Action en fonction de la touche appuyée
    def on_key_press(self, key, modifiers):
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
        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
        elif key == arcade.key.R:
            self.stop_rewind()

    # Action en fonction de la touche de la souris appuyée
    def on_mouse_press(self, x, y, button, modifiers):
        pass

    # Relache la touche de la souris appuyée
    def on_mouse_release(self, x, y, button, modifiers):
        pass

def main():
    window = GameEngine(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
