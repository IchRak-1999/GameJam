import arcade

class Player(arcade.Sprite):
    def __init__(self, x, y, speed, jump_strength, gravity, idle_right_sprite_path, run_right_sprite_path, idle_left_sprite_path, run_left_sprite_path, scale=4.0, animation_speed=0.1):
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
        self.scale = scale
        self.is_facing_right = True

        self.idle_right_textures = arcade.load_spritesheet(idle_right_sprite_path, sprite_width=93, sprite_height=112, columns=5, count=5)
        self.run_right_textures = arcade.load_spritesheet(run_right_sprite_path, sprite_width=93, sprite_height=112, columns=8, count=8)
        self.idle_left_textures = arcade.load_spritesheet(idle_left_sprite_path, sprite_width=93, sprite_height=112, columns=5, count=5)
        self.run_left_textures = arcade.load_spritesheet(run_left_sprite_path, sprite_width=93, sprite_height=112, columns=8, count=8)

        self.current_texture_index = 0
        self.is_running = False
        self.texture = self.idle_right_textures[self.current_texture_index]

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

        self.check_objects_collisions(solid_objects)
        self.check_platform_collisions(platforms, delta_time)

        if left_pressed:
            self.center_x -= self.speed
            self.is_running = True
            self.is_facing_right = False
        elif right_pressed:
            self.center_x += self.speed
            self.is_running = True
            self.is_facing_right = True
        else:
            self.is_running = False

        self.update_animation(delta_time)

    def check_objects_collisions(self, solid_objects):
        offset = 75
        for solid_object in solid_objects:
            if (self.velocity_y <= 0 and
                self.center_y - offset <= solid_object.sprite.center_y + solid_object.sprite.height / 2 and
                self.center_y - offset >= solid_object.sprite.center_y - solid_object.sprite.height / 2 and
                self.center_x >= solid_object.sprite.center_x - solid_object.sprite.width / 2 and
                self.center_x <= solid_object.sprite.center_x + solid_object.sprite.width / 2):
                
                self.is_on_ground = True
                self.center_y = solid_object.sprite.center_y + solid_object.sprite.height / 2 + offset
                self.velocity_y = 0
                self.is_jumping = False

    def check_platform_collisions(self, platforms, delta_time):
        offset = 75
        for platform in platforms:
            if (self.velocity_y <= 0 and
                self.center_y - offset <= platform.sprite.center_y + platform.sprite.height / 2 and
                self.center_y >= platform.sprite.center_y and
                self.center_x >= platform.sprite.center_x - platform.sprite.width / 2 and
                self.center_x <= platform.sprite.center_x + platform.sprite.width / 2):
                self.is_on_ground = True
                self.center_y = platform.sprite.center_y + platform.sprite.height / 2 + offset
                self.velocity_y = 0
                self.is_jumping = False
                self.center_x += platform.direction_x * 100 * delta_time
                self.center_y += platform.direction_y * 100 * delta_time

    def update_animation(self, delta_time):
        self.current_texture_index += self.animation_speed
        if self.is_running:
            if self.current_texture_index >= len(self.run_right_textures):
                self.current_texture_index = 0
            if self.is_facing_right:
                self.texture = self.run_right_textures[int(self.current_texture_index)]
            else:
                self.texture = self.run_left_textures[int(self.current_texture_index)]
        else:
            if self.current_texture_index >= len(self.idle_right_textures):
                self.current_texture_index = 0
            if self.is_facing_right:
                self.texture = self.idle_right_textures[int(self.current_texture_index)]
            else:
                self.texture = self.idle_left_textures[int(self.current_texture_index)]
