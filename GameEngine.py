import arcade
import os
import time
import json
from Platform2 import Platform2
from Platform import Platform
from SolidObject import SolidObject
from Player import Player
from Background import Background
from Ground import Ground
from Ladder import Ladder
from Key import Key
from Door import Door
from MainMenu import MainMenu
from Sounds import Sounds  # Importer la classe Sounds
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, FONT_NAME

#Constants variable
TILE_SCALING = 0.6
PLAYER_JUMP_STRENGTH = 13
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 0.5
ANIMATION_SPEED = 0.15  # Speed of the animation frames
PLAYER_SCALE = 2.0  # Scale to make the player sprite larger

MENU_CAMERA_CENTER_X = SCREEN_WIDTH // 2
MENU_CAMERA_CENTER_Y = SCREEN_HEIGHT // 2

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
        self.is_paused = False
        self.button_width = 200
        self.button_height = 50
        self.player_scale = 1.5
        self.animation_speed = ANIMATION_SPEED
        self.tile_map = None
        self.ground = None
        self.platform = None
        self.ladder = None
        self.background_list = None
        self.player_start_x = 0
        self.player_start_y = 0
        self.player_velocity_y = 0
        self.player_jumping = False
        self.player_climbing = False
        self.key_list = arcade.SpriteList()
        self.door_list = arcade.SpriteList()
        self.has_key = False
        player_data = None
        self.sounds = Sounds()  # Créer une instance de Sounds
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
        base_path = os.path.abspath(os.path.dirname(__file__))
        idle_right_sprite_path = os.path.join(base_path, "Assets", "player", "Samurai", "Sprites", "IDLE_RIGHT.png")
        run_left_sprite_path = os.path.join(base_path, "Assets", "player", "Samurai", "Sprites", "RUN_RIGHT.png")
        idle_left_sprite_path = os.path.join(base_path, "Assets", "player", "Samurai", "Sprites", "IDLE_LEFT.png")
        run_right_sprite_path = os.path.join(base_path, "Assets", "player", "Samurai", "Sprites", "RUN_LEFT.png")

        self.player = Player(self.player_start_x, self.player_start_y+100, PLAYER_MOVEMENT_SPEED, PLAYER_JUMP_STRENGTH, idle_right_sprite_path, run_left_sprite_path, idle_left_sprite_path, run_right_sprite_path, 2*TILE_SCALING, ANIMATION_SPEED)

        self.mana = 0
        self.mana_bar = arcade.SpriteSolidColor(50, self.mana, arcade.color.BLUE)
        self.mana_bar.center_x = SCREEN_WIDTH - 50
        self.mana_bar.center_y = SCREEN_HEIGHT - 100
        self.mana_rate = 1

        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False

        self.base_path = os.path.abspath(os.path.dirname(__file__))
        self.bg_layer_3_path = os.path.join(self.base_path, "Assets", "env", "Clouds", "Clouds 2", "3.png")
        self.bg_layer_4_path = os.path.join(self.base_path, "Assets", "env", "Clouds", "Clouds 2", "4.png")
        self.bg_color = arcade.color.ASH_GREY
        self.bg_width = SCREEN_WIDTH
        self.bg_height = SCREEN_HEIGHT
        self.background = Background(self.bg_width, self.bg_height, self.bg_color, self.bg_layer_3_path,
                                     self.bg_layer_4_path)

        self.camera = arcade.Camera(self.width, self.height)
        self.camera.move_to((MENU_CAMERA_CENTER_X,MENU_CAMERA_CENTER_Y))
        self.menu = MainMenu(self)

        music_path = os.path.join(base_path, "Assets", "sounds", "main_music.mp3")
        self.sounds.setup(music_path, volume=0.5)

        map_name = os.path.join("Assets", "levels","world1.json")

        layer_options = {
            "Ground": {
                "use_spatial_hash": True,
            },
            "Ground 2": {
                "use_spatial_hash": True,
            },
            "Platforme":{
                "use_spatial_hash": True,
            },
            "Platforme Background":{
                "use_spatial_hash": True,
            },
            "Background":{
                "use_spatial_hash": True,
            },
            "Background2":{
                "use_spatial_hash": True,
            }
            
        }

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)
        ground_list = self.tile_map.sprite_lists.get("Ground")
        platform_list = self.tile_map.sprite_lists.get("Platforme")
        platform_background_list = self.tile_map.sprite_lists.get("Platforme Background")
        self.background_list = self.tile_map.sprite_lists.get("Background")
        self.background_list.extend(self.tile_map.sprite_lists.get("Background2"))
        ground_list.extend(self.tile_map.sprite_lists.get("Ground 2"))
        ground_list.extend(platform_list)

        self.ground = Ground(ground_list)
        self.platform = Platform2(platform_list,platform_background_list,direction_x=-1,direction_y=1)
        self.ladder = Ladder(self.tile_map.sprite_lists.get("Echelle"))

        self.load_key_and_door()

        # Set up the physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player,platforms=self.platform.get_list(),ladders=self.ladder.get_lists(), walls=self.ground.get_list(), gravity_constant=GRAVITY)

    def load_key_and_door(self):
        """Load the key and door from the tile map."""
        # Retrieve keys and doors from the tilemap sprite lists
        key_layer = self.tile_map.sprite_lists.get("Clef")
        door_layer = self.tile_map.sprite_lists.get("Porte")

        if key_layer:
            for key_sprite in key_layer:
                key = Key(key_sprite)
                self.key_list.append(key)

        if door_layer:
            for door_sprite in door_layer:
                door = Door(door_sprite)
                self.door_list.append(door)

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
            self.mana_bar.draw()
            # Afficher les couches dans l'ordre correct
            if self.background_list:
                self.background_list.draw()
            if self.ground:
                self.ground.draw()
            if self.platform:
                self.platform.draw()
            if self.ladder:
                self.ladder.draw()
            if self.key_list:
                self.key_list.draw()
            if self.door_list:
                self.door_list.draw()
            self.player.draw()
            self.camera.use()

            if self.is_paused:
                camera_x, camera_y = self.camera.position
                arcade.draw_text("Jeu en pause", SCREEN_WIDTH / 2 + camera_x, SCREEN_HEIGHT / 2 + 100 + camera_y,
                                 arcade.color.GRAY_ASPARAGUS, font_size=23, anchor_x="center",
                                 anchor_y="center", font_name=FONT_NAME)
                arcade.draw_text("Appuyez sur ECHAP pour continuer", SCREEN_WIDTH / 2 + camera_x,
                                 SCREEN_HEIGHT / 2 + 50 + camera_y, arcade.color.GRAY_ASPARAGUS,
                                 font_size=17, anchor_x="center", anchor_y="center", font_name=FONT_NAME)
                new_game_button_x = SCREEN_WIDTH / 2
                new_game_button_y = SCREEN_HEIGHT / 2
                arcade.draw_rectangle_filled(new_game_button_x + camera_x, new_game_button_y + camera_y,
                                              self.button_width, self.button_height, arcade.color.DARK_BLUE)
                arcade.draw_text("Menu", new_game_button_x + camera_x, new_game_button_y + camera_y,
                                 arcade.color.WHITE, font_size=20, anchor_x="center", anchor_y="center",
                                 font_name=FONT_NAME)
                quit_button_x = SCREEN_WIDTH / 2
                quit_button_y = SCREEN_HEIGHT / 2 - 80
                arcade.draw_rectangle_filled(quit_button_x + camera_x, quit_button_y + camera_y,
                                              self.button_width, self.button_height, arcade.color.DARK_RED)
                arcade.draw_text("Quitter", quit_button_x + camera_x, quit_button_y + camera_y,
                                 arcade.color.WHITE, font_size=20, anchor_x="center", anchor_y="center",
                                 font_name=FONT_NAME)

    def on_update(self, delta_time):
        if not self.start_game:
            self.menu.update(delta_time,self.player)
            if self.menu.start_game:
                self.start_game = True
        else:
            if self.is_paused:
                return
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
                self.player.update(self.up_pressed, self.down_pressed, self.left_pressed, self.right_pressed,delta_time)

                self.pos_hist.append((self.player.center_x, self.player.center_y))

                if self.mana < 100:
                    self.mana += self.mana_rate

                if self.ladder.check_climb(self.player):
                    if self.up_pressed:
                        self.player.change_y = 2  # Move up while climbing
                    elif self.down_pressed:
                        self.player.change_y = -2  # Move down while climbing
                    else:
                        self.player.change_y = 0  # Stop climbing if no input
                    self.climbing = True
                else:
                    self.climbing = False
                    # Normal gravity or movement when not climbing
                    self.player.change_y -= 0.2

            if self.up_pressed and self.physics_engine.can_jump():
                self.player.change_y = PLAYER_JUMP_STRENGTH

            # Check for key collection
            key_hit_list = arcade.check_for_collision_with_list(self.player, self.key_list)
            if key_hit_list:
                for key in key_hit_list:
                    key.remove_from_sprite_lists()
                    self.has_key = True  # Player has collected the key

            # Check for door interaction
            door_hit_list = arcade.check_for_collision_with_list(self.player, self.door_list)
            for door in door_hit_list:
                if self.has_key and door.locked:
                    door.unlock()

            self.physics_engine.update()
            self.background.update(delta_time,self.player)
            self.platform.update(delta_time)

    def on_key_press(self, key, modifiers):
        if not self.start_game:
            return
        if key == arcade.key.ESCAPE:
            self.is_paused = not self.is_paused
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
        elif self.is_paused:
            new_game_button_x = SCREEN_WIDTH / 2
            new_game_button_y = SCREEN_HEIGHT / 2
            quit_button_x = SCREEN_WIDTH / 2
            quit_button_y = SCREEN_HEIGHT / 2 - 100
            if (new_game_button_x - self.button_width / 2 < x < new_game_button_x + self.button_width / 2 and
                    new_game_button_y - self.button_height / 2 < y < new_game_button_y + self.button_height / 2):
                self.start_game = False
                self.setup()
                self.is_paused = False
            elif (quit_button_x - self.button_width / 2 < x < quit_button_x + self.button_width / 2 and
                  quit_button_y - self.button_height / 2 < y < quit_button_y + self.button_height / 2):
                arcade.close_window()

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
