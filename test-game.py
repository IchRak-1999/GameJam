import arcade
import os

# Constants for screen width, height, and title
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "ChronoBlade"

# Constants for player properties
PLAYER_MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED = 12
GRAVITY = 0.2
ANIMATION_SPEED = 0.15  # Speed of the animation frames
PLAYER_SCALE = 2.0  # Scale to make the player sprite larger

# Background scrolling speeds
BACKGROUND_SCROLL_SPEED_3 = 1  # Layer 3 scroll speed
BACKGROUND_SCROLL_SPEED_4 = 2  # Layer 4 scroll speed

class GameEngine(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.ASH_GREY)

        # Player attributes
        self.player_list = None
        self.wall_list = None
        self.player_sprite = None

        self.up_pressed = False
        self.left_pressed = False
        self.right_pressed = False

        # Animation variables
        self.idle_textures = []
        self.run_textures = []
        self.current_texture_index = 0
        self.time_since_last_frame = 0
        self.is_running = False

        self.physics_engine = None

        # Background attributes
        self.bg_layer_1 = None
        self.bg_layer_2 = None
        self.bg_layer_3 = None
        self.bg_layer_4 = None
        self.bg_layer_3_x_1 = 0  # Initial x position for first instance of layer 3
        self.bg_layer_3_x_2 = SCREEN_WIDTH  # Initial x position for second instance of layer 3
        self.bg_layer_4_x_1 = 0  # Initial x position for first instance of layer 4
        self.bg_layer_4_x_2 = SCREEN_WIDTH  # Initial x position for second instance of layer 4

    def setup(self):
        """ Set up the game and initialize variables """
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # Build the path to your sprites
        base_path = os.path.abspath(os.path.dirname(__file__))
        idle_sprite_path = os.path.join(base_path, "Assets", "player", "Samurai", "Sprites", "IDLE.png")
        run_sprite_path = os.path.join(base_path, "Assets", "player", "Samurai", "Sprites", "RUN.png")

        bg_layer_1_path = os.path.join(base_path, "Assets", "env", "Clouds", "Clouds 2", "1.png")
        bg_layer_2_path = os.path.join(base_path, "Assets", "env", "Clouds", "Clouds 2", "2.png")
        bg_layer_3_path = os.path.join(base_path, "Assets", "env", "Clouds", "Clouds 2", "3.png")
        bg_layer_4_path = os.path.join(base_path, "Assets", "env", "Clouds", "Clouds 2", "4.png")

        print(f"Idle Sprite Path: {idle_sprite_path}")
        print(f"Run Sprite Path: {run_sprite_path}")

        # Load background textures
        self.bg_layer_1 = arcade.load_texture(bg_layer_1_path)
        self.bg_layer_2 = arcade.load_texture(bg_layer_2_path)
        self.bg_layer_3 = arcade.load_texture(bg_layer_3_path)
        self.bg_layer_4 = arcade.load_texture(bg_layer_4_path)

        # Check if files exist
        if not os.path.exists(idle_sprite_path) or not os.path.exists(run_sprite_path):
            print(f"Error: One or both of the sprite files are not found.")
            return

        # Load Idle and Run spritesheets with correct frame dimensions
        try:
            # Load Idle: 465x112 with 93x112 frames (5 frames in total)
            self.idle_textures = arcade.load_spritesheet(
                idle_sprite_path, sprite_width=93, sprite_height=112, columns=5, count=5
            )

            # Load Run: 744x112 with 93x112 frames (8 frames in total)
            self.run_textures = arcade.load_spritesheet(
                run_sprite_path, sprite_width=93, sprite_height=112, columns=8, count=8
            )
        except Exception as e:
            print(f"Error loading spritesheets: {e}")
            return

        # Set up the player, starting with the first idle frame
        self.player_sprite = arcade.Sprite(scale=PLAYER_SCALE)  # Increase size with scale
        self.player_sprite.texture = self.idle_textures[0]  # Set texture to the first idle frame
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.player_sprite.set_hit_box([(-32, -32), (32, -32), (32, 32), (-32, 32)])  # Manually set hitbox
        self.player_list.append(self.player_sprite)

        # Create the platforms
        for x in range(0, 800, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", 1)
            wall.center_x = x
            wall.center_y = 32
            wall.set_hit_box([(-32, -32), (32, -32), (32, 32), (-32, 32)])  # Manually set hitbox for walls
            self.wall_list.append(wall)

        for x in range(200, 600, 200):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", 1)
            wall.center_x = x
            wall.center_y = 200
            wall.set_hit_box([(-32, -32), (32, -32), (32, 32), (-32, 32)])  # Manually set hitbox for walls
            self.wall_list.append(wall)

        # Verify player and wall textures
        if not self.player_sprite.texture:
            print("Error: Player sprite texture is not loaded correctly.")
            return

        # Ensure wall sprites have proper textures
        for wall in self.wall_list:
            if not wall.texture:
                print("Error: Wall sprite texture is not loaded correctly.")
                return

        # Set up the physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, gravity_constant=GRAVITY)

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()

        # Draw background layers
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.bg_layer_1)  # Static background layer 1
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.bg_layer_2)  # Static background layer 2

        # Parallax scrolling for layer 3 (multiple instances)
        arcade.draw_lrwh_rectangle_textured(self.bg_layer_3_x_1, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.bg_layer_3)
        arcade.draw_lrwh_rectangle_textured(self.bg_layer_3_x_2, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.bg_layer_3)

        # Parallax scrolling for layer 4 (multiple instances)
        arcade.draw_lrwh_rectangle_textured(self.bg_layer_4_x_1, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.bg_layer_4)
        arcade.draw_lrwh_rectangle_textured(self.bg_layer_4_x_2, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.bg_layer_4)

        # Draw the player and walls
        self.wall_list.draw()
        self.player_list.draw()

    def on_update(self, delta_time):
        """ Game logic, updates, and animation handling """
        if self.up_pressed and self.physics_engine.can_jump():
            self.player_sprite.change_y = PLAYER_JUMP_SPEED

        if self.left_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
            self.is_running = True
        elif self.right_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
            self.is_running = True
        else:
            self.player_sprite.change_x = 0
            self.is_running = False

        # Update the physics engine
        try:
            self.physics_engine.update()
        except Exception as e:
            print(f"Error in physics engine update: {e}")
            print(f"Player sprite position: {self.player_sprite.position}")
            print(f"Player sprite hitbox: {self.player_sprite.get_adjusted_hit_box()}")

        # Update the player's animation
        self.update_animation(delta_time)

        # Update background positions for parallax scrolling
        self.bg_layer_3_x_1 -= BACKGROUND_SCROLL_SPEED_3
        self.bg_layer_3_x_2 -= BACKGROUND_SCROLL_SPEED_3
        self.bg_layer_4_x_1 -= BACKGROUND_SCROLL_SPEED_4
        self.bg_layer_4_x_2 -= BACKGROUND_SCROLL_SPEED_4

        # Reset background positions to create a continuous scrolling effect for layer 3
        if self.bg_layer_3_x_1 <= -SCREEN_WIDTH:
            self.bg_layer_3_x_1 = SCREEN_WIDTH
        if self.bg_layer_3_x_2 <= -SCREEN_WIDTH:
            self.bg_layer_3_x_2 = SCREEN_WIDTH

        # Reset background positions to create a continuous scrolling effect for layer 4
        if self.bg_layer_4_x_1 <= -SCREEN_WIDTH:
            self.bg_layer_4_x_1 = SCREEN_WIDTH
        if self.bg_layer_4_x_2 <= -SCREEN_WIDTH:
            self.bg_layer_4_x_2 = SCREEN_WIDTH

    def update_animation(self, delta_time):
        """ Update the animation for the player """
        self.time_since_last_frame += delta_time

        # Only update if enough time has passed for the next frame
        if self.time_since_last_frame > ANIMATION_SPEED:
            self.time_since_last_frame = 0

            # Switch between idle and run animations based on movement
            if self.is_running:
                # Update run animation
                self.current_texture_index += 1
                if self.current_texture_index >= len(self.run_textures):
                    self.current_texture_index = 0
                self.player_sprite.texture = self.run_textures[self.current_texture_index]
            else:
                # Update idle animation
                self.current_texture_index += 1
                if self.current_texture_index >= len(self.idle_textures):
                    self.current_texture_index = 0
                self.player_sprite.texture = self.idle_textures[self.current_texture_index]

    def on_key_press(self, key, modifiers):
        """ Called whenever a key is pressed. """
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """ Called whenever a key is released. """
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

def main():
    window = GameEngine(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
