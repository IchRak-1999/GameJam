import arcade
import os
import json
from Platform2 import Platform2
from Player import Player
from Background import Background
from Ground import Ground
from Ladder import Ladder

# Constants for screen width, height, and title
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "ChronoBlade"
TILE_SCALING = 0.6
PLAYER_JUMP_SPEED = 15
PLAYER_MOVEMENT_SPEED = 3
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

        self.player_list = None
        # Layered attributes
        self.tile_map = None
        self.ground = None
        self.platform = None
        self.ladder = None
        self.background_list = None
        self.player_sprite = None
        self.player_start_x = 0
        self.player_start_y = 0
        self.player_velocity_y = 0
        self.player_jumping = False
        self.player_climbing = False

        # Background handling
        self.background = None

        # Player movement keys
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False

        # Animation variables
        self.idle_textures = []
        self.run_textures = []
        self.current_texture_index = 0
        self.time_since_last_frame = 0
        self.is_running = False

        self.tile_map = None
            
        player_data = None

        # Background attributes
        self.bg_layer_1 = None
        self.bg_layer_2 = None
        self.bg_layer_3 = None
        self.bg_layer_4 = None
        self.bg_layer_3_x_1 = 0  # Initial x position for first instance of layer 3
        self.bg_layer_3_x_2 = SCREEN_WIDTH  # Initial x position for second instance of layer 3
        self.bg_layer_4_x_1 = 0  # Initial x position for first instance of layer 4
        self.bg_layer_4_x_2 = SCREEN_WIDTH  # Initial x position for second instance of layer 4


        # Physics engine
        self.physics_engine = None

        map_width = 0
        map_height = 0

        with open("./Assets/levels/world1.json") as f:

            map_data = json.load(f)

            for layer in map_data['layers']:
                if layer['name'] == 'Player':
                    player_data = layer['data']
                    map_width = layer['width']
                    map_height = layer['height']
                    break

            player_index = player_data.index(6565)

        self.player_start_x = player_index % map_width
        self.player_start_y = player_index // map_width
        self.player_start_y = map_height - self.player_start_y - 1

        self.player_start_x = self.player_start_x * (32 * TILE_SCALING)
        self.player_start_y = self.player_start_y * (32 * TILE_SCALING)

    def setup(self):
        
        self.player_list = arcade.SpriteList()

        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width,self.height)

        map_name = os.path.join("Assets", "levels","world1.json")

        layer_options = {
            "Ground": {
                "use_spatial_hash": True,
            },
            "Ground 2": {
                "use_spatial_hash": True,
            },
        }

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)
        ground_list = self.tile_map.sprite_lists.get("Ground")
        platform_list = self.tile_map.sprite_lists.get("Platforme")
        platform_background_list = self.tile_map.sprite_lists.get("Platforme Background")
        self.background_list = self.tile_map.sprite_lists.get("Background")

        ground_list.extend(self.tile_map.sprite_lists.get("Ground 2"))
        ground_list.extend(platform_list)

        self.ground = Ground(ground_list)
        self.platform = Platform2(platform_list,platform_background_list,direction_x=-1,direction_y=1)
        self.ladder = Ladder(self.tile_map.sprite_lists.get("Echelle"))
        player_spawn_object = self.tile_map.sprite_lists.get("Player")
        
        print(player_spawn_object)

        """if player_spawn_object:
            self.player_start_x = player_spawn_object[0].shape[0]
            self.player_start_y = player_spawn_object[0].shape[1]
            print(f'p x: {player_spawn_object[0].shape[0]} , y: {player_spawn_object[0].shape[1]}')
        """
        print(f'p x: {self.player_start_x} , y: {self.player_start_y}')
        print(player_spawn_object)

        # Build the path to your sprites
        base_path = os.path.abspath(os.path.dirname(__file__))
        idle_sprite_path = os.path.join(base_path, "Assets", "player", "Samurai", "Sprites", "IDLE_RIGHT.png")
        run_sprite_path = os.path.join(base_path, "Assets", "player", "Samurai", "Sprites", "RUN_RIGHT.png")

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

        self.player_sprite = arcade.Sprite(scale=2*TILE_SCALING)  # Increase size with scale
        self.player_sprite.texture = self.idle_textures[0]  # Set texture to the first idle frame
        self.player_sprite.center_x = self.player_start_x
        self.player_sprite.center_y = self.player_start_y + 100
        self.player_list.append(self.player_sprite)


        # Set up the physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,platforms=self.platform.get_list(),ladders=self.ladder.get_lists(), walls=self.ground.get_list(), gravity_constant=GRAVITY)


    def on_draw(self):

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


        # Afficher les couches dans l'ordre correct
        if self.background_list:
            self.background_list.draw()
        if self.ground:
            self.ground.draw()
        if self.platform:
            self.platform.draw()
        if self.ladder:
            self.ladder.draw()

        # Dessiner le joueur
        if self.player_sprite:
            self.player_sprite.draw()

        self.camera.use()
        self.gui_camera.use()

    def on_update(self, delta_time):
        """ Game logic, updates, and animation handling """

        if self.ladder.check_climb(self.player_sprite):
            if self.up_pressed:
                self.player_sprite.change_y = 2  # Move up while climbing
            elif self.down_pressed:
                self.player_sprite.change_y = -2  # Move down while climbing
            else:
                self.player_sprite.change_y = 0  # Stop climbing if no input
            self.climbing = True
        else:
            self.climbing = False
            # Normal gravity or movement when not climbing
            self.player_sprite.change_y -= 0.2

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
        self.platform.update(delta_time)
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

    def update(self, delta_time):
        # Appliquer la gravité si le joueur ne touche pas le sol
        self.center_camera_to_player()
        pass

    def on_key_press(self, key, modifiers):
        """ Called whenever a key is pressed. """
        if key == arcade.key.UP or key == arcade.key.Z:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """ Called whenever a key is released. """
        if key == arcade.key.UP or key == arcade.key.Z:
            self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

def main():
    window = GameEngine(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
