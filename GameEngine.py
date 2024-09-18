import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "ChronoBlade"

class GameEngine(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLUE)

        self.player_x = 400
        self.player_y = 300
        self.player_speed = 5
        self.gravity = -0.5
        self.jump_strength = 10
        self.player_velocity_y = 0
        self.is_jumping = False
        self.is_on_ground = False

        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False

        self.platforms = [
            arcade.SpriteSolidColor(200, 20, arcade.color.RED)
            for _ in range(2)
        ]
        self.platforms[0].center_x = 400
        self.platforms[0].center_y = 50
        self.platforms[1].center_x = 300
        self.platforms[1].center_y = 250

        self.platform_direction = 1

        self.ground = arcade.SpriteSolidColor(SCREEN_WIDTH, 20, arcade.color.BLACK)
        self.ground.center_x = SCREEN_WIDTH // 2
        self.ground.center_y = 30

        self.camera = None

    def setup(self):
         self.camera = arcade.Camera(self.width, self.height)


    def on_draw(self):
        arcade.start_render()
        self.ground.draw()
        for platform in self.platforms:
            platform.draw()
        arcade.draw_circle_filled(self.player_x, self.player_y, 30, arcade.color.GREEN)
        self.camera.use()

    def on_update(self, delta_time):
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

    def center_camera_to_player(self):
        screen_center_x = self.player_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_y - (
            self.camera.viewport_height / 2
        )

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def check_platform_collisions(self):
        self.is_on_ground = False
        for platform in self.platforms:
            if (self.player_y - 30 <= platform.center_y + 10 and
                self.player_y - 30 >= platform.center_y - 10 and
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


    def move_platforms(self, delta_time):
        for platform in self.platforms:
            platform.center_x += self.platform_direction * 100 * delta_time
            if platform.center_x > SCREEN_WIDTH - platform.width // 2 or platform.center_x < platform.width // 2:
                self.platform_direction *= -1

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
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
