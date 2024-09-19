import arcade
import os

class Player(arcade.Sprite):
    def __init__(self, x, y, speed, jump_strength, gravity, idle_sprite_path, run_sprite_path, scale=4.0, animation_speed=0.1):
        super().__init__(scale=scale)
        self.center_x = x
        self.center_y = y
        self.speed = speed
        self.jump_strength = jump_strength
        self.gravity = gravity
        self.velocity_y = 0
        self.is_jumping = False
        self.is_on_ground = False
        self.animation_speed = animation_speed
        self._scale = scale

        self.idle_textures = arcade.load_spritesheet(idle_sprite_path, sprite_width=93, sprite_height=112, columns=5, count=5)
        self.run_textures = arcade.load_spritesheet(run_sprite_path, sprite_width=93, sprite_height=112, columns=8, count=8)
        self.current_texture_index = 0
        self.is_running = False
        self.texture = self.idle_textures[self.current_texture_index]

    def update(self, up_pressed, down_pressed, left_pressed, right_pressed, solid_objects, platforms, delta_time):
        if up_pressed and self.is_on_ground:
            self.velocity_y = self.jump_strength
            self.is_jumping = True
            self.is_on_ground = False

        self.velocity_y += self.gravity
        self.center_y += self.velocity_y

        if self.center_y <= 30:
            self.center_y = 30
            self.is_on_ground = True
            self.velocity_y = 0
            self.is_jumping = False

        self.check_objects_collisions(platforms)
        self.check_objects_collisions(solid_objects)

        if left_pressed:
            self.center_x -= self.speed
            self.is_running = True
        elif right_pressed:
            self.center_x += self.speed
            self.is_running = True
        else:
            self.is_running = False
        self.update_animation(delta_time)

    def check_objects_collisions(self, solid_objects):
        self.is_on_ground = False
        offset = 75
        for solid_object in solid_objects:
            if (self.center_y - offset <= solid_object.sprite.center_y + solid_object.sprite.height / 2 and
                self.center_y - offset >= solid_object.sprite.center_y - solid_object.sprite.height / 2 and
                self.center_x >= solid_object.sprite.center_x - solid_object.sprite.width / 2 and
                self.center_x <= solid_object.sprite.center_x + solid_object.sprite.width / 2):
                self.is_on_ground = True
                self.center_y = solid_object.sprite.center_y + solid_object.sprite.height / 2 + offset
                self.velocity_y = 0
                self.is_jumping = False

    def update_animation(self, delta_time):
        self.current_texture_index += self.animation_speed
        if self.is_running:
            if self.current_texture_index >= len(self.run_textures):
                self.current_texture_index = 0
            self.texture = self.run_textures[int(self.current_texture_index)]
        else:
            if self.current_texture_index >= len(self.idle_textures):
                self.current_texture_index = 0
            self.texture = self.idle_textures[int(self.current_texture_index)]
