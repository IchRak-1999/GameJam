import arcade
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "???"

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

    # initialise les éléments du jeu
    def setup(self):
        self.player_x = 400
        self.player_y = 300
        self.player_speed = 5
        self.gravity = -0.5
        self.jump_strength = 10
        self.player_velocity_y = 0
        self.is_jumping = False
        self.is_on_ground = False

        """
        self.mana_bar_bg = arcade.SpriteSolidColor(55, 105, arcade.color.BLACK)
        self.mana_bar_bg.center_x = SCREEN_WIDTH - 50
        self.mana_bar_bg.center_y = SCREEN_HEIGHT - 100
        """

        self.mana = 0
        self.mana_bar = arcade.SpriteSolidColor(50, self.mana, arcade.color.BLUE)
        self.mana_bar.center_x = SCREEN_WIDTH - 50
        self.mana_bar.center_y = SCREEN_HEIGHT - 100
        self.mana_rate = 1

        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False

        # à modifier
        self.platforms = [
            arcade.SpriteSolidColor(200, 20, arcade.color.RED)
            for _ in range(3)
        ]
        self.platforms[0].center_x = 400
        self.platforms[0].center_y = 50
        self.platforms[1].center_x = 300
        self.platforms[1].center_y = 250
        self.platforms[2].center_x = 400
        self.platforms[2].center_y = 200
        self.platform_direction = 1

        self.ground = arcade.SpriteSolidColor(SCREEN_WIDTH, 20, arcade.color.BLACK)
        self.ground.center_x = SCREEN_WIDTH // 2
        self.ground.center_y = 10

        self.camera = arcade.Camera(self.width, self.height)

    # permet de retourner en arrière
    def rewind(self):
        if not self.rewinding:
            self.rewinding = True
            self.rewind_start_time = time.time()
            self.pos_hist = self.pos_hist[-int(self.rewind_duration * 60):]

    # arrete le rewind
    def stop_rewind(self):
        self.rewinding = False
        self.pos_hist = []

    # met a jour la bar de mana
    def update_mana_bar(self):
        camera_x, camera_y = self.camera.position
        self.mana_bar = arcade.SpriteSolidColor(50, self.mana, arcade.color.BLUE)
        self.mana_bar.center_x = camera_x + SCREEN_WIDTH - 50 
        self.mana_bar.center_y = camera_y + SCREEN_HEIGHT - self.mana / 2 - 10

    # dessine les objets du jeu
    def on_draw(self):
        arcade.start_render()
        self.ground.draw()
        self.mana_bar.draw()
        #self.mana_bar_bg.draw()
        for platform in self.platforms:
            platform.draw()
        arcade.draw_circle_filled(self.player_x, self.player_y, 30, arcade.color.GREEN)
        self.camera.use()

    # met a jour les objets du jeu
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
            
    # centre la camera sur la joueur
    def center_camera_to_player(self):
        screen_center_x = self.player_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_y - (self.camera.viewport_height / 2)

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    # verifie les collisions avec le decor(à modifier)
    def check_platform_collisions(self):
        self.is_on_ground = False
        for platform in self.platforms:
            if (self.player_y - 30 <= platform.center_y + self.jump_strength and
                self.player_y - 30 >= platform.center_y - self.jump_strength and
                self.player_x >= platform.center_x - 100 and
                self.player_x <= platform.center_x + 100):
                self.is_on_ground = True
                self.player_y = platform.center_y + 30
                self.player_velocity_y = 0
                self.is_jumping = False

        if self.player_y <= 30:
            self.player_y = 30
            self.is_on_ground = True
            self.player_velocity_y = 0
            self.is_jumping = False

    # deplace les plateformes(à modifier)
    def move_platforms(self, delta_time):
        for platform in self.platforms:
            platform.center_x += self.platform_direction * 100 * delta_time
            if platform.center_x > SCREEN_WIDTH - platform.width // 2 or platform.center_x < platform.width // 2:
                self.platform_direction *= -1

    # action en fonction de la touche appuyée
    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    # relache la touche appuyée
    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

    # action en fonction de la touche de la souris appuyée
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.rewind()

    # relache la touche de la souris appuyée
    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.stop_rewind()

def main():
    window = GameEngine(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
